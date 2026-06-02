# Superlista — Modelo de datos

## 1. Objetivo del modelo
El modelo debe permitir:
- usuarios y colaboración,
- listas compartidas,
- productos reutilizables,
- categorías,
- proveedores,
- compras,
- boletas,
- registro de precios estimados y reales,
- auditoría de cambios.

## 2. Entidades principales

### 2.1 User
Representa a cada persona registrada.
Campos sugeridos:
- id
- email
- password
- first_name
- last_name
- is_active
- date_joined
- last_login

### 2.2 ShoppingList
Lista principal compartida.
Campos:
- id (UUID)
- owner_id
- name
- description
- frequency_type (`weekly`, `monthly`, `custom`, `one_off`)
- status (`active`, `archived`)
- share_token
- share_token_expires_at
- created_at
- updated_at

### 2.3 ListMember
Relación entre usuario y lista.
Campos:
- id
- list_id
- user_id
- role (`owner`, `editor`, `viewer`)
- invited_by_id
- invitation_status
- invited_at
- accepted_at

### 2.4 Category
Categoría de producto.
Campos:
- id
- name
- slug
- parent_id (opcional)
- is_system
- is_active

### 2.5 ProductTemplate
Plantilla de producto reutilizable.
Campos:
- id
- name
- normalized_name
- default_category_id
- default_unit
- is_frequent
- owner_scope (global, user, list)
- created_by_id

### 2.6 ListItem
Ítem dentro de una lista.
Campos:
- id
- list_id
- template_id (opcional)
- category_id
- name
- quantity
- unit
- estimated_price
- actual_price
- status (`pending`, `bought`, `skipped`, `unavailable`)
- notes
- created_by_id
- updated_by_id
- created_at
- updated_at

### 2.7 Vendor
Proveedor o comercio.
Campos:
- id
- name
- address
- city
- vendor_type (`supermarket`, `fair`, `store`, `other`)
- notes
- created_by_id
- is_active

### 2.8 Purchase
Compra realizada.
Campos:
- id (UUID)
- list_id
- vendor_id
- purchased_by_id
- purchase_date
- subtotal
- discount_total
- tax_total
- total_paid
- currency
- receipt_id (opcional)
- notes
- created_at
- updated_at

### 2.9 PurchaseLine
Detalle de compra por ítem.
Campos:
- id
- purchase_id
- list_item_id (opcional)
- product_name
- quantity
- unit_price
- line_total
- estimated_line_total
- difference_amount

### 2.10 Receipt
Boleta/comprobante.
Campos:
- id
- purchase_id
- receipt_number
- issued_at
- file_path
- raw_text (opcional futuro OCR)
- notes

### 2.11 AuditEvent
Registro de actividad.
Campos:
- id
- actor_id
- entity_type
- entity_id
- action
- before_data
- after_data
- created_at

## 3. Relaciones
- Un `User` puede pertenecer a muchas `ShoppingList` mediante `ListMember`.
- Una `ShoppingList` tiene muchos `ListItem`.
- Un `ListItem` pertenece a una `Category`.
- Un `ListItem` puede apuntar a `ProductTemplate`.
- Una `ShoppingList` puede tener muchas `Purchase`.
- Una `Purchase` tiene muchas `PurchaseLine`.
- Una `Purchase` puede tener una `Receipt`.
- Un `Vendor` puede asociarse a muchas compras.
- Un `AuditEvent` puede registrar acciones sobre cualquier entidad.

## 4. Reglas de integridad
- `owner_id` debe coincidir con un miembro con rol owner.
- `quantity` debe ser mayor que cero.
- `estimated_price`, `actual_price` y `unit_price` no pueden ser negativas.
- `total_paid` debe ser coherente con la suma de líneas menos descuentos.
- No permitir acceso a listas sin miembro válido o token vigente.

## 5. Índices recomendados
- `ShoppingList(owner_id, status)`
- `ListMember(list_id, user_id)`
- `ListItem(list_id, status, category_id)`
- `ProductTemplate(normalized_name)`
- `Vendor(name)`
- `Purchase(list_id, vendor_id, purchase_date)`
- `AuditEvent(entity_type, entity_id, created_at)`

## 6. Normalización
El diseño debe evitar duplicar información de productos frecuentes y a la vez permitir capturar el dato real de compra en cada ocasión.

## 7. Observaciones de modelado
- `ListItem.name` sirve como texto libre para capturas rápidas.
- `ProductTemplate` resuelve el historial y la sugerencia dinámica.
- `PurchaseLine` es la entidad clave para conciliación de boleta.
- `estimated_price` y `actual_price` deben convivir para comparar plan vs realidad.
