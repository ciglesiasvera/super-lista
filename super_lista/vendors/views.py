from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from super_lista.vendors.forms import VendorForm
from super_lista.vendors.models import Vendor


class VendorListView(LoginRequiredMixin, ListView):
    """List all vendors for the current user."""
    model = Vendor
    template_name = 'vendors/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 20

    def get_queryset(self):
        return Vendor.objects.filter(
            created_by=self.request.user,
            is_active=True,
        ).order_by('name')


class VendorCreateView(LoginRequiredMixin, CreateView):
    """Create a new vendor."""
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'
    success_url = reverse_lazy('vendor_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Proveedor "{form.instance.name}" creado.')
        return response


class VendorUpdateView(LoginRequiredMixin, UpdateView):
    """Edit a vendor."""
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'
    success_url = reverse_lazy('vendor_list')

    def get_queryset(self):
        return Vendor.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Proveedor actualizado.')
        return response


class VendorDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a vendor (soft-delete by setting is_active=False)."""
    model = Vendor
    template_name = 'vendors/vendor_confirm_delete.html'
    success_url = reverse_lazy('vendor_list')

    def get_queryset(self):
        return Vendor.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        vendor = self.get_object()
        vendor.is_active = False
        vendor.save(update_fields=['is_active'])
        messages.success(self.request, f'Proveedor "{vendor.name}" eliminado.')
        return super().form_valid(form)
