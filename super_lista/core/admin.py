from django.contrib import admin

from super_lista.core.models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ['actor', 'entity_type', 'entity_id', 'action', 'created_at']
    list_filter = ['action', 'entity_type', 'created_at']
    search_fields = ['entity_type', 'entity_id', 'actor__username', 'actor__email']
    readonly_fields = ['actor', 'entity_type', 'entity_id', 'action', 'before_data', 'after_data', 'created_at']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
