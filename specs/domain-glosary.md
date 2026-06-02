# domain-glossary.md

# Glosario de Dominio

## Introducción

Este documento define el lenguaje oficial del dominio de negocio de Superlista.

Su propósito es asegurar que:

* Desarrolladores
* Product Owners
* Diseñadores UX/UI
* QA
* Agentes IA
* Usuarios avanzados

utilicen los mismos términos con exactamente el mismo significado.

Toda especificación futura deberá utilizar los conceptos definidos aquí.

---

# Conceptos Fundamentales

## Superlista

Aplicación colaborativa para la gestión de compras domésticas, presupuestos familiares y control de gastos.

---

## Usuario

Persona registrada en la plataforma.

Puede:

* Crear listas
* Compartir listas
* Agregar productos
* Registrar compras
* Consultar reportes

### Atributos principales

* Nombre
* Correo electrónico
* Contraseña
* Fecha de registro

---

## Propietario

Usuario que crea una lista.

Tiene control total sobre ella.

Puede:

* Compartir la lista
* Eliminar la lista
* Cambiar permisos
* Archivar la lista

Cada lista tiene exactamente un propietario.

---

## Colaborador

Usuario invitado a participar en una lista.

Puede tener distintos niveles de acceso.

---

## Invitación

Mecanismo mediante el cual un propietario comparte una lista con otro usuario.

Puede enviarse mediante:

* Correo electrónico
* URL segura
* Token de acceso

---

# Gestión de Listas

## Lista

Conjunto organizado de productos que se desea comprar.

Ejemplos:

* Compra semanal
* Compra mensual
* Compra de feriado largo
* Compra especial

---

## Lista Activa

Lista que puede seguir siendo modificada.

Estado:

```text
ACTIVE
```

---

## Lista Archivada

Lista cerrada para edición.

Conservada únicamente para consulta histórica.

Estado:

```text
ARCHIVED
```

---

## Lista Completada

Lista cuya compra ya fue realizada.

Estado:

```text
COMPLETED
```

---

## Miembro de Lista

Relación entre una lista y un usuario.

Define permisos y acceso.

---

## Permiso

Nivel de acceso otorgado a un miembro.

### Lector

Puede:

* Ver listas
* Ver productos

No puede modificar información.

---

### Editor

Puede:

* Agregar productos
* Editar productos
* Registrar compras

No puede administrar permisos.

---

### Propietario

Control total sobre la lista.

---

# Gestión de Productos

## Producto

Elemento que puede ser comprado.

Ejemplos:

* Leche
* Pan
* Detergente
* Huevos
* Queso

---

## Catálogo de Productos

Repositorio de productos previamente utilizados.

Permite reutilizar productos sin volver a escribirlos.

---

## Producto Recurrente

Producto utilizado frecuentemente en distintas listas.

Puede aparecer automáticamente en sugerencias.

---

## Ítem de Lista

Instancia específica de un producto dentro de una lista.

Ejemplo:

```text
Producto: Leche
Cantidad: 4
```

No debe confundirse con el concepto general de Producto.

---

## Cantidad

Número de unidades requeridas.

Ejemplos:

```text
2
4
10
```

---

## Unidad de Medida

Forma de expresar una cantidad.

Ejemplos:

* Unidad
* Kilogramo
* Gramo
* Litro
* Mililitro
* Paquete
* Caja
* Bandeja

---

## Categoría

Agrupación lógica de productos.

Ejemplos:

* Abarrotes
* Lácteos
* Carnes
* Frutas
* Verduras
* Congelados
* Limpieza
* Higiene Personal
* Mascotas
* Bebidas

---

# Gestión de Proveedores

## Proveedor

Lugar donde se adquieren productos.

Ejemplos:

* Supermercado
* Feria
* Carnicería
* Distribuidora
* Verdulería

---

## Proveedor Habitual

Proveedor utilizado frecuentemente por una familia.

Permite generar estadísticas y comparaciones.

---

## Dirección de Proveedor

Ubicación física donde se realiza la compra.

Puede contener:

* Calle
* Número
* Ciudad
* Observaciones

---

# Gestión de Compras

## Compra

Proceso real de adquisición de productos.

Ocurre cuando un usuario visita un proveedor y compra productos.

---

## Sesión de Compra

Registro de una visita de compra específica.

Ejemplo:

```text
Compra en Líder
03-06-2026
```

Una sesión de compra puede contener múltiples productos.

---

## Comprador

Usuario que realiza físicamente la compra.

---

## Producto Comprado

Registro de un producto efectivamente adquirido.

Incluye:

* Cantidad
* Precio real
* Fecha

---

## Compra Parcial

Situación en la que sólo parte de una lista es comprada.

Ejemplo:

```text
Frutas en la feria
Carnes en carnicería
Abarrotes en supermercado
```

---

## Compra Completa

Situación en la que todos los productos de una lista han sido adquiridos.

---

# Gestión de Precios

## Precio Estimado

Valor proyectado antes de realizar una compra.

Se utiliza para generar presupuestos.

Ejemplo:

```text
Leche = $1.200
```

---

## Precio Real

Valor efectivamente pagado por un producto.

Se registra después de la compra.

Ejemplo:

```text
Leche = $1.350
```

---

## Historial de Precios

Registro cronológico de precios observados para un producto.

Permite:

* Comparar precios
* Detectar aumentos
* Detectar ofertas

---

## Variación de Precio

Diferencia entre dos precios registrados para el mismo producto.

---

# Gestión Presupuestaria

## Presupuesto

Estimación económica de una compra.

Se calcula utilizando precios estimados.

---

## Total Estimado

Suma de todos los precios estimados.

Fórmula:

```text
Σ(cantidad × precio_estimado)
```

---

## Total Real

Suma de todos los precios reales registrados.

Fórmula:

```text
Σ(cantidad × precio_real)
```

---

## Total Boleta

Monto final indicado en el comprobante de compra.

Puede diferir del Total Real por:

* Descuentos
* Promociones
* Redondeos
* Errores de digitación

---

## Diferencia Presupuestaria

Comparación entre presupuesto y gasto real.

Fórmula:

```text
Total Real - Total Estimado
```

---

## Desviación Presupuestaria

Porcentaje de diferencia entre lo estimado y lo gastado.

Fórmula:

```text
((Total Real - Total Estimado)
 / Total Estimado) × 100
```

---

# Historial y Analítica

## Reporte

Visualización de información histórica.

---

## Gasto Mensual

Suma de compras realizadas durante un mes.

---

## Tendencia de Precios

Evolución temporal de precios de un producto.

---

## Categoría Más Costosa

Categoría que concentra el mayor gasto acumulado.

---

## Proveedor Más Utilizado

Proveedor con mayor cantidad de compras registradas.

---

# Seguridad

## Token de Invitación

Identificador único que permite acceder a una invitación.

Debe ser:

* Aleatorio
* Seguro
* Temporal

---

## Sesión

Estado autenticado de un usuario dentro de la aplicación.

---

## Auditoría

Registro histórico de acciones relevantes.

Ejemplos:

* Lista creada
* Producto eliminado
* Usuario invitado
* Compra registrada

---

# Métricas de Negocio

## Ahorro

Monto que se dejó de gastar respecto del presupuesto proyectado.

---

## Sobregasto

Monto adicional gastado respecto del presupuesto proyectado.

---

## Frecuencia de Compra

Número de veces que un producto es adquirido en un período.

---

## Índice de Reutilización

Porcentaje de productos agregados desde el catálogo existente versus productos creados manualmente.

---

# Lenguaje Ubicuo Oficial

Los siguientes términos son los únicos que deben utilizarse en documentación, APIs y código:

| Concepto             | Nombre Oficial     |
| -------------------- | ------------------ |
| Usuario              | User               |
| Lista                | ShoppingList       |
| Miembro              | ShoppingListMember |
| Producto             | Product            |
| Categoría            | Category           |
| Proveedor            | Supplier           |
| Compra               | Purchase           |
| Sesión de Compra     | PurchaseSession    |
| Precio Estimado      | EstimatedPrice     |
| Precio Real          | ActualPrice        |
| Total Estimado       | EstimatedTotal     |
| Total Real           | ActualTotal        |
| Total Boleta         | ReceiptTotal       |
| Presupuesto          | Budget             |
| Historial de Precios | PriceHistory       |

---

# Regla de Gobierno del Dominio

Si existe una discrepancia entre:

* Código
* Base de datos
* Documentación
* Historias de usuario

el significado correcto de un término será siempre el definido en este documento.
