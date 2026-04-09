# Guía de Despliegue en Railway

## Pasos para Desplegar tu Aplicación en Railway

### 1. Preparar tu Repositorio Git

Primero, asegúrate de que tu proyecto esté en un repositorio Git:

```bash
# Si no has inicializado git
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparar proyecto para Railway"
```

### 2. Crear Cuenta en Railway

1. Ve a [railway.app](https://railway.app)
2. Haz clic en "Start a New Project"
3. Inicia sesión con GitHub

### 3. Crear Nuevo Proyecto

1. En Railway, haz clic en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Autoriza Railway para acceder a tus repositorios
4. Selecciona tu repositorio del proyecto

### 4. Configurar Base de Datos MySQL

1. En tu proyecto de Railway, haz clic en "+ New"
2. Selecciona "Database" → "Add MySQL"
3. Railway creará automáticamente una base de datos MySQL
4. Copia las credenciales que aparecen

### 5. Configurar Variables de Entorno

En Railway, ve a tu servicio web y agrega estas variables de entorno:

**Variables Requeridas:**
```
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
PORT=5000

# Database (Railway te dará estos valores automáticamente)
DB_HOST=containers-us-west-xxx.railway.app
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu-password-de-railway
DB_NAME=railway

# Shipping
INTERNATIONAL_SHIPPING_RATE=25.00
LOCAL_SHIPPING_RATE=10.00

# Upload
UPLOAD_FOLDER=static/images/wines
MAX_CONTENT_LENGTH=16777216
```

**IMPORTANTE:** Railway te proporcionará automáticamente las variables de MySQL. Cópialas desde la pestaña "Variables" de tu servicio MySQL.

### 6. Conectar Base de Datos

Railway conectará automáticamente tu aplicación con MySQL usando las variables de entorno. Asegúrate de que tu `config.py` use estas variables.

### 7. Importar Base de Datos

Necesitas importar tu esquema de base de datos a Railway:

**Opción A: Usando Railway CLI**
```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Conectar a tu proyecto
railway link

# Conectar a MySQL y ejecutar script
railway run mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < database_mysql.sql
```

**Opción B: Usando MySQL Workbench o phpMyAdmin**
1. Usa las credenciales de Railway para conectarte
2. Importa el archivo `database_mysql.sql`

### 8. Crear Usuario Admin

Después de importar la base de datos, ejecuta el script para crear el admin:

```bash
# Usando Railway CLI
railway run python create_admin.py
```

O conéctate a la base de datos y ejecuta manualmente:
```sql
INSERT INTO users (email, password, name, is_admin) 
VALUES ('admin@vinosdelvalle.com', '$2b$12$...', 'Admin', 1);
```

### 9. Desplegar

Railway desplegará automáticamente tu aplicación cuando hagas push a tu repositorio:

```bash
git add .
git commit -m "Configurar para producción"
git push origin main
```

### 10. Verificar Despliegue

1. Railway te dará una URL pública (ej: `tu-app.up.railway.app`)
2. Visita la URL para verificar que funciona
3. Prueba el login con las credenciales de admin

## Configuración de Dominio Personalizado (Opcional)

1. En Railway, ve a tu servicio
2. Haz clic en "Settings" → "Domains"
3. Agrega tu dominio personalizado
4. Configura los registros DNS según las instrucciones

## Monitoreo y Logs

- Ve a la pestaña "Deployments" para ver el historial
- Haz clic en "View Logs" para ver los logs en tiempo real
- Railway reiniciará automáticamente tu app si falla

## Solución de Problemas Comunes

### Error de Conexión a Base de Datos
- Verifica que las variables de entorno estén correctas
- Asegúrate de que MySQL esté corriendo en Railway
- Revisa los logs para ver el error específico

### Error 502 Bad Gateway
- Verifica que gunicorn esté instalado en requirements.txt
- Asegúrate de que el Procfile esté correcto
- Revisa que el puerto sea el correcto (Railway usa PORT)

### Imágenes no se Cargan
- Las imágenes subidas se perderán en cada redeploy
- Considera usar un servicio de almacenamiento como:
  - AWS S3
  - Cloudinary
  - Railway Volumes (para persistencia)

## Comandos Útiles de Railway CLI

```bash
# Ver logs en tiempo real
railway logs

# Ejecutar comandos en el servidor
railway run python script.py

# Abrir shell en el servidor
railway shell

# Ver variables de entorno
railway variables

# Conectar a MySQL
railway connect mysql
```

## Costos

Railway ofrece:
- **Plan Hobby**: $5/mes de crédito gratis
- **Plan Pro**: $20/mes con más recursos
- Cobro por uso después de los créditos gratuitos

## Recursos Adicionales

- [Documentación de Railway](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)

## Notas de Seguridad

1. **NUNCA** subas el archivo `.env` a Git
2. Usa variables de entorno en Railway para datos sensibles
3. Cambia `SECRET_KEY` a un valor seguro en producción
4. Habilita HTTPS (Railway lo hace automáticamente)
5. Considera usar Railway's Private Networking para la base de datos

## Backup de Base de Datos

Es importante hacer backups regulares:

```bash
# Exportar base de datos
railway run mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME > backup.sql

# Importar backup
railway run mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < backup.sql
```

---

¡Tu aplicación de vinos ahora está lista para producción en Railway! 🍷🚀
