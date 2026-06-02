/**
 * Admin Panel JavaScript - Professional Edition with SweetAlert2
 * Funcionalidad avanzada para el panel de administración
 */

// ========================================
// APLICAR TEMA DINÁMICO
// ========================================
(function() {
    const themeColor = document.body.dataset.themeColor;
    if (themeColor) {
        document.documentElement.style.setProperty('--theme-color', themeColor);
        document.documentElement.style.setProperty('--theme-color-dark', themeColor + 'dd');
        document.documentElement.style.setProperty('--theme-color-darker', themeColor + 'bb');
    }
})();

// ========================================
// UTILIDADES DE ALERTAS CON SWEETALERT2
// ========================================
const AdminAlerts = {
    // Alerta de éxito
    success: (title, text = '') => {
        return Swal.fire({
            icon: 'success',
            title: title,
            text: text,
            confirmButtonColor: '#7f1d1d',
            showClass: {
                popup: 'animate__animated animate__fadeInDown'
            },
            hideClass: {
                popup: 'animate__animated animate__fadeOutUp'
            }
        });
    },

    // Alerta de error
    error: (title, text = '') => {
        return Swal.fire({
            icon: 'error',
            title: title,
            text: text,
            confirmButtonColor: '#7f1d1d',
            showClass: {
                popup: 'animate__animated animate__shakeX'
            }
        });
    },

    // Alerta de advertencia
    warning: (title, text = '') => {
        return Swal.fire({
            icon: 'warning',
            title: title,
            text: text,
            confirmButtonColor: '#7f1d1d',
            showClass: {
                popup: 'animate__animated animate__fadeInDown'
            }
        });
    },

    // Alerta de información
    info: (title, text = '') => {
        return Swal.fire({
            icon: 'info',
            title: title,
            text: text,
            confirmButtonColor: '#7f1d1d',
            showClass: {
                popup: 'animate__animated animate__fadeInDown'
            }
        });
    },

    // Confirmación de eliminación con SweetAlert2
    confirmDelete: (itemName = 'este elemento') => {
        return Swal.fire({
            title: '¿Estás seguro?',
            html: `Estás a punto de eliminar <strong>"${itemName}"</strong>.<br>Esta acción no se puede deshacer.`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc2626',
            cancelButtonColor: '#6b7280',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar',
            showClass: {
                popup: 'animate__animated animate__fadeInDown'
            },
            hideClass: {
                popup: 'animate__animated animate__fadeOutUp'
            }
        });
    },

    // Confirmación genérica
    confirm: (title, text) => {
        return Swal.fire({
            title: title,
            text: text,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#7f1d1d',
            cancelButtonColor: '#6b7280',
            confirmButtonText: 'Sí, continuar',
            cancelButtonText: 'Cancelar',
            showClass: {
                popup: 'animate__animated animate__fadeInDown'
            }
        });
    },

    // Loading/Cargando
    loading: (title = 'Cargando...', text = 'Por favor espera') => {
        Swal.fire({
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

    // Cerrar alerta actual
    close: () => {
        Swal.close();
    },

    // Toast notification con SweetAlert2
    toast: (message, type = 'success') => {
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

        Toast.fire({
            icon: type,
            title: message
        });
    }
};

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {

    // ========================================
    // SIDEBAR MOBILE TOGGLE
    // ========================================
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarMenu = document.getElementById('sidebarMenu');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    // Toggle del sidebar cuando se hace clic en el botón hamburguesa
    if (sidebarToggle && sidebarMenu && sidebarOverlay) {
        sidebarToggle.addEventListener('click', function () {
            sidebarMenu.classList.toggle('hidden');
            sidebarOverlay.classList.toggle('hidden');
        });

        // Cerrar sidebar cuando se hace clic en el overlay
        sidebarOverlay.addEventListener('click', function () {
            sidebarMenu.classList.add('hidden');
            sidebarOverlay.classList.add('hidden');
        });

        // Cerrar sidebar cuando se selecciona un enlace (solo en mobile)
        const sidebarLinks = sidebarMenu.querySelectorAll('a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function () {
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
    window.addEventListener('resize', function () {
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
    // CONFIRMACIÓN DE ELIMINACIÓN MEJORADA
    // ========================================
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    console.log('Botones de eliminar encontrados:', deleteButtons.length);

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            const itemName = this.getAttribute('data-confirm-delete') || 'este elemento';
            const form = this.closest('form');

            console.log('Botón clickeado:', itemName);
            console.log('Formulario encontrado:', form);
            console.log('Action del formulario:', form ? form.action : 'N/A');
            console.log('Method del formulario:', form ? form.method : 'N/A');

            if (!form) {
                console.error('No se encontró el formulario');
                AdminAlerts.error('Error', 'No se pudo encontrar el formulario');
                return;
            }

            AdminAlerts.confirmDelete(itemName).then((result) => {
                console.log('Resultado de confirmación:', result);
                if (result.isConfirmed) {
                    console.log('Usuario confirmó eliminación');
                    AdminAlerts.loading('Eliminando...', 'Por favor espera');

                    // Usar setTimeout para asegurar que el loading se muestre
                    setTimeout(() => {
                        console.log('Enviando formulario ahora...');
                        Swal.close(); // 👈 IMPORTANTE
                        form.requestSubmit(); // 👈 CLAVE
                    }, 100);
                } else {
                    console.log('Usuario canceló eliminación');
                }
            }).catch((error) => {
                console.error('Error en confirmDelete:', error);
            });
        });
    });

    // ========================================
    // MANEJO DE FORMULARIOS CON CONFIRMACIÓN
    // ========================================
    const confirmForms = document.querySelectorAll('[data-confirm-submit]');
    confirmForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const message = this.getAttribute('data-confirm-submit') || '¿Deseas continuar con esta acción?';

            AdminAlerts.confirm('Confirmar acción', message).then((result) => {
                if (result.isConfirmed) {
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
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            let firstInvalidField = null;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500', 'border-2');
                    if (!firstInvalidField) firstInvalidField = field;
                } else {
                    field.classList.remove('border-red-500', 'border-2');
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

        AdminAlerts.toast(text, type);

        // Remover el elemento del DOM
        message.remove();
    });

    // ========================================
    // CONFIRMACIÓN DE CAMBIO DE ESTADO
    // ========================================
    const statusButtons = document.querySelectorAll('[data-change-status]');
    statusButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const newStatus = this.getAttribute('data-change-status');
            const itemName = this.getAttribute('data-item-name') || 'este elemento';
            const form = this.closest('form');

            AdminAlerts.confirm('Cambiar estado', `¿Deseas cambiar el estado de ${itemName} a "${newStatus}"?`).then((result) => {
                if (result.isConfirmed) {
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
        input.addEventListener('change', function (e) {
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

                // Mostrar preview si existe un elemento con id 'image-preview'
                const preview = document.getElementById('image-preview');
                if (preview) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        preview.src = e.target.result;
                        preview.classList.remove('hidden');
                        AdminAlerts.toast('Imagen cargada correctamente', 'success');
                    };
                    reader.readAsDataURL(file);
                } else {
                    AdminAlerts.toast('Imagen seleccionada correctamente', 'success');
                }
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
            input.addEventListener('input', function () {
                clearTimeout(saveTimeout);

                // Mostrar indicador de "guardando..."
                const indicator = document.getElementById('save-indicator');
                if (indicator) {
                    indicator.textContent = '💾 Guardando...';
                    indicator.classList.remove('hidden');
                }

                saveTimeout = setTimeout(() => {
                    if (indicator) {
                        indicator.textContent = '✅ Guardado';
                        setTimeout(() => indicator.classList.add('hidden'), 2000);
                    }
                    AdminAlerts.toast('Cambios guardados automáticamente', 'success');
                }, 2000);
            });
        });
    });

    // ========================================
    // AUTO-CERRAR ALERTAS
    // ========================================
    const alerts = document.querySelectorAll('.alert-auto-close');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // ========================================
    // CONTADOR DE CARACTERES EN TEXTAREAS
    // ========================================
    const textareasWithCounter = document.querySelectorAll('textarea[data-max-length]');
    textareasWithCounter.forEach(textarea => {
        const maxLength = parseInt(textarea.getAttribute('data-max-length'));
        const counterId = textarea.getAttribute('data-counter-id');
        const counter = counterId ? document.getElementById(counterId) : null;

        if (counter) {
            const updateCounter = () => {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = `${remaining} caracteres restantes`;

                if (remaining < 0) {
                    counter.classList.add('text-red-600');
                    counter.classList.remove('text-gray-600');
                } else if (remaining < 50) {
                    counter.classList.add('text-yellow-600');
                    counter.classList.remove('text-gray-600', 'text-red-600');
                } else {
                    counter.classList.add('text-gray-600');
                    counter.classList.remove('text-yellow-600', 'text-red-600');
                }
            };

            textarea.addEventListener('input', updateCounter);
            updateCounter(); // Inicializar
        }
    });

    // ========================================
    // COPIAR AL PORTAPAPELES
    // ========================================
    const copyButtons = document.querySelectorAll('[data-copy-text]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function () {
            const textToCopy = this.getAttribute('data-copy-text');

            navigator.clipboard.writeText(textToCopy).then(() => {
                AdminAlerts.toast('Copiado al portapapeles', 'success');

                // Cambiar texto del botón temporalmente
                const originalText = this.textContent;
                this.textContent = '✓ Copiado';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            }).catch(() => {
                AdminAlerts.error('Error', 'No se pudo copiar al portapapeles');
            });
        });
    });

});

// ========================================
// EXPORTAR UTILIDADES GLOBALMENTE
// ========================================
window.AdminAlerts = AdminAlerts;
