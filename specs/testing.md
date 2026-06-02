# Superlista — Estrategia de pruebas

## 1. Objetivos
Validar que la aplicación:
- gestione acceso seguro,
- comparta listas correctamente,
- permita colaboración según permisos,
- calcule precios y diferencias con precisión,
- mantenga integridad de datos.

## 2. Tipos de prueba

### 2.1 Unitarias
- cálculo de totales,
- diferencias entre estimado y real,
- validación de cantidades,
- validación de permisos,
- normalización de nombres de productos.

### 2.2 Integración
- creación de lista y membresías,
- invitación y aceptación,
- creación de ítems con categorías,
- registro de compra y boleta,
- conciliación con varias líneas.

### 2.3 Funcionales / end-to-end
- registro, login y creación de lista,
- compartir lista con otro usuario,
- edición colaborativa,
- consulta de reportes.

### 2.4 Seguridad
- acceso denegado sin membresía,
- acceso solo lectura para viewers,
- revocación de token,
- protección contra edición no autorizada.

## 3. Casos críticos
- Dos usuarios editando el mismo ítem.
- Un ítem repetido que debe sugerirse dinámicamente.
- Compra parcial de una lista en varios proveedores.
- Diferencia entre precio estimado y boleta.
- Eliminación de un miembro con permisos activos.

## 4. Criterios de aceptación
- Un usuario autorizado puede ver la lista.
- Un editor autorizado puede agregar y modificar ítems.
- Un viewer no puede editar.
- El total real se calcula correctamente con líneas de compra.
- La boleta puede asociarse a una compra específica.
- Los reportes muestran totales consistentes.

## 5. Datos de prueba
- Usuarios: owner, editor, viewer.
- Lista semanal y lista mensual.
- Categorías base.
- Proveedores tipo supermercado y feria.
- Ítems frecuentes con repetición.
- Compra con descuento y con diferencia de precio.

## 6. Automatización
Se recomienda iniciar con:
- pytest para lógica de negocio,
- tests de Django para vistas y permisos,
- factories para datos,
- cobertura mínima en servicios de cálculo y autorización.
