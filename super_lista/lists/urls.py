from django.urls import path

from super_lista.items.views import (
    ListItemCreateView,
    ListItemUpdateView,
    ListItemDeleteView,
    ToggleItemStatusView,
)

from super_lista.lists.views import (
    ShoppingListListView,
    ShoppingListDetailView,
    ShoppingListCreateView,
    ShoppingListUpdateView,
    ShoppingListDeleteView,
    ShareListView,
    ShareByTokenView,
    AcceptInvitationView,
    RevokeMemberView,
)

urlpatterns = [
    # CRUD
    path('', ShoppingListListView.as_view(), name='list_list'),
    path('create/', ShoppingListCreateView.as_view(), name='list_create'),
    path('<uuid:pk>/', ShoppingListDetailView.as_view(), name='list_detail'),
    path('<uuid:pk>/edit/', ShoppingListUpdateView.as_view(), name='list_update'),
    path('<uuid:pk>/delete/', ShoppingListDeleteView.as_view(), name='list_delete'),

    # Items nested under list
    path('<uuid:pk>/items/create/', ListItemCreateView.as_view(), name='item_create'),
    path('<uuid:pk>/items/<int:item_pk>/edit/', ListItemUpdateView.as_view(), name='item_update'),
    path('<uuid:pk>/items/<int:item_pk>/delete/', ListItemDeleteView.as_view(), name='item_delete'),
    path('<uuid:pk>/items/<int:item_pk>/toggle/', ToggleItemStatusView.as_view(), name='item_toggle'),

    # Sharing
    path('<uuid:pk>/share/', ShareListView.as_view(), name='list_share'),
    path('<uuid:pk>/share-token/', ShareByTokenView.as_view(), name='list_share_token'),
    path('<uuid:pk>/revoke/<int:member_id>/', RevokeMemberView.as_view(), name='list_revoke_member'),

    # Invitations (no pk needed — token-based)
    path('invitation/<str:token>/', AcceptInvitationView.as_view(), name='accept_invitation'),
]
