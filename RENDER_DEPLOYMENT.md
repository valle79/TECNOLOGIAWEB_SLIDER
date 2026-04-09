# 🚀 Guía Completa de Despliegue en Render

## 📋 Requisitos Previos

1. Cuenta en [Render.com](https://render.com) (gratis)
2. Cuenta en GitHub
3. Tu proyecto subido a un repositorio de GitHub

---

## 🔧 Paso 1: Preparar tu Repositorio Git

```bash
# Si no has inicializado git
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparar proyecto para Render"

# Crear repositorio en GitHub y subir
git remote add origin https://github.com/tu-usuario/tu-repo.git
git branch -M main
git push -u origin main
```

---

## 🌐 Paso 2: Crear Cuenta en Render

1. Ve a [render.com](https://render.com)
2. Haz clic en "Get Started"
3. Inicia sesión con GitHub
4. Autoriza Render para acceder a tus repositorios

---

## 🗄️ Paso 3: Crear Base de Datos MySQL

### Opción A: MySQL en Render (Recomendado para producción)

1. En el Dashboard de Render, haz clic en "New +"
2. Selecciona "MySQL"
3. Configura:
   - **Name**: `vinos-mysql`
   - **Database**: `wine_ecommerce`
   - **User**: `wine_user`
   - **Region**: Elige el más cercano (Oregon, USA)
   - **Plan**: Free (o el que prefieras)
4. Haz clic en "Create Database"
5. **IMPORTANTE**: Guarda las credenciales que aparecen:
   - Internal Database URL
   - External Database URL
   - Host
   - Port
   - Database
   - Username
   - Password

### Opción B: Base de Datos Externa (FreeSQLDatabase, etc.)

Si prefieres usar un servicio gratuito externo:
1. Ve a [freesqldatabase.com](https://www.freesqldatabase.com)
2. Crea una base de datos MySQL gratuita
3. Guarda las credenciales

---

## 🌍 Paso 4: Crear Web Service

1. En Render Dashboard, haz clic en "New +" → "Web Service"
2. Conecta tu repositorio de GitHub
3. Configura el servicio:

### Configuración Básica:
```
Name: vinos-del-valle
Region: Oregon (USA) - o el más cercano
Branch: main
Root Directory: (dejar vacío)
Runtime: Python 3
Build Command: ./build.sh
Start Command: gunicorn app:app
```

### Plan:
- **Free**: Para pruebas (se duerme después de 15 min de inactividad)
- **Starter ($7/mes)**: Para producción (siempre activo)

---

## 🔐 Paso 5: Configurar Variables de Entorno

En la sección "Environment" de tu Web Service, agrega estas variables:

### Variables Requeridas:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=tu-clave-super-secreta-cambiala-aqui-123456789
PORT=10000

# Database Configuration (usa los valores de tu MySQL de Render)
DB_HOST=dpg-xxxxx-a.oregon-postgres.render.com
DB_PORT=3306
DB_USER=wine_user
DB_PASSWORD=tu-password-de-render
DB_NAME=wine_ecommerce

# Shipping Configuration
INTERNATIONAL_SHIPPING_RATE=25.00
LOCAL_SHIPPING_RATE=10.00

# Upload Configuration
UPLOAD_FOLDER=static/images/wines
MAX_CONTENT_LENGTH=16777216
```

**IMPORTANTE**: 
- Reemplaza los valores de `DB_*` con las credenciales de tu base de datos MySQL de Render
- Cambia `SECRET_KEY` por una clave segura y única
- Si usas la Internal Database URL de Render, será algo como: `dpg-xxxxx-a.oregon-postgres.render.com`

---

## 📊 Paso 6: Importar Base de Datos

### Método 1: Usando MySQL Workbench (Recomendado)

1. Abre MySQL Workbench
2. Crea nueva conexión con las credenciales de Render:
   - **Hostname**: El host externo de Render
   - **Port**: 3306
   - **Username**: wine_user
   - **Password**: Tu password de Render
3. Conecta y ejecuta el archivo `database_mysql.sql`

### Método 2: Usando línea de comandos

```bash
# Conectar a MySQL de Render
mysql -h tu-host-de-render.com -P 3306 -u wine_user -p wine_ecommerce < database_mysql.sql
```

### Método 3: Usando phpMyAdmin o Adminer

1. Render no incluye phpMyAdmin, pero puedes usar [Adminer](https://www.adminer.org/)
2. Descarga Adminer y súbelo a tu proyecto
3. Accede vía web y conecta con las credenciales de Render

---

## 👤 Paso 7: Crear Usuario Administrador

Después de importar la base de datos, necesitas crear el usuario admin.

### Opción A: Ejecutar script desde Render Shell

1. En tu Web Service de Render, ve a "Shell"
2. Ejecuta:
```bash
python create_admin.py
```

### Opción B: Insertar manualmente en la base de datos

Conecta a tu MySQL y ejecuta:

```sql
-- Primero, genera el hash de la contraseña en Python
-- python -c "import bcrypt; print(bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode())"

INSERT INTO users (email, password, name, is_admin, created_at) 
VALUES (
    'admin@vinosdelvalle.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5jtJ3yGqK3fC6',  -- password: admin123
    'Administrador', 
    1,
    NOW()
);
```

---

## 🚀 Paso 8: Desplegar

1. Haz clic en "Create Web Service"
2. Render comenzará a construir y desplegar tu aplicación
3. Espera a que el build termine (puede tomar 5-10 minutos)
4. Una vez completado, verás "Live" en verde

---

## ✅ Paso 9: Verificar Despliegue

1. Render te dará una URL pública: `https://vinos-del-valle.onrender.com`
2. Visita la URL
3. Prueba el login con:
   - **Email**: admin@vinosdelvalle.com
   - **Password**: admin123
4. Verifica que puedas:
   - Ver el catálogo
   - Agregar productos al carrito
   - Acceder al panel de admin

---

## 🌐 Paso 10: Dominio Personalizado (Opcional)

### Configurar tu propio dominio:

1. En tu Web Service, ve a "Settings" → "Custom Domain"
2. Haz clic en "Add Custom Domain"
3. Ingresa tu dominio (ej: `www.vinosdelvalle.com`)
4. Render te dará registros DNS para configurar:

```
Type: CNAME
Name: www
Value: vinos-del-valle.onrender.com
```

5. Agrega estos registros en tu proveedor de dominio (GoDaddy, Namecheap, etc.)
6. Espera la propagación DNS (puede tomar hasta 48 horas)

---

## 📁 Paso 11: Configurar Almacenamiento de Imágenes (Importante)

⚠️ **PROBLEMA**: Render usa almacenamiento efímero. Las imágenes subidas se perderán en cada redeploy.

### Solución: Usar Cloudinary (Recomendado y Gratuito)

1. Crea cuenta en [Cloudinary](https://cloudinary.com) (gratis)
2. Obtén tus credenciales (Cloud Name, API Key, API Secret)
3. Instala el SDK:

```bash
pip install cloudinary
```

4. Agrega a `requirements.txt`:
```
cloudinary>=1.36.0
```

5. Actualiza `utils/file_upload.py` para usar Cloudinary:

```python
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

def save_wine_image(file):
    result = cloudinary.uploader.upload(file)
    return result['secure_url']
```

6. Agrega variables de entorno en Render:
```
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

---

## 🔍 Monitoreo y Logs

### Ver Logs en Tiempo Real:
1. Ve a tu Web Service
2. Haz clic en "Logs"
3. Verás todos los logs de tu aplicación

### Métricas:
1. Ve a "Metrics" para ver:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🐛 Solución de Problemas Comunes

### 1. Error: "Application failed to respond"
```bash
# Verifica que gunicorn esté en requirements.txt
# Verifica que el comando de inicio sea correcto: gunicorn app:app
# Revisa los logs para ver el error específico
```

### 2. Error de Conexión a Base de Datos
```bash
# Verifica las variables de entorno DB_*
# Asegúrate de usar el host EXTERNO de Render para conexiones desde fuera
# Verifica que MySQL esté corriendo (debe estar en "Available")
```

### 3. Error 502 Bad Gateway
```bash
# Verifica que el puerto sea 10000 (Render lo requiere)
# Asegúrate de que app.py use: app.run(host='0.0.0.0', port=port)
# Revisa que no haya errores de sintaxis en el código
```

### 4. Las imágenes no se cargan
```bash
# Implementa Cloudinary como se explicó arriba
# O usa un servicio de almacenamiento externo (AWS S3, etc.)
```

### 5. La aplicación se "duerme" (Plan Free)
```bash
# El plan Free se duerme después de 15 minutos de inactividad
# La primera petición después de dormir tomará ~30 segundos
# Solución: Upgrade a plan Starter ($7/mes) para mantenerla siempre activa
```

---

## 💰 Costos de Render

### Plan Free:
- ✅ 750 horas/mes gratis
- ✅ SSL automático
- ❌ Se duerme después de 15 min de inactividad
- ❌ 512 MB RAM
- ❌ Almacenamiento efímero

### Plan Starter ($7/mes):
- ✅ Siempre activo
- ✅ 512 MB RAM
- ✅ SSL automático
- ✅ Mejor rendimiento

### MySQL Database:
- Free: 1 GB storage
- Starter: $7/mes - 10 GB storage

---

## 🔒 Mejores Prácticas de Seguridad

1. ✅ Cambia `SECRET_KEY` a un valor único y seguro
2. ✅ Usa variables de entorno para datos sensibles
3. ✅ Nunca subas `.env` a Git
4. ✅ Habilita HTTPS (Render lo hace automáticamente)
5. ✅ Usa contraseñas fuertes para la base de datos
6. ✅ Actualiza regularmente las dependencias
7. ✅ Implementa rate limiting para prevenir ataques

---

## 📦 Backup de Base de Datos

### Exportar base de datos:
```bash
mysqldump -h tu-host-render.com -P 3306 -u wine_user -p wine_ecommerce > backup_$(date +%Y%m%d).sql
```

### Importar backup:
```bash
mysql -h tu-host-render.com -P 3306 -u wine_user -p wine_ecommerce < backup_20240101.sql
```

### Automatizar backups:
Considera usar servicios como:
- [SimpleBackups](https://simplebackups.com)
- [BackupNinja](https://backupninja.com)
- Cron jobs en un servidor separado

---

## 🔄 Actualizar la Aplicación

Render despliega automáticamente cuando haces push a GitHub:

```bash
# Hacer cambios en tu código
git add .
git commit -m "Actualizar funcionalidad X"
git push origin main

# Render detectará el push y redesplegará automáticamente
```

---

## 📚 Recursos Útiles

- [Documentación de Render](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Render Status](https://status.render.com)
- [Gunicorn Documentation](https://docs.gunicorn.org)

---

## 🎉 ¡Listo!

Tu aplicación de vinos ahora está desplegada en Render y lista para producción. 

**URL de tu aplicación**: `https://vinos-del-valle.onrender.com`

**Credenciales de Admin**:
- Email: admin@vinosdelvalle.com
- Password: admin123

**Recuerda**:
- Cambiar la contraseña del admin después del primer login
- Configurar Cloudinary para las imágenes
- Hacer backups regulares de la base de datos
- Monitorear los logs regularmente

---

## 🆘 ¿Necesitas Ayuda?

Si encuentras problemas:
1. Revisa los logs en Render
2. Consulta la documentación de Render
3. Busca en Render Community
4. Revisa este archivo de nuevo

¡Buena suerte con tu tienda de vinos! 🍷🚀
