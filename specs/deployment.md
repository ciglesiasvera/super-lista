# Superlista — Despliegue y operación

## 1. Entorno local
### Requisitos
- Python 3.12.12
- MySQL 8+
- Node no es requerido para el MVP si se usa Bootstrap servido por CDN o estático.
- Git

### Variables de entorno sugeridas
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL` o credenciales MySQL
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

## 2. Configuración de base de datos
- Crear base de datos MySQL para desarrollo.
- Definir usuario con privilegios limitados.
- Aplicar migraciones de Django.
- Cargar datos iniciales de categorías y roles.

## 3. Arranque local
- instalar dependencias,
- migrar,
- crear superusuario,
- ejecutar servidor de desarrollo.

## 4. Despliegue productivo
### Recomendado
- Gunicorn o equivalente WSGI.
- Nginx como proxy inverso.
- HTTPS obligatorio.
- Archivos estáticos servidos por Nginx o storage externo.
- Backups periódicos de MySQL.

## 5. Observabilidad
- Logging estructurado.
- Registro de errores de aplicación.
- Monitoreo básico de salud.
- Alertas sobre fallos de correo o base de datos.

## 6. Operación
- Política de backup y restauración.
- Rotación de secretos.
- Revisión periódica de permisos.
- Limpieza de tokens expirados.
- Archivado de listas inactivas.

## 7. Evolución
- Agregar CI/CD en GitHub Actions.
- Separar settings por ambiente.
- Incorporar tests automáticos en cada PR.
