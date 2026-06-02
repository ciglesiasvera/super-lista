from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView

from super_lista.core.models import AuditEvent
from super_lista.lists.models import ShoppingList
from super_lista.lists.permissions import EditorRequiredMixin, ListAccessMixin
from super_lista.purchases.forms import PurchaseForm, PurchaseLineForm, ReceiptForm
from super_lista.purchases.models import Purchase, PurchaseLine, Receipt


class PurchaseCreateView(EditorRequiredMixin, CreateView):
    """Create a purchase for a specific shopping list."""
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchases/purchase_form.html'

    def get_shopping_list(self):
        pk = self.kwargs.get('list_pk')
        return get_object_or_404(ShoppingList, pk=pk)

    def form_valid(self, form):
        shopping_list = self.get_shopping_list()
        form.instance.shopping_list = shopping_list
        form.instance.purchased_by = self.request.user
        # Calculate total from discount/tax if subtotal not set
        response = super().form_valid(form)
        AuditEvent.log(
            actor=self.request.user,
            entity_type='Purchase',
            entity_id=self.object.id,
            action='purchase',
        )
        messages.success(self.request, 'Compra registrada.')
        return redirect('purchase_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_obj'] = self.get_shopping_list()
        return context

    def get_success_url(self):
        return reverse('purchase_detail', kwargs={'pk': self.object.pk})


class PurchaseDetailView(ListAccessMixin, DetailView):
    """Show purchase details with lines and receipt."""
    model = Purchase
    template_name = 'purchases/purchase_detail.html'
    context_object_name = 'purchase'

    def get_shopping_list(self):
        purchase = self.get_object()
        return purchase.shopping_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase = self.object
        context['lines'] = purchase.lines.all()
        context['receipt'] = getattr(purchase, 'receipt', None)
        context['receipt_form'] = ReceiptForm()
        context['line_form'] = PurchaseLineForm()
        return context


class PurchaseLineCreateView(EditorRequiredMixin, CreateView):
    """Add a line to a purchase (inline/HTMX friendly)."""
    model = PurchaseLine
    form_class = PurchaseLineForm
    template_name = 'purchases/purchase_form.html'

    def get_shopping_list(self):
        purchase = get_object_or_404(Purchase, pk=self.kwargs['purchase_pk'])
        return purchase.shopping_list

    def form_valid(self, form):
        purchase = get_object_or_404(Purchase, pk=self.kwargs['purchase_pk'])
        form.instance.purchase = purchase
        qty = form.cleaned_data['quantity']
        price = form.cleaned_data['unit_price']
        form.instance.line_total = qty * price
        # Calculate difference if linked to a list item
        response = super().form_valid(form)
        # Update purchase totals
        self._update_purchase_totals(purchase)
        messages.success(self.request, 'Línea agregada a la compra.')
        return redirect('purchase_detail', pk=purchase.pk)

    def _update_purchase_totals(self, purchase):
        lines = purchase.lines.all()
        subtotal = sum((l.line_total or Decimal('0')) for l in lines)
        purchase.subtotal = subtotal
        discount = purchase.discount_total or Decimal('0')
        tax = purchase.tax_total or Decimal('0')
        purchase.total_paid = subtotal - discount + tax
        purchase.save(update_fields=['subtotal', 'total_paid'])


class PurchaseDeleteView(EditorRequiredMixin, DeleteView):
    """Delete a purchase."""
    model = Purchase
    template_name = 'purchases/purchase_confirm_delete.html'
    pk_url_kwarg = 'pk'

    def get_shopping_list(self):
        return self.get_object().shopping_list

    def get_success_url(self):
        return reverse('list_detail', kwargs={'pk': self.object.shopping_list.pk})

    def form_valid(self, form):
        AuditEvent.log(
            actor=self.request.user,
            entity_type='Purchase',
            entity_id=self.object.id,
            action='delete',
        )
        messages.success(self.request, 'Compra eliminada.')
        return super().form_valid(form)


class ReceiptUploadView(EditorRequiredMixin, FormView):
    """Upload a receipt for a purchase."""
    form_class = ReceiptForm
    template_name = 'purchases/purchase_detail.html'

    def get_shopping_list(self):
        purchase = get_object_or_404(Purchase, pk=self.kwargs['purchase_pk'])
        return purchase.shopping_list

    def form_valid(self, form):
        purchase = get_object_or_404(Purchase, pk=self.kwargs['purchase_pk'])
        receipt, created = Receipt.objects.update_or_create(
            purchase=purchase,
            defaults={
                'receipt_number': form.cleaned_data.get('receipt_number'),
                'issued_at': form.cleaned_data.get('issued_at'),
                'file': form.cleaned_data.get('file'),
                'notes': form.cleaned_data.get('notes'),
            },
        )
        AuditEvent.log(
            actor=self.request.user,
            entity_type='Receipt',
            entity_id=receipt.pk,
            action='upload',
        )
        messages.success(self.request, 'Boleta subida exitosamente.')
        return redirect('purchase_detail', pk=purchase.pk)


class ReceiptDeleteView(EditorRequiredMixin, DeleteView):
    """Delete a receipt."""
    model = Receipt
    pk_url_kwarg = 'receipt_pk'

    def get_shopping_list(self):
        receipt = self.get_object()
        return receipt.purchase.shopping_list

    def get_success_url(self):
        return reverse('purchase_detail', kwargs={'pk': self.object.purchase.pk})

    def form_valid(self, form):
        receipt = self.get_object()
        purchase_pk = receipt.purchase.pk
        receipt.delete()
        messages.success(self.request, 'Boleta eliminada.')
        return redirect('purchase_detail', pk=purchase_pk)
