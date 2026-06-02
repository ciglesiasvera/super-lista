"""
Items models — Category, ProductTemplate, and ListItem.
"""

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Product category — hierarchical with optional parent."""

    name = models.CharField(max_length=100, verbose_name="nombre")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="slug")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="categoría padre",
    )
    is_system = models.BooleanField(default=False, verbose_name="es del sistema")
    is_active = models.BooleanField(default=True, verbose_name="activa")

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductTemplate(models.Model):
    """Reusable product template shared across lists."""

    class OwnerScope(models.TextChoices):
        GLOBAL = "global", "Global"
        USER = "user", "Usuario"
        LIST = "list", "Lista"

    name = models.CharField(max_length=200, verbose_name="nombre")
    normalized_name = models.CharField(
        max_length=200, db_index=True, verbose_name="nombre normalizado"
    )
    default_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_templates",
        verbose_name="categoría por defecto",
    )
    default_unit = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="unidad por defecto"
    )
    is_frequent = models.BooleanField(default=False, verbose_name="frecuente")
    owner_scope = models.CharField(
        max_length=20,
        choices=OwnerScope.choices,
        default=OwnerScope.GLOBAL,
        verbose_name="ámbito",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_templates",
        verbose_name="creado por",
    )

    class Meta:
        verbose_name = "plantilla de producto"
        verbose_name_plural = "plantillas de producto"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["normalized_name"]),
        ]

    def __str__(self):
        return self.name


class ListItem(models.Model):
    """An item on a specific shopping list."""

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pendiente"
        BOUGHT = "bought", "Comprado"
        SKIPPED = "skipped", "Saltado"
        UNAVAILABLE = "unavailable", "No disponible"

    list = models.ForeignKey(
        "lists.ShoppingList",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="lista",
    )
    template = models.ForeignKey(
        ProductTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="list_items",
        verbose_name="plantilla",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="list_items",
        verbose_name="categoría",
    )
    name = models.CharField(max_length=200, verbose_name="nombre")
    quantity = models.DecimalField(
        max_digits=10, decimal_places=0, default=1, verbose_name="cantidad"
    )
    unit = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="unidad"
    )
    estimated_price = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="precio estimado"
    )
    actual_price = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="precio real"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="estado",
    )
    notes = models.TextField(null=True, blank=True, verbose_name="notas")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_items",
        verbose_name="creado por",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_items",
        verbose_name="actualizado por",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="actualizado en")

    class Meta:
        verbose_name = "ítem de lista"
        verbose_name_plural = "ítems de lista"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["list", "status", "category"]),
        ]

    def __str__(self):
        return f"{self.name} — {self.list}"
