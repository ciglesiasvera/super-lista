"""
Vendors model — stores/storefront information.
"""

from django.conf import settings
from django.db import models


class Vendor(models.Model):
    """A store, supermarket, or market where purchases are made."""

    class VendorType(models.TextChoices):
        SUPERMARKET = "supermarket", "Supermercado"
        FAIR = "fair", "Feria"
        STORE = "store", "Tienda"
        OTHER = "other", "Otro"

    name = models.CharField(max_length=200, verbose_name="nombre")
    address = models.TextField(null=True, blank=True, verbose_name="dirección")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="ciudad")
    vendor_type = models.CharField(
        max_length=20,
        choices=VendorType.choices,
        default=VendorType.OTHER,
        verbose_name="tipo",
    )
    notes = models.TextField(null=True, blank=True, verbose_name="notas")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendors",
        verbose_name="creado por",
    )
    is_active = models.BooleanField(default=True, verbose_name="activo")

    class Meta:
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name
