# design.md

# Diseño Técnico y Arquitectura

## Visión General

Superlista es una aplicación web colaborativa para la gestión de compras familiares, presupuestos domésticos y seguimiento de gastos reales.

La solución se construirá bajo principios de:

* Domain Driven Design (DDD Lite)
* Spec Driven Development (SDD)
* Clean Architecture
* Separation of Concerns
* Mobile First
* API First

---

# Arquitectura General

```text
┌──────────────────────────┐
│      Navegador Web       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Bootstrap 5.3.8 Frontend │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Django Views / DRF APIs  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Domain Services          │
│ Business Rules           │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ MySQL                    │
└──────────────────────────┘
```

---

# Arquitectura de Dominio

## Objetivo

El dominio principal de Superlista consiste en administrar compras domésticas colaborativas, permitiendo que múltiples usuarios construyan listas, registren presupuestos y controlen gastos reales.

---

# Bounded Contexts

Para evitar un modelo monolítico complejo, el dominio se divide en los siguientes contextos.

## 1. Identity & Access

Responsable de:

* Registro de usuarios
* Inicio de sesión
* Roles
* Permisos
* Invitaciones

### Entidades

* User
* Invitation
* Membership

---

## 2. Shopping Lists

Responsable de:

* Creación de listas
* Edición de listas
* Compartición
* Colaboración

### Entidades

* ShoppingList
* ShoppingListMember
* ShoppingListItem

---

## 3. Product Catalog

Responsable de:

* Catálogo reutilizable de productos
* Categorías
* Historial de uso

### Entidades

* Product
* Category

---

## 4. Suppliers

Responsable de:

* Gestión de proveedores
* Supermercados
* Ferias
* Comercios

### Entidades

* Supplier

---

## 5. Purchasing

Responsable de:

* Registro de compras
* Registro de precios
* Comparación de presupuestos

### Entidades

* PurchaseSession
* PurchasedItem
* Receipt

---

## 6. Budget & Analytics

Responsable de:

* Presupuestos
* Reportes
* Historial de precios
* Estadísticas

### Entidades

* BudgetSnapshot
* PriceHistory

---

# Aggregate Roots

Los siguientes Aggregate Roots gobiernan las reglas principales del sistema.

## User

Controla:

* Perfil
* Acceso
* Membresías

---

## ShoppingList

Controla:

* Miembros
* Ítems
* Permisos

Regla:

Una lista siempre tiene exactamente un propietario.

---

## Product

Controla:

* Categorías
* Historial de precios

---

## PurchaseSession

Controla:

* Compra realizada
* Productos comprados
* Comparación con presupuesto

---

# Entidades Principales

## User

```text
User
├── id
├── email
├── password
├── first_name
├── last_name
├── created_at
└── updated_at
```

---

## ShoppingList

```text
ShoppingList
├── id
├── owner_id
├── name
├── description
├── status
├── created_at
└── updated_at
```

Estados:

* ACTIVE
* ARCHIVED
* COMPLETED

---

## ShoppingListItem

```text
ShoppingListItem
├── id
├── list_id
├── product_id
├── quantity
├── unit
├── notes
├── estimated_price
└── purchased
```

---

## Product

```text
Product
├── id
├── name
├── category_id
├── default_unit
└── active
```

---

## Supplier

```text
Supplier
├── id
├── name
├── address
├── notes
└── active
```

---

## PurchaseSession

Representa una salida real de compra.

```text
PurchaseSession
├── id
├── shopping_list_id
├── supplier_id
├── purchased_by
├── estimated_total
├── actual_total
├── receipt_total
├── purchase_date
└── notes
```

---

# Reglas de Negocio

## RB-001

Un usuario debe estar autenticado para acceder a una lista.

---

## RB-002

Solo el propietario puede:

* Compartir listas
* Revocar permisos
* Eliminar listas

---

## RB-003

Un editor puede:

* Agregar productos
* Modificar productos
* Marcar productos comprados

---

## RB-004

Un lector únicamente puede visualizar.

---

## RB-005

Una compra debe asociarse a un proveedor.

---

## RB-006

Todo precio registrado genera historial.

---

## RB-007

El total de una compra se calcula automáticamente.

```text
SUM(
 cantidad × precio_real
)
```

---

## RB-008

La diferencia presupuestaria se calcula automáticamente.

```text
diferencia = total_real - total_estimado
```

---

# Eventos de Dominio

Los Domain Events permiten desacoplar funcionalidades futuras.

## Usuario

* UserRegistered
* UserLoggedIn
* UserInvited

---

## Listas

* ShoppingListCreated
* ShoppingListShared
* ShoppingListArchived

---

## Productos

* ProductAddedToList
* ProductRemovedFromList
* ProductUpdated

---

## Compras

* PurchaseStarted
* PurchaseCompleted
* PurchaseCancelled

---

## Presupuestos

* BudgetGenerated
* BudgetCompared

---

# Visión Event Storming

## Flujo Principal de Negocio

```text
Usuario registra cuenta
        │
        ▼
Usuario crea lista
        │
        ▼
Invita colaboradores
        │
        ▼
Colaboradores agregan productos
        │
        ▼
Se genera presupuesto estimado
        │
        ▼
Usuario realiza compra
        │
        ▼
Registra precios reales
        │
        ▼
Registra total boleta
        │
        ▼
Sistema compara montos
        │
        ▼
Genera historial financiero
```

---

# Event Storming Completo

## Comando

CreateShoppingList

↓

## Evento

ShoppingListCreated

↓

## Política

Asignar propietario

---

## Comando

InviteUser

↓

## Evento

UserInvited

↓

## Política

Enviar invitación

---

## Comando

AddProductToList

↓

## Evento

ProductAddedToList

↓

## Política

Actualizar presupuesto

---

## Comando

UpdateItemQuantity

↓

## Evento

ItemQuantityUpdated

↓

## Política

Recalcular estimación

---

## Comando

RegisterPurchase

↓

## Evento

PurchaseCompleted

↓

## Política

Guardar historial de precios

---

## Comando

RegisterReceiptTotal

↓

## Evento

ReceiptTotalRegistered

↓

## Política

Comparar diferencia

---

## Comando

ArchiveShoppingList

↓

## Evento

ShoppingListArchived

↓

## Política

Bloquear edición

---

# Futuros Eventos

Diseñados para versiones posteriores.

* BarcodeScanned
* PromotionDetected
* PriceDropDetected
* BudgetExceeded
* SharedListModified
* SupplierRecommendationGenerated
* MonthlyBudgetGenerated

---

# Proyección para Microservicios

Aunque la versión inicial será monolítica con Django, la separación del dominio permitirá migrar posteriormente a:

```text
identity-service
shopping-service
catalog-service
supplier-service
purchase-service
analytics-service
```

sin modificar significativamente las reglas de negocio.

---

# Decisiones Arquitectónicas

| Decisión        | Motivo                                  |
| --------------- | --------------------------------------- |
| Django Monolith | Mayor velocidad de desarrollo           |
| MySQL           | Simplicidad y robustez                  |
| Bootstrap       | Menor complejidad frontend              |
| DDD Lite        | Mantener reglas de negocio organizadas  |
| Event Storming  | Facilitar escalabilidad futura          |
| REST API        | Compatibilidad con futuras apps móviles |

---

# Resultado Esperado

Superlista deberá evolucionar desde un MVP de listas compartidas hacia una plataforma integral de planificación financiera familiar basada en compras reales, presupuestos e inteligencia de consumo doméstico.
