"""
URL configuration for super_lista project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Home / Dashboard
    path('', include('super_lista.core.urls')),

    # Authentication & Users
    path('accounts/', include('super_lista.users.urls')),

    # Shopping Lists
    path('lists/', include('super_lista.lists.urls')),

    # Items (nested under lists)
    path('items/', include('super_lista.items.urls')),

    # Vendors
    path('vendors/', include('super_lista.vendors.urls')),

    # Purchases
    path('purchases/', include('super_lista.purchases.urls')),

    # Reports
    path('reports/', include('super_lista.reports.urls')),

    # Admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
