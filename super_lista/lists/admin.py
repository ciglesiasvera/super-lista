from django.contrib import admin

from super_lista.lists.models import ShoppingList, ListMember, Invitation


class ListMemberInline(admin.TabularInline):
    model = ListMember
    extra = 0
    raw_id_fields = ['user']
    readonly_fields = ['invited_by', 'invited_at', 'accepted_at']


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 0
    readonly_fields = ['token', 'invited_by', 'created_at', 'expires_at']
    raw_id_fields = []


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'frequency_type', 'status', 'created_at']
    list_filter = ['frequency_type', 'status', 'created_at']
    search_fields = ['name', 'owner__username', 'owner__email']
    readonly_fields = ['id', 'share_token', 'share_token_expires_at', 'created_at', 'updated_at']
    inlines = [ListMemberInline, InvitationInline]
    date_hierarchy = 'created_at'


@admin.register(ListMember)
class ListMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'list', 'role', 'invited_by', 'accepted_at']
    list_filter = ['role', 'invited_at']
    search_fields = ['user__username', 'list__name']
    raw_id_fields = ['user', 'list', 'invited_by']
    readonly_fields = ['invited_at', 'accepted_at']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'list', 'role', 'status', 'invited_by', 'created_at', 'expires_at']
    list_filter = ['status', 'role', 'created_at']
    search_fields = ['email', 'list__name']
    readonly_fields = ['token', 'invited_by', 'created_at']
    raw_id_fields = ['list']
