import json
import uuid
from django.db import models
from django.conf import settings


class TimeStampedMixin(models.Model):
    """Abstract mixin with created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditEvent(models.Model):
    """Registro de auditoría para cambios importantes."""
    ACTION_CHOICES = [
        ('create', 'Creación'),
        ('update', 'Actualización'),
        ('delete', 'Eliminación'),
        ('share', 'Compartir'),
        ('revoke', 'Revocar'),
        ('invite', 'Invitación'),
        ('purchase', 'Compra'),
        ('upload', 'Carga'),
    ]

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Actor'
    )
    entity_type = models.CharField(max_length=50, verbose_name='Tipo de entidad')
    entity_id = models.CharField(max_length=255, verbose_name='ID de entidad')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='Acción')
    before_data = models.JSONField(null=True, blank=True, verbose_name='Datos anteriores')
    after_data = models.JSONField(null=True, blank=True, verbose_name='Datos posteriores')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')

    class Meta:
        verbose_name = 'Evento de auditoría'
        verbose_name_plural = 'Eventos de auditoría'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['created_at']),
            models.Index(fields=['actor']),
        ]

    def __str__(self):
        return f'{self.get_action_display()} - {self.entity_type}#{self.entity_id}'

    @classmethod
    def log(cls, actor, entity_type, entity_id, action, before=None, after=None):
        """Helper para crear un evento de auditoría."""
        return cls.objects.create(
            actor=actor,
            entity_type=entity_type,
            entity_id=str(entity_id),
            action=action,
            before_data=before,
            after_data=after,
        )
