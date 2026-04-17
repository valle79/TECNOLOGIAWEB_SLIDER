# 🖼️ Configuración de Cloudinary en Render

## Problema
Las imágenes de vinos no se suben correctamente en Render porque faltan las variables de entorno de Cloudinary.

## Solución - Pasos a seguir:

### 1️⃣ Crea una cuenta en Cloudinary (si no tienes)
- Ve a: https://cloudinary.com/
- Regístrate de forma gratuita
- Confirma tu email

### 2️⃣ Obtén tus credenciales
- Accede a tu Dashboard de Cloudinary
- En la esquina superior derecha, haz clic en tu perfil
- Selecciona **Settings**
- Ve a la pestaña **API Keys**
- Copia estos datos:
  - **Cloud Name**
  - **API Key**
  - **API Secret**

### 3️⃣ Configura las variables en Render

**Opción A: Desde el Dashboard de Render (Recomendado)**

1. Accede a https://render.com/
2. Abre tu servicio web "vinos-del-valle"
3. Ve a **Environment**
4. Haz clic en **"Add Environment Variable"**
5. Agrega estas 3 variables:

```
CLOUDINARY_CLOUD_NAME = [Tu Cloud Name de Cloudinary]
CLOUDINARY_API_KEY = [Tu API Key de Cloudinary]
CLOUDINARY_API_SECRET = [Tu API Secret de Cloudinary]
```

**Opción B: Desde el archivo render.yaml**

Si prefieres, puedes editar directamente el `render.yaml`:

```yaml
envVars:
  - key: CLOUDINARY_CLOUD_NAME
    value: "tu_cloud_name_aqui"
  - key: CLOUDINARY_API_KEY
    value: "tu_api_key_aqui"
  - key: CLOUDINARY_API_SECRET
    value: "tu_api_secret_aqui"
```

### 4️⃣ Redeploy tu aplicación

Después de agregar las variables de entorno:

1. Ve a tu Dashboard de Render
2. Abre "vinos-del-valle"
3. Haz clic en **"Manual Deploy"** > **"Deploy latest commit"**
4. Espera a que el deploy termine

### 5️⃣ Prueba la carga de imágenes

1. Accede a tu app en producción
2. Inicia sesión como administrador
3. Ve a **Gestionar Vinos** > **Agregar Vino**
4. Intenta subir una imagen
5. Si funciona, ¡listo! ✅

## ⚠️ Solución de Problemas

### Las imágenes aún no se suben
- ✅ Verifica que las variables de entorno estén configuradas correctamente en Render
- ✅ Haz clic en **Manual Deploy** para recargar
- ✅ Limpia el cache del navegador (Ctrl+Shift+Del)
- ✅ Abre la consola del navegador (F12) para ver si hay errores

### Error: "Credenciales de Cloudinary inválidas"
- ✅ Verifica que copiaste bien el Cloud Name, API Key y API Secret
- ✅ Asegúrate de que NO hay espacios al principio o final
- ✅ Ve a Cloudinary Dashboard y confirma que los valores son correctos

### Seguridad: ¿Debo proteger mi API Secret?
- ✅ **SÍ**, usar variables de entorno es la forma segura
- ✅ **NUNCA** pongas credenciales en el código
- ✅ Las variables en Render están encriptadas

## 📚 Recursos útiles
- Documentación de Cloudinary: https://cloudinary.com/documentation
- Documentación de Render: https://render.com/docs

---

**Nota**: Una vez configurado, cualquier imagen que subes se almacena en la nube de Cloudinary, no en el servidor de Render. Esto es mucho más seguro y escalable.
