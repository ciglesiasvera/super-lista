from django.urls import path

from super_lista.reports.views import (
    DashboardView,
    ListSummaryView,
    VendorSummaryView,
    PriceHistoryView,
)

urlpatterns = [
    # Global dashboard (reports overview)
    path('', DashboardView.as_view(), name='reports_dashboard'),

    # Per-list reports
    path('lists/<uuid:pk>/summary/', ListSummaryView.as_view(), name='report_list_summary'),
    path('lists/<uuid:pk>/history/', PriceHistoryView.as_view(), name='report_price_history'),

    # Vendor summary
    path('vendors/', VendorSummaryView.as_view(), name='report_vendor_summary'),
]
