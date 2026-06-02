"""
Users models — profile extending Django's built-in User.
"""

from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extended user profile linked one-to-one to auth.User."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="usuario",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name="avatar",
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="teléfono",
    )
    preferred_currency = models.CharField(
        max_length=3,
        default="CLP",
        verbose_name="moneda preferida",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="actualizado en")

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"
