# Superlista — Especificación de interfaz

## 1. Convención
La aplicación puede iniciar con vistas servidor-rendered de Django. Este documento describe endpoints lógicos y operaciones esperadas, aunque la implementación inicial sea por templates.

## 2. Autenticación
### 2.1 Registro
- `GET /accounts/register/`
- `POST /accounts/register/`

### 2.2 Login
- `GET /accounts/login/`
- `POST /accounts/login/`

### 2.3 Logout
- `POST /accounts/logout/`

### 2.4 Recuperación de contraseña
- `GET /accounts/password-reset/`
- `POST /accounts/password-reset/`

## 3. Listas
### 3.1 Crear lista
- `GET /lists/new/`
- `POST /lists/new/`

### 3.2 Detalle de lista
- `GET /lists/{list_id}/`

### 3.3 Editar lista
- `GET /lists/{list_id}/edit/`
- `POST /lists/{list_id}/edit/`

### 3.4 Archivar / restaurar
- `POST /lists/{list_id}/archive/`
- `POST /lists/{list_id}/restore/`

### 3.5 Compartir lista
- `POST /lists/{list_id}/share/invite/`
- `POST /lists/{list_id}/share/token/`
- `POST /lists/{list_id}/share/revoke/`

## 4. Miembros y permisos
- `GET /lists/{list_id}/members/`
- `POST /lists/{list_id}/members/`
- `POST /lists/{list_id}/members/{member_id}/role/`
- `POST /lists/{list_id}/members/{member_id}/remove/`

## 5. Ítems
- `POST /lists/{list_id}/items/`
- `POST /lists/{list_id}/items/{item_id}/edit/`
- `POST /lists/{list_id}/items/{item_id}/delete/`
- `POST /lists/{list_id}/items/{item_id}/toggle-status/`
- `GET /items/suggest/?q=...`

### Respuesta esperada de sugerencias
- coincidencia por nombre,
- coincidencia por historial del usuario,
- coincidencia por historial de lista,
- coincidencia por categoría.

## 6. Proveedores
- `GET /vendors/`
- `GET /vendors/new/`
- `POST /vendors/new/`
- `GET /vendors/{vendor_id}/edit/`
- `POST /vendors/{vendor_id}/edit/`

## 7. Compras
- `GET /lists/{list_id}/purchases/new/`
- `POST /lists/{list_id}/purchases/new/`
- `GET /purchases/{purchase_id}/`
- `POST /purchases/{purchase_id}/add-line/`
- `POST /purchases/{purchase_id}/finalize/`

## 8. Boletas
- `POST /purchases/{purchase_id}/receipt/upload/`
- `GET /purchases/{purchase_id}/receipt/`
- `POST /purchases/{purchase_id}/receipt/remove/`

## 9. Reportes
- `GET /reports/dashboard/`
- `GET /reports/lists/{list_id}/summary/`
- `GET /reports/vendors/{vendor_id}/summary/`
- `GET /reports/history/`

## 10. Respuestas y errores
### Éxito
- `200` para vistas y lectura.
- `201` para creación.
- `204` para eliminación lógica o acción sin cuerpo.

### Errores
- `400` validación.
- `401` no autenticado.
- `403` sin permiso.
- `404` no encontrado.
- `409` conflicto por edición concurrente o datos duplicados.

## 11. Cargas útiles esperadas
### Crear ítem
- `name`
- `quantity`
- `unit`
- `category_id`
- `estimated_price`
- `template_id` opcional
- `notes`

### Registrar compra
- `vendor_id`
- `purchase_date`
- `discount_total`
- `tax_total`
- `notes`

### Registrar línea
- `product_name`
- `quantity`
- `unit_price`
- `estimated_line_total`
- `list_item_id` opcional

## 12. Validaciones clave
- El usuario debe tener permiso sobre la lista.
- El nombre del producto no debe quedar vacío.
- La cantidad debe ser mayor a cero.
- El precio no debe ser negativo.
- La suma de líneas debe cuadrar con el total o justificar diferencia.
