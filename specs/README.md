# Superlista — Spec-Driven Development

Este directorio reúne las especificaciones técnicas y funcionales para desarrollar **Superlista**, una aplicación web colaborativa para gestionar listas de compra del hogar, presupuesto familiar, control de proveedores y conciliación de boletas.

## Stack objetivo
- Python 3.12.12
- Django
- MySQL
- Bootstrap 5.3.8

## Documentos
- `requirements.md`: alcance, requisitos funcionales y no funcionales.
- `design.md`: arquitectura, módulos, permisos, UX y decisiones de diseño.
- `data-model.md`: modelo de datos y esquema relacional propuesto.
- `api-spec.md`: contratos de alto nivel para vistas/endpoints.
- `security.md`: autenticación, autorización, auditoría y privacidad.
- `testing.md`: estrategia de pruebas y criterios de aceptación.
- `tasks.md`: desglose en épicas, historias y tareas.
- `deployment.md`: entorno local, variables, despliegue y operación.
- `roadmap.md`: entregas por fases recomendadas.

## Objetivo del producto
Permitir que una persona cree una lista de compra compartida, invite a otros usuarios por correo o URL, controle permisos de visualización/edición, asigne ítems a categorías y proveedores, registre precios reales y boletas, y calcule diferencias entre precio estimado y precio cobrado.
