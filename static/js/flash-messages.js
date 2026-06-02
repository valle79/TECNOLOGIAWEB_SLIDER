/**
 * Flash Messages Handler
 * Maneja la visualización de mensajes flash del servidor
 */

(function() {
    'use strict';
    
    /**
     * Procesa y muestra los mensajes flash
     * @param {Array} messages - Array de objetos {category: string, message: string}
     */
    function displayFlashMessages(messages) {
        if (!messages || messages.length === 0) return;
        
        // Esperar a que AdminAlerts esté disponible
        if (typeof AdminAlerts === 'undefined') {
            console.error('AdminAlerts no está disponible');
            return;
        }
        
        messages.forEach(function(msg) {
            const category = msg.category || 'info';
            const message = msg.message;
            
            switch(category) {
                case 'success':
                    AdminAlerts.toast(message, 'success');
                    break;
                case 'error':
                    AdminAlerts.toast(message, 'error');
                    break;
                case 'warning':
                    AdminAlerts.toast(message, 'warning');
                    break;
                default:
                    AdminAlerts.toast(message, 'info');
            }
        });
    }
    
    // Exportar función globalmente
    window.displayFlashMessages = displayFlashMessages;
    
})();
