from django.urls import path

from super_lista.vendors.views import (
    VendorListView,
    VendorCreateView,
    VendorUpdateView,
    VendorDeleteView,
)

urlpatterns = [
    path('', VendorListView.as_view(), name='vendor_list'),
    path('create/', VendorCreateView.as_view(), name='vendor_create'),
    path('<int:pk>/edit/', VendorUpdateView.as_view(), name='vendor_update'),
    path('<int:pk>/delete/', VendorDeleteView.as_view(), name='vendor_delete'),
]
