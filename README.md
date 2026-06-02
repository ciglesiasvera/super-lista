# Superlista

**Superlista** es una aplicación web colaborativa para la gestión inteligente de listas de compras familiares, diseñada para facilitar la planificación, presupuesto, seguimiento de gastos y organización de compras en múltiples establecimientos.

La plataforma permite que una familia o grupo de personas construya listas compartidas, gestione permisos de acceso, registre precios reales de compra y compare presupuestos con los montos efectivamente pagados, proporcionando una visión más precisa de los gastos domésticos.

## URL de Producción

**Producción:** https://superlista.skylabs.cl

---

# Objetivo

Permitir que múltiples usuarios colaboren en la construcción y mantenimiento de listas de compras para el hogar, registrando productos, cantidades, categorías, proveedores habituales y precios reales, con el fin de:

* Organizar compras familiares.
* Mejorar la planificación financiera.
* Controlar gastos mensuales.
* Comparar presupuestos versus gastos reales.
* Mantener un historial de precios.
* Facilitar compras colaborativas.

---

# Características Principales

## Gestión de Usuarios

* Registro de usuarios.
* Inicio y cierre de sesión.
* Recuperación de contraseña.
* Gestión de perfil.

## Listas Compartidas

* Creación de listas de compras.
* Compartir listas mediante invitaciones.
* Gestión de permisos:

  * Propietario
  * Editor
  * Lector

## Gestión de Productos

* Agregar productos a una lista.
* Especificar:

  * Nombre
  * Cantidad
  * Unidad de medida
  * Categoría
  * Observaciones

## Catálogo Inteligente

Cuando un producto haya sido utilizado previamente:

* Aparece en sugerencias automáticas.
* Puede seleccionarse desde un listado dinámico.
* Se reutilizan categorías y configuraciones anteriores.

## Categorías de Productos

Ejemplos:

* Abarrotes
* Lácteos
* Carnes
* Congelados
* Frutas
* Verduras
* Limpieza
* Higiene Personal
* Mascotas
* Bebidas
* Otros

Las categorías son administrables por el usuario.

## Gestión de Proveedores

Permite registrar:

* Supermercados
* Ferias
* Carnicerías
* Queserías
* Distribuidoras
* Otros comercios

Cada proveedor almacena:

* Nombre
* Dirección
* Observaciones

## Presupuestos

Antes de realizar una compra el usuario puede:

* Estimar precios por producto.
* Visualizar subtotales.
* Obtener un presupuesto total.

## Registro de Compra Real

Una vez realizada la compra:

* Registrar precio real por producto.
* Registrar cantidad comprada.
* Registrar establecimiento de compra.

## Control de Diferencias

Permite comparar:

* Presupuesto estimado.
* Monto real pagado.
* Diferencia absoluta.
* Diferencia porcentual.

## Historial de Precios

Almacena:

* Precio histórico por producto.
* Fecha de compra.
* Establecimiento.
* Variaciones de precio.

---

# Casos de Uso Principales

### Como propietario

Quiero crear una lista compartida para que mi familia pueda colaborar agregando productos.

### Como colaborador

Quiero agregar productos a una lista para ayudar a preparar la compra.

### Como comprador

Quiero registrar precios reales para controlar cuánto gasté.

### Como administrador del hogar

Quiero comparar presupuestos con gastos reales para mejorar la planificación financiera.

### Como usuario frecuente

Quiero reutilizar productos ya registrados para ahorrar tiempo.

---

# Stack Tecnológico

## Backend

* Python 3.12.12
* Django 5.x
* Django REST Framework
* MySQL 8.x

## Frontend

* HTML5
* CSS3
* Bootstrap 5.3.8
* JavaScript ES2023

## Autenticación

* Django Authentication
* Django Permissions
* Tokens de invitación

## Infraestructura

* Linux
* Nginx
* Gunicorn
* SSL/TLS
* Docker (opcional)

## Control de Versiones

* Git
* GitHub

---

# Arquitectura

La aplicación sigue una arquitectura MVC/MVT basada en Django:

```text
Cliente Web
     │
     ▼
Bootstrap UI
     │
     ▼
Django Views / API
     │
     ▼
Servicios de Negocio
     │
     ▼
MySQL
```

---

# Módulos del Sistema

## 1. Autenticación

* Registro
* Login
* Logout
* Recuperación de contraseña

## 2. Gestión de Usuarios

* Perfil
* Preferencias

## 3. Gestión de Listas

* Crear
* Editar
* Compartir
* Archivar

## 4. Gestión de Productos

* Catálogo personal
* Categorías
* Cantidades

## 5. Gestión de Proveedores

* Crear proveedores
* Asociar precios

## 6. Presupuestos

* Estimación
* Comparación

## 7. Historial y Reportes

* Gastos mensuales
* Evolución de precios
* Diferencias entre presupuesto y gasto real

---

# Principios de Diseño

* Mobile First
* Responsive Design
* Simplicidad de uso
* Colaboración en tiempo real
* Seguridad por defecto
* Escalabilidad futura

---

# Roadmap

## MVP v1.0

* Registro de usuarios
* Gestión de listas
* Productos
* Categorías
* Compartir listas
* Presupuestos
* Registro de compra real

## v1.1

* Historial de precios
* Reportes básicos

## v1.2

* Dashboard financiero

## v2.0

* Aplicación móvil
* Notificaciones push
* Escaneo de códigos de barras
* Sincronización avanzada

---

# Licencia

Copyright © Skylabs

Todos los derechos reservados.

---

# Autor

**Skylabs**
https://superlista.skylabs.cl
