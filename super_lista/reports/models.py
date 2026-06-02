"""
Reports models — budget tracking and reporting snapshots.
"""

from django.conf import settings
from django.db import models


class BudgetSnapshot(models.Model):
    """Periodic snapshot of budget vs actual spending for a shopping list."""

    shopping_list = models.ForeignKey(
        "lists.ShoppingList",
        on_delete=models.CASCADE,
        related_name="budget_snapshots",
        verbose_name="lista de compras",
    )
    period_start = models.DateField(verbose_name="inicio del período")
    period_end = models.DateField(verbose_name="fin del período")
    budgeted_amount = models.DecimalField(
        max_digits=12, decimal_places=0, verbose_name="monto presupuestado"
    )
    actual_spent = models.DecimalField(
        max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="gasto real"
    )
    difference = models.DecimalField(
        max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="diferencia"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado en")

    class Meta:
        verbose_name = "instantánea de presupuesto"
        verbose_name_plural = "instantáneas de presupuesto"
        ordering = ["-period_start"]
        indexes = [
            models.Index(fields=["shopping_list", "period_start"]),
        ]

    def __str__(self):
        return f"Presupuesto {self.shopping_list} ({self.period_start} — {self.period_end})"
