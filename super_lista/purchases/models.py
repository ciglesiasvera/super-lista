"""
Purchases models — Purchase, PurchaseLine, and Receipt.
"""

import uuid

from django.conf import settings
from django.db import models


class Purchase(models.Model):
    """A purchase transaction made at a vendor for a shopping list."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    shopping_list = models.ForeignKey(
        "lists.ShoppingList",
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="lista de compras",
    )
    vendor = models.ForeignKey(
        "vendors.Vendor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchases",
        verbose_name="proveedor",
    )
    purchased_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchases",
        verbose_name="comprado por",
    )
    purchase_date = models.DateTimeField(null=True, blank=True, verbose_name="fecha de compra")
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="subtotal"
    )
    discount_total = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="descuento total"
    )
    tax_total = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="impuesto total"
    )
    total_paid = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="total pagado"
    )
    currency = models.CharField(
        max_length=3, default="CLP", verbose_name="moneda"
    )
    notes = models.TextField(null=True, blank=True, verbose_name="notas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="actualizado en")

    class Meta:
        verbose_name = "compra"
        verbose_name_plural = "compras"
        ordering = ["-purchase_date", "-created_at"]
        indexes = [
            models.Index(fields=["shopping_list", "vendor", "purchase_date"]),
        ]

    def __str__(self):
        return f"Compra {self.id} — {self.shopping_list}"


class PurchaseLine(models.Model):
    """Individual line item within a purchase — mirrors the receipt."""

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="lines",
        verbose_name="compra",
    )
    list_item = models.ForeignKey(
        "items.ListItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchase_lines",
        verbose_name="ítem de lista",
    )
    product_name = models.CharField(max_length=200, verbose_name="nombre del producto")
    quantity = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="cantidad"
    )
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="precio unitario"
    )
    line_total = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="total línea"
    )
    estimated_line_total = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="total estimado"
    )
    difference_amount = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="diferencia"
    )

    class Meta:
        verbose_name = "línea de compra"
        verbose_name_plural = "líneas de compra"
        ordering = ["id"]

    def __str__(self):
        return f"{self.product_name} × {self.quantity} — {self.purchase}"


class Receipt(models.Model):
    """Receipt/ticket associated with a purchase (one-to-one)."""

    purchase = models.OneToOneField(
        Purchase,
        on_delete=models.CASCADE,
        related_name="receipt",
        verbose_name="compra",
    )
    receipt_number = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="número de boleta"
    )
    issued_at = models.DateTimeField(null=True, blank=True, verbose_name="emitido en")
    file = models.FileField(
        upload_to="receipts/", null=True, blank=True, verbose_name="archivo"
    )
    notes = models.TextField(null=True, blank=True, verbose_name="notas")

    class Meta:
        verbose_name = "boleta"
        verbose_name_plural = "boletas"

    def __str__(self):
        return f"Boleta {self.receipt_number or self.id} — {self.purchase}"
