from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Q
from django.views.generic import TemplateView, ListView

from super_lista.lists.models import ShoppingList
from super_lista.lists.permissions import ListAccessMixin
from super_lista.purchases.models import Purchase, PurchaseLine
from super_lista.reports.models import BudgetSnapshot


class DashboardView(LoginRequiredMixin, TemplateView):
    """Global dashboard: totals, differences across all user lists."""
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        user_lists = ShoppingList.objects.filter(
            Q(owner=user) | Q(members__user=user)
        ).distinct()

        total_budgeted = Decimal('0')
        total_spent = Decimal('0')
        total_difference = Decimal('0')
        list_stats = []

        for lst in user_lists:
            budget_qs = BudgetSnapshot.objects.filter(shopping_list=lst)
            budget = budget_qs.aggregate(
                total_budget=Sum('budgeted_amount'),
                total_actual=Sum('actual_spent'),
            )
            b = budget['total_budget'] or Decimal('0')
            a = budget['total_actual'] or Decimal('0')
            diff = b - a

            purchases = Purchase.objects.filter(shopping_list=lst)
            total_purchases = purchases.aggregate(total=Sum('total_paid'))['total'] or Decimal('0')

            list_stats.append({
                'list': lst,
                'budgeted': b,
                'actual': a,
                'difference': diff,
                'purchases_total': total_purchases,
                'purchase_count': purchases.count(),
            })

            total_budgeted += b
            total_spent += a
            total_difference += diff

        context.update({
            'list_stats': list_stats,
            'total_budgeted': total_budgeted,
            'total_spent': total_spent,
            'total_difference': total_difference,
            'list_count': user_lists.count(),
        })
        return context


class ListSummaryView(ListAccessMixin, TemplateView):
    """Per-list financial summary."""
    template_name = 'reports/list_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.shopping_list

        purchases = Purchase.objects.filter(shopping_list=shopping_list)
        total_purchases = purchases.aggregate(total=Sum('total_paid'))['total'] or Decimal('0')

        lines = PurchaseLine.objects.filter(purchase__shopping_list=shopping_list)
        total_items = lines.aggregate(total=Sum('line_total'))['total'] or Decimal('0')
        total_diff = lines.aggregate(total=Sum('difference_amount'))['total'] or Decimal('0')

        vendor_breakdown = purchases.values('vendor__name').annotate(
            total=Sum('total_paid'),
            count=Count('id'),
        ).order_by('-total')

        snapshots = BudgetSnapshot.objects.filter(shopping_list=shopping_list)[:12]

        context.update({
            'list_obj': shopping_list,
            'total_purchases': total_purchases,
            'total_items': total_items,
            'total_diff': total_diff,
            'purchase_count': purchases.count(),
            'vendor_breakdown': vendor_breakdown,
            'snapshots': snapshots,
        })
        return context


class VendorSummaryView(LoginRequiredMixin, TemplateView):
    """Per-vendor spending summary."""
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        user_lists = ShoppingList.objects.filter(
            Q(owner=user) | Q(members__user=user)
        ).distinct()

        vendor_data = (
            Purchase.objects
            .filter(shopping_list__in=user_lists)
            .values('vendor__name', 'vendor__id')
            .annotate(
                total=Sum('total_paid'),
                count=Count('id'),
            )
            .exclude(vendor__isnull=True)
            .order_by('-total')
        )

        context.update({
            'vendor_data': vendor_data,
            'vendors_section': True,
        })
        return context


class PriceHistoryView(ListAccessMixin, ListView):
    """Show price history for items in a list."""
    template_name = 'reports/history.html'
    context_object_name = 'lines'

    def get_queryset(self):
        shopping_list = self.shopping_list
        return (
            PurchaseLine.objects
            .filter(purchase__shopping_list=shopping_list)
            .select_related('purchase', 'list_item')
            .order_by('-purchase__purchase_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_obj'] = self.shopping_list
        return context
