from django.contrib import admin

from super_lista.vendors.models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor_type', 'city', 'is_active', 'created_by']
    list_filter = ['vendor_type', 'is_active', 'city']
    search_fields = ['name', 'city', 'address']
    raw_id_fields = ['created_by']
