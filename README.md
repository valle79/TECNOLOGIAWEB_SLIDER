# Flask Modern Slider

Un slider (carrusel) moderno e interactivo construido con Flask como backend y HTML/Tailwind CSS v4/JavaScript en el frontend. Proporciona una experiencia de usuario fluida, responsive y con funcionalidades avanzadas.

## Características Principales

- 🎨 Diseño moderno con efectos glassmorphism y backdrop blur
- 📱 Completamente responsive (móvil, tablet, desktop)
- 👆 Soporte para gestos táctiles (swipe en dispositivos móviles)
- 🌓 Modo claro y oscuro con toggle interactivo
- ⚡ Autoplay con pausa automática en hover
- 🎯 Navegación circular infinita
- 📊 Contador de slides e indicadores visuales (dots)
- 🧭 Navbar responsive con menú móvil
- 🎭 Transiciones suaves y animaciones fluidas
- 🖱️ Controles de navegación intuitivos (botones prev/next)

## Requisitos

- Python 3.8 o superior
- Flask 3.0.0 o superior
- Navegador web moderno con soporte para ES6+

## Instalación

1. Clona este repositorio:
```bash
git clone <repository-url>
cd flask-modern-slider
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activa el entorno virtual:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

1. Ejecuta el servidor Flask:
```bash
python app.py
```

2. Abre tu navegador y visita:
```
http://localhost:5000
```

El servidor se ejecutará en modo debug, lo que permite ver cambios en tiempo real durante el desarrollo.

## Estructura del Proyecto

```
tecnologiaweb_slider/
├── app.py                      # Aplicación Flask principal
├── requirements.txt            # Dependencias de Python
├── README.md                   # Documentación
├── static/                     # Archivos estáticos
│   ├── css/                    # Hojas de estilo
│   ├── js/                     # Scripts JavaScript
│   └── images/                 # Imágenes del slider
└── templates/                  # Templates HTML
    └── index.html              # Template principal
```

### Componentes Principales

- **app.py**: Punto de entrada de la aplicación Flask. Gestiona rutas y datos del slider con validación de datos.
- **templates/index.html**: Template HTML principal con estructura del slider, navbar responsive y controles interactivos.
- **static/css/styles.css**: Archivo de estilos personalizados (actualmente vacío, se usa Tailwind CSS v4 vía CDN).
- **static/js/slider.js**: Lógica JavaScript del slider (navegación, autoplay, controles, swipe, tema oscuro/claro).
- **static/images/**: Directorio con las imágenes de los slides (slide1.jpg - slide4.jpg).

## Tecnologías Utilizadas

- **Backend**: Flask 3.x (Python)
- **Frontend**: HTML5, Tailwind CSS v4 (CDN), JavaScript ES6+
- **Estilos**: Tailwind CSS utility-first framework con efectos glassmorphism
- **Características**: Responsive design, touch gestures, dark/light mode

## Funcionalidades del Slider

### Navegación
- Botones prev/next con iconos SVG
- Indicadores (dots) clicables para acceso directo
- Navegación circular infinita
- Contador visual de slides (ej: 1 / 4)

### Interactividad
- Autoplay cada 4 segundos
- Pausa automática al hacer hover sobre el slider
- Swipe gestures para dispositivos táctiles (50px threshold)
- Toggle de tema oscuro/claro

### Diseño
- Navbar responsive con menú móvil
- Efectos glassmorphism (backdrop-blur)
- Transiciones suaves (opacity, scale, hover effects)
- Gradientes sobre imágenes para mejor legibilidad
- Botones CTA personalizables por slide

## Desarrollo

El proyecto está configurado en modo debug por defecto. Los cambios en archivos Python reiniciarán automáticamente el servidor. Para cambios en archivos estáticos (CSS/JS/HTML), simplemente recarga el navegador.

### Personalización

Para personalizar el slider, puedes modificar:

1. **Datos de los slides** en `app.py`:
   - Edita el array `slides_data` con tus propias imágenes, títulos, descripciones y textos de botones
   - Cada slide requiere: `image_url`, `title`, `description`, `button_text`

2. **Velocidad del autoplay** en `static/js/slider.js`:
   - Modifica el valor en `setInterval(nextSlide, 4000)` (4000ms = 4 segundos)

3. **Estilos** en `templates/index.html`:
   - Ajusta las clases de Tailwind CSS para cambiar colores, tamaños, espaciados, etc.
   - Modifica efectos glassmorphism cambiando `bg-white/10`, `backdrop-blur-md`, etc.

4. **Imágenes**:
   - Reemplaza las imágenes en `static/images/` manteniendo los nombres o actualiza las rutas en `slides_data`

## Estructura de Datos

Cada slide en `app.py` sigue esta estructura:

```python
{
    'image_url': '/static/images/slide1.jpg',  # Ruta a la imagen
    'title': 'Título del Slide',                # Título principal
    'description': 'Descripción del slide',     # Texto descriptivo
    'button_text': 'Texto del Botón'           # Texto del CTA button
}
```

La función `get_slides_data()` valida que todos los campos requeridos estén presentes antes de renderizar.
