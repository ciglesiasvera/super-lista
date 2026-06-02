"""
Lists models — ShoppingList, ListMember, and Invitation.
"""

import uuid

from django.conf import settings
from django.db import models


class ShoppingList(models.Model):
    """A collaborative shopping list owned by a user and optionally shared."""

    class FrequencyChoices(models.TextChoices):
        WEEKLY = "weekly", "Semanal"
        MONTHLY = "monthly", "Mensual"
        CUSTOM = "custom", "Personalizado"
        ONE_OFF = "one_off", "Una vez"

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Activa"
        ARCHIVED = "archived", "Archivada"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_lists",
        verbose_name="propietario",
    )
    name = models.CharField(max_length=200, verbose_name="nombre")
    description = models.TextField(null=True, blank=True, verbose_name="descripción")
    frequency_type = models.CharField(
        max_length=20,
        choices=FrequencyChoices.choices,
        default=FrequencyChoices.WEEKLY,
        verbose_name="tipo de frecuencia",
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        verbose_name="estado",
    )
    share_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=True,
        blank=True,
        verbose_name="token de compartición",
    )
    share_token_expires_at = models.DateTimeField(
        null=True, blank=True, verbose_name="expiración del token"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="actualizado en")

    class Meta:
        verbose_name = "lista de compras"
        verbose_name_plural = "listas de compras"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status"]),
        ]

    def __str__(self):
        return self.name


class ListMember(models.Model):
    """Membership linking a user to a shared shopping list."""

    class RoleChoices(models.TextChoices):
        OWNER = "owner", "Propietario"
        EDITOR = "editor", "Editor"
        VIEWER = "viewer", "Espectador"

    list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="lista",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="list_memberships",
        verbose_name="usuario",
    )
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.VIEWER,
        verbose_name="rol",
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_invitations",
        verbose_name="invitado por",
    )
    invited_at = models.DateTimeField(auto_now_add=True, verbose_name="invitado en")
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name="aceptado en")

    class Meta:
        verbose_name = "miembro de lista"
        verbose_name_plural = "miembros de lista"
        unique_together = [("list", "user")]
        indexes = [
            models.Index(fields=["list", "user"]),
        ]

    def __str__(self):
        return f"{self.user} — {self.list} ({self.role})"


class Invitation(models.Model):
    """Pending invitation to join a shopping list via email."""

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pendiente"
        ACCEPTED = "accepted", "Aceptada"
        EXPIRED = "expired", "Expirada"
        CANCELLED = "cancelled", "Cancelada"

    class RoleChoices(models.TextChoices):
        EDITOR = "editor", "Editor"
        VIEWER = "viewer", "Espectador"

    list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name="invitations",
        verbose_name="lista",
    )
    email = models.EmailField(max_length=254, verbose_name="correo electrónico")
    token = models.CharField(max_length=255, unique=True, verbose_name="token")
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.VIEWER,
        verbose_name="rol",
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_invitations",
        verbose_name="invitado por",
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="estado",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado en")
    expires_at = models.DateTimeField(verbose_name="expira en")

    class Meta:
        verbose_name = "invitación"
        verbose_name_plural = "invitaciones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Invitación para {self.email} → {self.list}"
