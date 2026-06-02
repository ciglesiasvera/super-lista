from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from super_lista.lists.models import ShoppingList


class DashboardView(LoginRequiredMixin, TemplateView):
    """Home/dashboard showing user's shopping list summary."""
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        owned_lists = ShoppingList.objects.filter(owner=user, status='active')
        shared_lists = ShoppingList.objects.filter(
            members__user=user,
            status='active',
        ).exclude(owner=user)

        context.update({
            'owned_lists': owned_lists,
            'shared_lists': shared_lists,
            'owned_count': owned_lists.count(),
            'shared_count': shared_lists.count(),
            'total_active': owned_lists.count() + shared_lists.count(),
        })
        return context
