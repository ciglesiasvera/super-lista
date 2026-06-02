# Superlista — Requerimientos

## 1. Propósito
Superlista es una aplicación web para planificar, compartir y administrar listas de compra del hogar con colaboración en tiempo real o casi en tiempo real, control de permisos, categorización de productos, proveedores, presupuesto y conciliación de precios con boletas.

## 2. Problema que resuelve
Los hogares compran en múltiples lugares y con frecuencia necesitan:
- coordinar compras entre varias personas,
- reutilizar productos frecuentes,
- registrar precios reales pagados,
- controlar presupuestos,
- comparar lo planificado con lo efectivamente cobrado.

## 3. Alcance funcional

### 3.1 Gestión de cuentas
- Registro de usuario por correo electrónico y contraseña.
- Inicio de sesión y cierre de sesión.
- Recuperación de contraseña.
- Perfil básico de usuario.

### 3.2 Gestión de listas
- Crear una lista de compra.
- Definir periodicidad u objetivo de la lista: mensual, semanal, evento puntual o libre.
- Renombrar, archivar y eliminar listas.
- Compartir una lista mediante URL segura y por invitación a correo electrónico.
- Ver listas compartidas según permisos.

### 3.3 Colaboración y permisos
- Invitar usuarios por correo.
- Asignar permisos por lista:
  - solo lectura,
  - edición,
  - administración parcial o total.
- El dueño de la lista define quién puede ver y quién puede editar.
- Registrar quién agregó o editó cada ítem.

### 3.4 Gestión de ítems
- Crear ítems indicando nombre, cantidad y categoría.
- Categorías mínimas:
  - limpieza,
  - alimentos,
  - congelados,
  - frutas,
  - verduras.
- Permitir agregar categorías personalizadas.
- Sugerir ítems repetidos mediante un selector dinámico/autocompletado.
- Permitir marcar ítems como pendientes, comprados, omitidos o no disponibles.
- Permitir registrar notas por ítem.

### 3.5 Proveedores y comercios
- Registrar supermercados, ferias, almacenes u otros proveedores.
- Guardar nombre, dirección, tipo de proveedor y observaciones.
- Asociar productos frecuentes a uno o más proveedores.
- Permitir comparar compras por proveedor.

### 3.6 Precios y boletas
- Registrar precio estimado por ítem.
- Registrar precio efectivo al momento de compra.
- Registrar cantidad efectivamente comprada.
- Registrar boleta o comprobante asociado a la compra.
- Calcular diferencia entre estimado y cobrado.
- Detectar posibles descuentos, sobrecargos o diferencias de redondeo.

### 3.7 Presupuesto y control financiero
- Calcular total estimado de una lista.
- Calcular total real de una compra.
- Mostrar diferencias por lista, por proveedor y por período.
- Entregar resumen para presupuesto familiar.
- Filtrar historial por fechas, categorías y proveedores.

## 4. Alcance no funcional
- La aplicación debe ser responsive.
- Debe ser usable en desktop y móvil.
- Debe soportar múltiples usuarios concurrentes.
- Debe mantener integridad de permisos y datos.
- Debe registrar auditoría de cambios relevantes.
- Debe ser fácil de extender con nuevas categorías y proveedores.

## 5. Roles
### 5.1 Propietario de lista
Crea la lista, administra permisos y conserva control total.

### 5.2 Colaborador editor
Puede agregar, modificar y marcar ítems según el permiso otorgado.

### 5.3 Colaborador lector
Puede ver la lista, pero no editarla.

## 6. Reglas de negocio
- Un usuario solo accede a una lista si fue invitado, tiene URL válida o fue autorizado explícitamente.
- El dueño de la lista puede revocar permisos en cualquier momento.
- Un ítem puede pertenecer a una categoría principal y opcionalmente a una subcategoría.
- El precio efectivo puede ser distinto del estimado.
- Una misma lista puede tener varios proveedores asociados.
- Un mismo producto frecuente puede aparecer varias veces en diferentes listas.
- El selector dinámico debe priorizar coincidencias con el historial del usuario y de la lista.
- La boleta registrada debe quedar vinculada a una compra y no solo al ítem individual.

## 7. Suposiciones
- El producto se construirá como aplicación web.
- La colaboración puede implementarse inicialmente con refresco manual o polling; tiempo real queda como mejora.
- La autenticación será basada en Django.
- MySQL será la base de datos principal.

## 8. Fuera de alcance inicial
- Aplicación móvil nativa.
- Integración bancaria automática.
- OCR de boletas, salvo futura extensión.
- Sincronización con marketplaces externos.
- Motor avanzado de recomendaciones con IA, salvo evolución posterior.

## 9. Criterios de éxito
- Una persona puede crear una lista y compartirla en menos de 2 minutos.
- Varios usuarios pueden colaborar sin pérdida de datos.
- El usuario puede ver el total estimado y el total real con diferencias.
- El sistema permite llevar control histórico de gastos por proveedor y categoría.
