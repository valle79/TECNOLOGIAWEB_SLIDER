# Vinos del Valle - E-commerce Platform

Sistema de e-commerce profesional para venta de vinos premium en Perú con capacidad de exportación internacional. Construido con Flask, PostgreSQL (Neon), y tecnologías web modernas.

## 🎯 Características Principales

### Frontend
- ✨ Diseño moderno y responsive con Tailwind CSS
- 🛒 Carrito de compras interactivo con AJAX
- 🔍 Catálogo con filtros avanzados (tipo, país, precio, búsqueda)
- 📱 Completamente responsive (móvil, tablet, desktop)
- 🎨 Interfaz elegante tipo tienda premium
- ⚡ Experiencia de usuario fluida

### Backend
- 🐍 Python 3.8+ con Flask 3.x
- 🗄️ PostgreSQL (compatible con Neon.tech)
- 🏗️ Arquitectura MVC profesional (Models, Services, Controllers)
- 🔐 Sistema de autenticación con bcrypt
- 📦 Gestión de sesiones y carrito
- 🌍 Cálculo automático de envío local/internacional

### Funcionalidades de Negocio
- 🍷 Catálogo completo de vinos con detalles
- 🛍️ Sistema de compras con carrito
- 📋 Gestión de pedidos y estados
- 👥 Registro y login de usuarios
- 🔧 Panel de administración completo
- 🌎 Soporte para exportación internacional
- 💰 Cálculo de costos de envío por país
- 📊 Dashboard con estadísticas de ventas

### Seguridad
- ✅ Validación de inputs en frontend y backend
- 🔒 Consultas parametrizadas (prevención SQL injection)
- 🛡️ Contraseñas hasheadas con bcrypt
- 🔐 Sesiones seguras con Flask
- ⚠️ Manejo robusto de errores

## 📁 Estructura del Proyecto

```
wine-ecommerce/
├── app.py                      # Aplicación principal Flask
├── config.py                   # Configuración de la aplicación
├── database.sql                # Script de inicialización de BD
├── requirements.txt            # Dependencias Python
├── .env.example                # Ejemplo de variables de entorno
├── INSTALL.md                  # Guía de instalación detallada
├── README.md                   # Este archivo
│
├── models/                     # Modelos de datos
│   ├── __init__.py
│   ├── database.py            # Gestión de conexiones
│   ├── wine.py                # Modelo de vinos
│   ├── order.py               # Modelo de pedidos
│   └── user.py                # Modelo de usuarios
│
├── services/                   # Lógica de negocio
│   ├── __init__.py
│   ├── cart_service.py        # Servicio de carrito
│   └── order_service.py       # Servicio de pedidos
│
├── controllers/                # Controladores/Rutas
│   ├── __init__.py
│   ├── main_controller.py     # Rutas principales
│   ├── wine_controller.py     # Rutas de vinos
│   ├── cart_controller.py     # Rutas de carrito
│   ├── order_controller.py    # Rutas de pedidos
│   ├── auth_controller.py     # Autenticación
│   └── admin_controller.py    # Panel admin
│
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── index.html             # Página principal
│   ├── catalog.html           # Catálogo de vinos
│   ├── wine_detail.html       # Detalle de vino
│   ├── cart.html              # Carrito de compras
│   ├── checkout.html          # Checkout
│   ├── order_confirmation.html # Confirmación de pedido
│   ├── login.html             # Login
│   ├── register.html          # Registro
│   ├── my_orders.html         # Mis pedidos
│   ├── 404.html               # Error 404
│   ├── 500.html               # Error 500
│   └── admin/                 # Templates de admin
│       ├── dashboard.html
│       ├── wines.html
│       ├── wine_form.html
│       ├── orders.html
│       └── order_detail.html
│
└── static/                     # Archivos estáticos
    ├── css/
    │   └── styles.css         # Estilos personalizados
    ├── js/
    │   ├── main.js            # JavaScript principal
    │   └── slider.js          # (legacy - puede eliminarse)
    ├── images/
    │   ├── wines/             # Imágenes de vinos
    │   ├── icons/             # Iconos
    │   └── hero-wine.jpg      # Imagen hero
    └── icons/                 # Iconos adicionales
```

## 🚀 Instalación Rápida

### 1. Requisitos
- Python 3.8+
- PostgreSQL o cuenta en Neon.tech
- pip

### 2. Clonar e Instalar
```bash
git clone <repository-url>
cd wine-ecommerce
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar Base de Datos
```bash
# Crear cuenta en Neon.tech o usar PostgreSQL local
# Ejecutar database.sql en tu base de datos
```

### 4. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 5. Ejecutar
```bash
python app.py
```

Visita: `http://localhost:5000`

**Ver [INSTALL.md](INSTALL.md) para instrucciones detalladas.**

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask 3.x** - Framework web Python
- **PostgreSQL** - Base de datos relacional
- **psycopg2** - Adaptador PostgreSQL para Python
- **bcrypt** - Hashing de contraseñas
- **python-dotenv** - Gestión de variables de entorno

### Frontend
- **HTML5** - Estructura
- **Tailwind CSS** - Framework CSS utility-first
- **JavaScript ES6+** - Interactividad
- **Fetch API** - Comunicación AJAX

### Base de Datos
- **Neon.tech** - PostgreSQL serverless (recomendado)
- **PostgreSQL 14+** - Compatible con cualquier instancia

## 📊 Esquema de Base de Datos

### Tablas Principales

**users** - Usuarios del sistema
- id (UUID, PK)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- full_name (VARCHAR)
- phone (VARCHAR)
- is_admin (BOOLEAN)
- created_at, updated_at (TIMESTAMP)

**wines** - Catálogo de vinos
- id (UUID, PK)
- name (VARCHAR)
- wine_type (VARCHAR) - Tinto, Blanco, Rosé, Espumoso
- price (DECIMAL)
- country (VARCHAR)
- region (VARCHAR)
- year (INTEGER)
- grape_variety (VARCHAR)
- alcohol_content (DECIMAL)
- description (TEXT)
- stock (INTEGER)
- image_url (VARCHAR)
- is_featured (BOOLEAN)
- created_at, updated_at (TIMESTAMP)

**orders** - Pedidos
- id (UUID, PK)
- user_id (UUID, FK)
- customer_name, customer_email, customer_phone
- shipping_address, shipping_city, shipping_country
- is_international (BOOLEAN)
- subtotal, shipping_cost, total (DECIMAL)
- status (VARCHAR) - pending, confirmed, processing, shipped, delivered, cancelled
- payment_method (VARCHAR)
- notes (TEXT)
- created_at, updated_at (TIMESTAMP)

**order_items** - Detalles de pedidos
- id (UUID, PK)
- order_id (UUID, FK)
- wine_id (UUID, FK)
- wine_name, wine_price (VARCHAR, DECIMAL)
- quantity (INTEGER)
- subtotal (DECIMAL)
- created_at (TIMESTAMP)

## 🔐 Credenciales por Defecto

**Administrador:**
- Email: `admin@vinosdelvalle.com`
- Contraseña: `admin123`

⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción.

## 🌐 API Endpoints

### Públicos
- `GET /` - Página principal
- `GET /wines` - Catálogo de vinos
- `GET /wines/<id>` - Detalle de vino
- `GET /wines/api/wines` - API de vinos (JSON)
- `POST /cart/add` - Agregar al carrito
- `POST /cart/update` - Actualizar carrito
- `POST /cart/remove` - Eliminar del carrito
- `GET /cart` - Ver carrito

### Autenticación Requerida
- `GET /orders/checkout` - Checkout
- `POST /orders/create` - Crear pedido
- `GET /orders/my-orders` - Mis pedidos
- `GET /orders/<id>` - Detalle de pedido

### Admin (Requiere is_admin=true)
- `GET /admin/dashboard` - Dashboard
- `GET /admin/wines` - Gestionar vinos
- `POST /admin/wines/add` - Agregar vino
- `POST /admin/wines/edit/<id>` - Editar vino
- `POST /admin/wines/delete/<id>` - Eliminar vino
- `GET /admin/orders` - Gestionar pedidos
- `POST /admin/orders/<id>/update-status` - Actualizar estado

## 💡 Características Avanzadas

### Exportación Internacional
- Detección automática de país
- Cálculo de costos de envío diferenciados
- Campos específicos para envío internacional

### Panel de Administración
- Dashboard con estadísticas
- Gestión completa de vinos (CRUD)
- Gestión de pedidos y estados
- Filtros y búsqueda avanzada

### Carrito de Compras
- Persistencia en sesión
- Actualización en tiempo real
- Validación de stock
- Cálculo automático de totales

## 🎨 Personalización

### Cambiar Colores
Editar clases de Tailwind en templates:
- `bg-red-800` → Color principal
- `text-red-800` → Color de texto
- `hover:bg-red-900` → Color hover

### Agregar Vinos
1. Acceder al panel admin
2. Ir a "Gestionar Vinos"
3. Click en "Agregar Vino"
4. Completar formulario

### Modificar Costos de Envío
Editar en `config.py`:
```python
INTERNATIONAL_SHIPPING_RATE = 25.00
LOCAL_SHIPPING_RATE = 10.00
```

## 📝 Buenas Prácticas Implementadas

- ✅ Separación de responsabilidades (MVC)
- ✅ Validación de datos en múltiples capas
- ✅ Manejo de errores robusto
- ✅ Logging de aplicación
- ✅ Connection pooling para BD
- ✅ Consultas parametrizadas
- ✅ Código modular y reutilizable
- ✅ Comentarios y documentación
- ✅ Variables de entorno para configuración
- ✅ Estructura escalable

## 🚀 Despliegue en Producción

### Recomendaciones
1. Usar Gunicorn como servidor WSGI
2. Configurar Nginx como reverse proxy
3. Habilitar HTTPS con Let's Encrypt
4. Usar variables de entorno seguras
5. Configurar backups de base de datos
6. Implementar monitoreo y logs
7. Optimizar imágenes
8. Configurar CDN para estáticos

### Ejemplo con Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🐛 Solución de Problemas

Ver [INSTALL.md](INSTALL.md) para soluciones comunes.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o soporte:
- Email: info@vinosdelvalle.com
- Web: www.vinosdelvalle.com

---

**Desarrollado con ❤️ para la industria vitivinícola peruana**
