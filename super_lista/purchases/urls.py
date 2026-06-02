from django.urls import path

from super_lista.purchases.views import (
    PurchaseCreateView,
    PurchaseDetailView,
    PurchaseLineCreateView,
    PurchaseDeleteView,
    ReceiptUploadView,
    ReceiptDeleteView,
)

urlpatterns = [
    # Purchases within a list
    path('<uuid:list_pk>/purchases/create/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('<uuid:list_pk>/purchases/<uuid:pk>/', PurchaseDetailView.as_view(), name='purchase_detail'),
    path('<uuid:list_pk>/purchases/<uuid:pk>/delete/', PurchaseDeleteView.as_view(), name='purchase_delete'),

    # Purchase lines
    path('<uuid:list_pk>/purchases/<uuid:purchase_pk>/lines/add/', PurchaseLineCreateView.as_view(), name='purchase_line_add'),

    # Receipts
    path('<uuid:list_pk>/purchases/<uuid:purchase_pk>/receipt/upload/', ReceiptUploadView.as_view(), name='receipt_upload'),
    path('<uuid:list_pk>/purchases/<uuid:purchase_pk>/receipt/<int:receipt_pk>/delete/', ReceiptDeleteView.as_view(), name='receipt_delete'),
]
