from django.urls import path
from django.contrib.auth.decorators import login_required

from super_lista.core.views import DashboardView

urlpatterns = [
    path('', login_required(DashboardView.as_view()), name='dashboard'),
]
