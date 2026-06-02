from django.contrib import admin

from super_lista.purchases.models import Purchase, PurchaseLine, Receipt


class PurchaseLineInline(admin.TabularInline):
    model = PurchaseLine
    extra = 0
    readonly_fields = ['line_total', 'estimated_line_total', 'difference_amount']
    raw_id_fields = ['list_item']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'shopping_list', 'vendor', 'purchased_by', 'purchase_date', 'subtotal', 'total_paid', 'currency']
    list_filter = ['purchase_date', 'currency', 'vendor']
    search_fields = ['shopping_list__name', 'vendor__name', 'notes']
    raw_id_fields = ['shopping_list', 'vendor', 'purchased_by']
    readonly_fields = ['subtotal', 'total_paid', 'created_at', 'updated_at']
    inlines = [PurchaseLineInline]
    date_hierarchy = 'purchase_date'


@admin.register(PurchaseLine)
class PurchaseLineAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'purchase', 'quantity', 'unit_price', 'line_total', 'list_item']
    list_filter = ['purchase__purchase_date']
    search_fields = ['product_name']
    raw_id_fields = ['purchase', 'list_item']
    readonly_fields = ['line_total', 'estimated_line_total', 'difference_amount']


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'receipt_number', 'issued_at']
    search_fields = ['receipt_number', 'purchase__shopping_list__name']
    raw_id_fields = ['purchase']
