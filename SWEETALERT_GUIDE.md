# 🎨 Guía de Alertas Profesionales con SweetAlert2

## 📋 Descripción

Se han implementado alertas profesionales y elegantes usando **SweetAlert2** en todo el proyecto. Las alertas están completamente integradas y listas para usar en todas las páginas.

## ✨ Características Implementadas

### 🔧 Configuración Global
- ✅ SweetAlert2 instalado en `admin_base.html` y `base.html`
- ✅ Tema Material UI aplicado
- ✅ Animaciones con Animate.css
- ✅ Configuración personalizada con colores del proyecto

### 📦 Utilidades Disponibles

#### Para el Panel de Administración (`AdminAlerts`)

```javascript
// Alerta de éxito
AdminAlerts.success('¡Éxito!', 'La operación se completó correctamente');

// Alerta de error
AdminAlerts.error('Error', 'Algo salió mal');

// Alerta de advertencia
AdminAlerts.warning('Advertencia', 'Ten cuidado con esta acción');

// Alerta de información
AdminAlerts.info('Información', 'Aquí hay información importante');

// Confirmación de eliminación
AdminAlerts.confirmDelete('Vino Malbec 2020').then((result) => {
    if (result.isConfirmed) {
        // Usuario confirmó la eliminación
    }
});

// Confirmación genérica
AdminAlerts.confirm('¿Continuar?', 'Esta acción es importante', 'Sí', 'No').then((result) => {
    if (result.isConfirmed) {
        // Usuario confirmó
    }
});

// Indicador de carga
AdminAlerts.loading('Procesando...', 'Por favor espera');
// Cerrar con: Swal.close();

// Toast (notificación pequeña)
AdminAlerts.toast('Guardado correctamente', 'success');
```

#### Para el Sitio Público (`Alerts`)

```javascript
// Alerta de éxito
Alerts.success('¡Producto agregado!', 'Se agregó al carrito');

// Alerta de error
Alerts.error('Error', 'No se pudo procesar');

// Confirmación
Alerts.confirm('¿Eliminar?', '¿Estás seguro?', 'Sí', 'No').then((result) => {
    if (result.isConfirmed) {
        // Usuario confirmó
    }
});

// Indicador de carga
Alerts.loading('Cargando...', 'Espera un momento');

// Toast
Alerts.toast('¡Listo!', 'success');
```

## 🎯 Implementaciones Realizadas

### 1. Panel de Administración

#### ✅ Gestión de Vinos (`admin_wines.html`)
- Confirmación elegante antes de eliminar vinos
- Indicador de carga durante la eliminación
- Nombre del vino mostrado en la confirmación

#### ✅ Formulario de Vinos (`admin_wine_form.html`)
- Validación de campos requeridos
- Indicador de carga al guardar/actualizar
- Validación de imágenes (tamaño y tipo)
- Preview de imágenes cargadas

#### ✅ JavaScript Admin (`admin.js`)
- Sistema completo de alertas
- Validación automática de formularios
- Confirmaciones para cambios de estado
- Manejo de flash messages
- Auto-guardado con indicadores

### 2. Sitio Público

#### ✅ Carrito de Compras (`cart.html` + `main.js`)
- Confirmación antes de eliminar productos
- Validación de cantidad vs stock
- Alertas de éxito al actualizar
- Animación al eliminar items
- Toast notifications

#### ✅ Checkout (`checkout.html` + `checkout.js`)
- Validación completa de formulario
- Validación de email y teléfono
- Confirmación final antes de realizar pedido
- Indicador de carga durante el proceso
- Resaltado de campos inválidos

#### ✅ Gestión de Carrito (`main.js`)
- Alertas al agregar productos
- Confirmación al eliminar
- Indicadores de carga en operaciones AJAX
- Actualización automática de contadores

## 🎨 Estilos Personalizados

Las alertas están estilizadas con:
- Colores del proyecto (rojo vino #7f1d1d)
- Bordes redondeados (rounded-xl)
- Sombras profesionales (shadow-2xl)
- Animaciones suaves (Animate.css)
- Botones con hover effects
- Tema Material UI

## 📝 Ejemplos de Uso

### Ejemplo 1: Eliminar un Vino
```html
<button onclick="AdminAlerts.confirmDelete('Vino Malbec').then((result) => {
    if (result.isConfirmed) {
        AdminAlerts.loading('Eliminando...', 'Por favor espera');
        // Realizar eliminación
    }
})">
    Eliminar
</button>
```

### Ejemplo 2: Agregar al Carrito
```javascript
async function addToCart(wineId) {
    Alerts.loading('Agregando al carrito...', 'Por favor espera');
    
    try {
        const response = await fetch('/cart/add', {
            method: 'POST',
            body: JSON.stringify({ wine_id: wineId })
        });
        
        Swal.close();
        
        if (response.ok) {
            Alerts.toast('¡Producto agregado!', 'success');
        } else {
            Alerts.error('Error', 'No se pudo agregar el producto');
        }
    } catch (error) {
        Swal.close();
        Alerts.error('Error de conexión', 'Intenta nuevamente');
    }
}
```

### Ejemplo 3: Validar Formulario
```javascript
form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!validateForm()) {
        AdminAlerts.warning('Campos incompletos', 'Completa todos los campos');
        return;
    }
    
    AdminAlerts.loading('Guardando...', 'Por favor espera');
    this.submit();
});
```

## 🔍 Atributos HTML Especiales

### Para Confirmación de Eliminación
```html
<button data-confirm-delete="Nombre del elemento">Eliminar</button>
```

### Para Validación de Formularios
```html
<form data-validate="true">
    <!-- campos del formulario -->
</form>
```

### Para Cambio de Estado
```html
<button data-change-status="confirmado" data-item-name="Pedido #123">
    Cambiar Estado
</button>
```

### Para Flash Messages
```html
<div data-flash-message="Operación exitosa" data-flash-type="success"></div>
```

## 🎭 Tipos de Iconos Disponibles

- `success` - ✅ Éxito (verde)
- `error` - ❌ Error (rojo)
- `warning` - ⚠️ Advertencia (amarillo)
- `info` - ℹ️ Información (azul)
- `question` - ❓ Pregunta (gris)

## 🚀 Mejoras Implementadas

1. **Experiencia de Usuario**
   - Animaciones suaves y profesionales
   - Feedback visual inmediato
   - Confirmaciones claras y descriptivas
   - Indicadores de carga durante operaciones

2. **Validación**
   - Validación en tiempo real
   - Resaltado de campos inválidos
   - Mensajes de error específicos
   - Scroll automático a campos con error

3. **Accesibilidad**
   - Botones con focus visible
   - Textos descriptivos
   - Escape key para cerrar
   - Click fuera para cerrar (configurable)

4. **Responsive**
   - Alertas adaptadas a móviles
   - Toast en posición óptima
   - Botones táctiles grandes

## 📱 Compatibilidad

- ✅ Chrome/Edge (últimas versiones)
- ✅ Firefox (últimas versiones)
- ✅ Safari (últimas versiones)
- ✅ Móviles iOS/Android
- ✅ Tablets

## 🔧 Personalización Adicional

Si necesitas personalizar más las alertas, puedes modificar `SwalConfig` en:
- `static/js/admin.js` (para admin)
- `static/js/main.js` (para sitio público)

```javascript
const SwalConfig = {
    customClass: {
        popup: 'rounded-xl shadow-2xl',
        title: 'text-2xl font-bold',
        confirmButton: 'bg-red-900 hover:bg-red-800 ...',
        // ... más clases
    },
    buttonsStyling: false,
    // ... más opciones
};
```

## 📚 Documentación Oficial

Para más opciones y configuraciones avanzadas:
- [SweetAlert2 Documentation](https://sweetalert2.github.io/)
- [SweetAlert2 Examples](https://sweetalert2.github.io/#examples)

## ✅ Checklist de Implementación

- [x] SweetAlert2 instalado en templates base
- [x] Animate.css agregado
- [x] Utilidades AdminAlerts creadas
- [x] Utilidades Alerts creadas
- [x] Confirmaciones de eliminación en admin
- [x] Validación de formularios
- [x] Alertas en carrito de compras
- [x] Validación de checkout
- [x] Toast notifications
- [x] Indicadores de carga
- [x] Animaciones personalizadas
- [x] Estilos del proyecto aplicados

## 🎉 ¡Todo Listo!

Las alertas profesionales están completamente implementadas y funcionando en todo el proyecto. Disfruta de una experiencia de usuario mejorada y profesional.
