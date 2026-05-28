/**
 * Admin Panel JavaScript
 * Funcionalidad para el panel de administración
 */

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // SIDEBAR MOBILE TOGGLE
    // ========================================
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarMenu = document.getElementById('sidebarMenu');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    // Toggle del sidebar cuando se hace clic en el botón hamburguesa
    if (sidebarToggle && sidebarMenu && sidebarOverlay) {
        sidebarToggle.addEventListener('click', function() {
            sidebarMenu.classList.toggle('hidden');
            sidebarOverlay.classList.toggle('hidden');
        });

        // Cerrar sidebar cuando se hace clic en el overlay
        sidebarOverlay.addEventListener('click', function() {
            sidebarMenu.classList.add('hidden');
            sidebarOverlay.classList.add('hidden');
        });

        // Cerrar sidebar cuando se selecciona un enlace (solo en mobile)
        const sidebarLinks = sidebarMenu.querySelectorAll('a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Solo cerrar en dispositivos móviles (menos de 768px)
                if (window.innerWidth < 768) {
                    sidebarMenu.classList.add('hidden');
                    sidebarOverlay.classList.add('hidden');
                }
            });
        });
    }

    // ========================================
    // CERRAR SIDEBAR AL CAMBIAR TAMAÑO DE VENTANA
    // ========================================
    window.addEventListener('resize', function() {
        // Si la ventana se hace más grande que mobile, asegurar que el sidebar esté visible
        if (window.innerWidth >= 768) {
            if (sidebarMenu) sidebarMenu.classList.remove('hidden');
            if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
        } else {
            // En mobile, mantener el sidebar oculto por defecto
            if (sidebarMenu) sidebarMenu.classList.add('hidden');
            if (sidebarOverlay) sidebarOverlay.classList.add('hidden');
        }
    });

    // ========================================
    // FUNCIONALIDAD ADICIONAL (OPCIONAL)
    // ========================================
    
    // Confirmar antes de eliminar elementos
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || '¿Estás seguro de que deseas eliminar este elemento?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Auto-cerrar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert-auto-close');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

});
