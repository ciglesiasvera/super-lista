from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from super_lista.items.forms import ListItemForm, CategoryForm
from super_lista.items.models import ListItem, Category, ProductTemplate
from super_lista.lists.models import ShoppingList, ListMember
from super_lista.lists.permissions import EditorRequiredMixin, can_edit, get_user_role


class ListItemCreateView(EditorRequiredMixin, CreateView):
    """Add a new item to a shopping list."""
    model = ListItem
    form_class = ListItemForm
    template_name = 'items/item_form.html'

    def get_shopping_list(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(ShoppingList, pk=pk)

    def form_valid(self, form):
        shopping_list = self.get_shopping_list()
        form.instance.list = shopping_list
        form.instance.created_by = self.request.user

        # Auto-fill from template if provided
        template_pk = self.request.POST.get('template')
        if template_pk:
            try:
                template = ProductTemplate.objects.get(pk=template_pk)
                form.instance.template = template
                if not form.instance.category_id and template.default_category:
                    form.instance.category = template.default_category
                if not form.instance.unit and template.default_unit:
                    form.instance.unit = template.default_unit
            except ProductTemplate.DoesNotExist:
                pass

        response = super().form_valid(form)

        # Mark template as frequent
        template = form.instance.template
        if template and not template.is_frequent:
            template.is_frequent = True
            template.save(update_fields=['is_frequent'])

        messages.success(self.request, f'"{form.instance.name}" agregado a la lista.')
        return redirect('list_detail', pk=shopping_list.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_obj'] = self.get_shopping_list()
        return context


class ListItemUpdateView(EditorRequiredMixin, UpdateView):
    """Edit an existing list item."""
    model = ListItem
    form_class = ListItemForm
    template_name = 'items/item_form.html'
    pk_url_kwarg = 'item_pk'

    def get_shopping_list(self):
        item = self.get_object()
        return item.list

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Ítem actualizado.')
        return redirect('list_detail', pk=self.object.list.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_obj'] = self.object.list
        return context


class ListItemDeleteView(EditorRequiredMixin, DeleteView):
    """Remove an item from a list."""
    model = ListItem
    template_name = 'items/item_confirm_delete.html'
    pk_url_kwarg = 'item_pk'

    def get_shopping_list(self):
        item = self.get_object()
        return item.list

    def get_success_url(self):
        return reverse('list_detail', kwargs={'pk': self.object.list.pk})

    def form_valid(self, form):
        shopping_list = self.object.list
        messages.success(self.request, f'"{self.object.name}" eliminado.')
        return super().form_valid(form)


class ToggleItemStatusView(EditorRequiredMixin, UpdateView):
    """Toggle item status (pending → bought → pending, etc.)."""
    model = ListItem
    fields = ['status']
    pk_url_kwarg = 'item_pk'

    def get_shopping_list(self):
        return self.get_object().list

    def form_valid(self, form):
        item = self.get_object()
        current = item.status
        if current == ListItem.StatusChoices.PENDING:
            form.instance.status = ListItem.StatusChoices.BOUGHT
        elif current == ListItem.StatusChoices.BOUGHT:
            form.instance.status = ListItem.StatusChoices.PENDING
        else:
            form.instance.status = ListItem.StatusChoices.PENDING
        form.instance.updated_by = self.request.user
        form.save()
        return redirect('list_detail', pk=item.list.pk)


class ItemSuggestView(LoginRequiredMixin, CreateView):
    """Return JSON suggestions for frequent products (autocomplete)."""

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        results = []

        if query:
            templates = ProductTemplate.objects.filter(
                Q(name__icontains=query) | Q(normalized_name__icontains=query),
                is_frequent=True,
            )[:10]
            results = [
                {
                    'id': t.id,
                    'name': t.name,
                    'category': t.default_category.name if t.default_category else None,
                    'category_id': t.default_category_id,
                    'unit': t.default_unit,
                }
                for t in templates
            ]

        return JsonResponse({'results': results})
