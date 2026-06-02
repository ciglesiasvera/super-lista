from django.contrib import admin

from super_lista.reports.models import BudgetSnapshot


@admin.register(BudgetSnapshot)
class BudgetSnapshotAdmin(admin.ModelAdmin):
    list_display = ['shopping_list', 'period_start', 'period_end', 'budgeted_amount', 'actual_spent', 'difference']
    list_filter = ['period_start', 'period_end']
    search_fields = ['shopping_list__name']
    raw_id_fields = ['shopping_list']
    date_hierarchy = 'period_start'
