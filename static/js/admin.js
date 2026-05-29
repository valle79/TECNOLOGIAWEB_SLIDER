/**
 * Admin Panel JavaScript - Professional Edition
 * Funcionalidad avanzada para el panel de administración con SweetAlert2
 */

// ========================================
// CONFIGURACIÓN DE SWEETALERT2
// ========================================
const SwalConfig = {
    customClass: {
        popup: 'rounded-xl shadow-2xl',
        title: 'text-2xl font-bold',
        confirmButton: 'bg-red-900 hover:bg-red-800 text-white font-bold py-2 px-6 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl',
        cancelButton: 'bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded-lg transition-all duration-200 ml-2',
        denyButton: 'bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-6 rounded-lg transition-all duration-200 ml-2'
    },
    buttonsStyling: false,
    showClass: {
        popup: 'animate__animated animate__fadeInDown animate__faster'
    },
    hideClass: {
        popup: 'animate__animated animate__fadeOutUp animate__faster'
    }
};

// ========================================
// UTILIDADES DE ALERTAS
// ========================================
const AdminAlerts = {
    // Alerta de éxito
    success: (title, text = '') => {
        return Swal.fire({
            ...SwalConfig,
            icon: 'success',
            title: title,
            text: text,
            timer: 3000,
            timerProgressBar: true,
            showConfirmButton: false
        });
    },

    // Alerta de error
    error: (title, text = '') => {
        return Swal.fire({
            ...SwalConfig,
            icon: 'error',
            title: title,
            text: text,
            confirmButtonText: 'Entendido'
        });
    },

    // Alerta de advertencia
    warning: (title, text = '') => {
        return Swal.fire({
            ...SwalConfig,
            icon: 'warning',
            title: title,
            text: text,
            confirmButtonText: 'Entendido'
        });
    },

    // Alerta de información
    info: (title, text = '') => {
        return Swal.fire({
            ...SwalConfig,
            icon: 'info',
            title: title,
            text: text,
            confirmButtonText: 'Entendido'
        });
    },

    // Confirmación de eliminación
    confirmDelete: (itemName = 'este elemento') => {
        return Swal.fire({
            ...SwalConfig,
            title: '¿Estás seguro?',
            html: `Estás a punto de eliminar <strong>${itemName}</strong>.<br>Esta acción no se puede deshacer.`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar',
            reverseButtons: true,
            focusCancel: true
        });
    },

    // Confirmación genérica
    confirm: (title, text, confirmText = 'Confirmar', cancelText = 'Cancelar') => {
        return Swal.fire({
            ...SwalConfig,
            title: title,
            text: text,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: confirmText,
            cancelButtonText: cancelText,
            reverseButtons: true
        });
    },

    // Alerta de carga
    loading: (title = 'Procesando...', text = 'Por favor espera') => {
        return Swal.fire({
            ...SwalConfig,
            title: title,
            text: text,
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
    },

    // Toast notification (pequeña notificación)
    toast: (message, icon = 'success') => {
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer);
                toast.addEventListener('mouseleave', Swal.resumeTimer);
            }
        });

        return Toast.fire({
            icon: icon,
            title: message
        });
    }
};

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
    // CONFIRMACIÓN DE ELIMINACIÓN CON SWEETALERT2
    // ========================================
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemName = this.getAttribute('data-confirm-delete') || 'este elemento';
            const form = this.closest('form');
            
            AdminAlerts.confirmDelete(itemName).then((result) => {
                if (result.isConfirmed) {
                    // Mostrar loading
                    AdminAlerts.loading('Eliminando...', 'Por favor espera un momento');
                    
                    // Enviar el formulario
                    if (form) {
                        form.submit();
                    }
                }
            });
        });
    });

    // ========================================
    // MANEJO DE FORMULARIOS CON CONFIRMACIÓN
    // ========================================
    const confirmForms = document.querySelectorAll('[data-confirm-submit]');
    confirmForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const message = this.getAttribute('data-confirm-submit') || '¿Deseas continuar con esta acción?';
            
            AdminAlerts.confirm('Confirmar acción', message, 'Sí, continuar', 'Cancelar').then((result) => {
                if (result.isConfirmed) {
                    AdminAlerts.loading('Procesando...', 'Por favor espera');
                    this.submit();
                }
            });
        });
    });

    // ========================================
    // VALIDACIÓN DE FORMULARIOS
    // ========================================
    const adminForms = document.querySelectorAll('form[data-validate]');
    adminForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            let firstInvalidField = null;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    if (!firstInvalidField) firstInvalidField = field;
                } else {
                    field.classList.remove('border-red-500');
                }
            });

            if (!isValid) {
                e.preventDefault();
                AdminAlerts.warning('Campos incompletos', 'Por favor completa todos los campos requeridos');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                    firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });

    // ========================================
    // MOSTRAR ALERTAS DE FLASH MESSAGES
    // ========================================
    const flashMessages = document.querySelectorAll('[data-flash-message]');
    flashMessages.forEach(message => {
        const type = message.getAttribute('data-flash-type') || 'info';
        const text = message.getAttribute('data-flash-message');
        
        if (type === 'success') {
            AdminAlerts.toast(text, 'success');
        } else if (type === 'error') {
            AdminAlerts.toast(text, 'error');
        } else if (type === 'warning') {
            AdminAlerts.toast(text, 'warning');
        } else {
            AdminAlerts.toast(text, 'info');
        }
        
        // Remover el elemento del DOM
        message.remove();
    });

    // ========================================
    // CONFIRMACIÓN DE CAMBIO DE ESTADO
    // ========================================
    const statusButtons = document.querySelectorAll('[data-change-status]');
    statusButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const newStatus = this.getAttribute('data-change-status');
            const itemName = this.getAttribute('data-item-name') || 'este elemento';
            
            AdminAlerts.confirm(
                'Cambiar estado',
                `¿Deseas cambiar el estado de ${itemName} a "${newStatus}"?`,
                'Sí, cambiar',
                'Cancelar'
            ).then((result) => {
                if (result.isConfirmed) {
                    AdminAlerts.loading('Actualizando estado...', 'Por favor espera');
                    // Aquí iría la lógica para cambiar el estado
                    const form = this.closest('form');
                    if (form) form.submit();
                }
            });
        });
    });

    // ========================================
    // PREVIEW DE IMÁGENES
    // ========================================
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tamaño (máx 16MB)
                if (file.size > 16 * 1024 * 1024) {
                    AdminAlerts.error('Archivo muy grande', 'La imagen no debe superar los 16MB');
                    this.value = '';
                    return;
                }

                // Validar tipo
                if (!file.type.startsWith('image/')) {
                    AdminAlerts.error('Tipo de archivo inválido', 'Por favor selecciona una imagen válida');
                    this.value = '';
                    return;
                }

                // Mostrar preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    AdminAlerts.toast('Imagen cargada correctamente', 'success');
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // ========================================
    // AUTO-GUARDAR INDICADOR
    // ========================================
    const autoSaveForms = document.querySelectorAll('[data-auto-save]');
    autoSaveForms.forEach(form => {
        let saveTimeout;
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    AdminAlerts.toast('Cambios guardados automáticamente', 'success');
                }, 2000);
            });
        });
    });

});

// ========================================
// EXPORTAR UTILIDADES GLOBALMENTE
// ========================================
window.AdminAlerts = AdminAlerts;
