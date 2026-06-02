from django.contrib import admin

from super_lista.items.models import Category, ProductTemplate, ListItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_system', 'is_active']
    list_filter = ['is_system', 'is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}


@admin.register(ProductTemplate)
class ProductTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'normalized_name', 'default_category', 'default_unit', 'is_frequent', 'owner_scope', 'created_by']
    list_filter = ['is_frequent', 'owner_scope', 'default_category']
    search_fields = ['name', 'normalized_name']
    raw_id_fields = ['created_by']


@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'list', 'category', 'quantity', 'unit', 'status', 'estimated_price', 'actual_price', 'created_by']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['name', 'list__name']
    raw_id_fields = ['list', 'template', 'category', 'created_by', 'updated_by']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
