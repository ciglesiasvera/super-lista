"""
Permissions helpers and mixins for shopping list access control.
"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from super_lista.lists.models import ShoppingList, ListMember


def get_user_role(shopping_list, user):
    """
    Return the user's role in the list ('owner', 'editor', 'viewer') or None.
    """
    if shopping_list.owner == user:
        return ListMember.RoleChoices.OWNER
    try:
        member = ListMember.objects.get(list=shopping_list, user=user)
        return member.role
    except ListMember.DoesNotExist:
        return None


def can_edit(shopping_list, user):
    """Return True if user is owner or editor of the list."""
    role = get_user_role(shopping_list, user)
    return role in (ListMember.RoleChoices.OWNER, ListMember.RoleChoices.EDITOR)


def can_view(shopping_list, user):
    """Return True if user has any role in the list (including owner)."""
    return get_user_role(shopping_list, user) is not None


class ListAccessMixin(UserPassesTestMixin):
    """
    CBV mixin to verify list access.
    Requires the view to have a URL kwarg 'pk' or 'list_pk' that
    resolves to the ShoppingList primary key (UUID).
    Sets self.shopping_list and self.list_role for use in the view.

    Usage:
        class MyView(ListAccessMixin, DetailView):
            # ...

    Override check_access(role) to customize. By default requires any access.
    """

    permission_denied_message = 'No tienes acceso a esta lista.'

    def check_access(self, role):
        """Override in subclass to require specific roles. Default: any access."""
        return role is not None

    def get_shopping_list(self):
        pk = self.kwargs.get('pk') or self.kwargs.get('list_pk')
        return get_object_or_404(ShoppingList, pk=pk)

    def test_func(self):
        self.shopping_list = self.get_shopping_list()
        self.list_role = get_user_role(self.shopping_list, self.request.user)
        return self.check_access(self.list_role)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(self.permission_denied_message)
        return super().handle_no_permission()


class EditorRequiredMixin(ListAccessMixin):
    """Mixin that requires editor or owner role."""

    def check_access(self, role):
        return role in (ListMember.RoleChoices.OWNER, ListMember.RoleChoices.EDITOR)


class OwnerRequiredMixin(ListAccessMixin):
    """Mixin that requires owner role only."""

    def check_access(self, role):
        return role == ListMember.RoleChoices.OWNER
