# Superlista — Seguridad

## 1. Objetivos
- Proteger listas compartidas.
- Restringir acceso por rol.
- Evitar exposición de datos financieros.
- Mantener trazabilidad de cambios.

## 2. Autenticación
- Django Auth.
- Contraseñas hasheadas con mecanismos estándar de Django.
- Recuperación por correo.
- Sesiones seguras y expiración razonable.

## 3. Autorización
- Verificación de membrecía en cada lista.
- Control de rol por acción:
  - owner: todo permitido,
  - editor: crear y modificar según reglas,
  - viewer: solo lectura.
- URLs de invitación con token aleatorio, revocable y preferiblemente con expiración.

## 4. Protección de datos
- Uso de HTTPS en ambientes productivos.
- No exponer tokens en logs.
- Sanitización de entradas de texto.
- Validación de archivos subidos para boletas.
- Limitación de tamaño de archivos.

## 5. Auditoría
Registrar:
- creación de lista,
- invitaciones,
- cambios de rol,
- altas, ediciones y borrados de ítems,
- registro de compras,
- carga de boletas,
- cambios de totales y conciliaciones.

## 6. Riesgos
- Un enlace compartido puede ser reenviado fuera del grupo previsto.
- Un colaborador con permisos altos puede alterar información crítica.
- Las boletas pueden contener datos sensibles.
- La edición concurrente puede causar inconsistencias si no se aplican controles.

## 7. Controles recomendados
- Tokens de invitación con expiración.
- Revocación inmediata de acceso.
- Confirmación para acciones destructivas.
- Soft delete para entidades sensibles.
- Registro de actor y timestamp en acciones críticas.
