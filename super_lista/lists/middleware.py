"""
Middleware for list access control.
"""
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from super_lista.lists.models import ShoppingList


class ListAccessMiddleware:
    """
    Middleware that intercepts requests to /lists/<uuid>/ and verifies
    the user is a member of that list before the view processes it.

    This is a lightweight alternative to using mixins on every view.
    It only acts on paths matching /lists/<uuid>/... pattern.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_parts = request.path.strip('/').split('/')
        if len(path_parts) >= 2 and path_parts[0] == 'lists':
            list_uuid = path_parts[1]
            from super_lista.lists.permissions import can_view
            from uuid import UUID
            try:
                UUID(list_uuid)
            except (ValueError, AttributeError):
                pass
            else:
                if request.user.is_authenticated:
                    shopping_list = get_object_or_404(ShoppingList, pk=list_uuid)
                    if not can_view(shopping_list, request.user):
                        raise PermissionDenied('No tienes acceso a esta lista.')
        return self.get_response(request)
