/**
 * Checkout page functionality
 * Handles shipping cost calculation based on country selection
 */

document.addEventListener('DOMContentLoaded', function() {
    const countrySelect = document.getElementById('shipping_country');
    const configElement = document.getElementById('checkout-config');
    
    if (countrySelect && configElement) {
        // Get configuration values from data attributes
        const cartTotal = parseFloat(configElement.dataset.cartTotal);
        const localShipping = parseFloat(configElement.dataset.localShipping);
        const intlShipping = parseFloat(configElement.dataset.intlShipping);
        
        // Calculate shipping on country change
        countrySelect.addEventListener('change', function() {
            const shipping = (this.value === 'Peru') ? localShipping : intlShipping;
            const total = cartTotal + shipping;
            
            document.getElementById('shipping-cost').textContent = 'S/ ' + shipping.toFixed(2);
            document.getElementById('total-cost').textContent = 'S/ ' + total.toFixed(2);
        });
        
        // Initialize shipping cost on page load
        const initialShipping = (countrySelect.value === 'Peru') ? localShipping : intlShipping;
        const initialTotal = cartTotal + initialShipping;
        document.getElementById('shipping-cost').textContent = 'S/ ' + initialShipping.toFixed(2);
        document.getElementById('total-cost').textContent = 'S/ ' + initialTotal.toFixed(2);
    }
});

// ========================================
// VALIDACIÓN Y CONFIRMACIÓN DE CHECKOUT
// ========================================
function handleCheckoutSubmit(event) {
    event.preventDefault();
    const form = event.target;
    
    // Validar campos requeridos
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    let firstInvalidField = null;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('border-red-500', 'ring-2', 'ring-red-500');
            if (!firstInvalidField) firstInvalidField = field;
        } else {
            field.classList.remove('border-red-500', 'ring-2', 'ring-red-500');
        }
    });
    
    if (!isValid) {
        if (typeof Alerts !== 'undefined') {
            Alerts.error('Campos incompletos', 'Por favor completa todos los campos requeridos');
        } else {
            alert('Por favor completa todos los campos requeridos');
        }
        
        if (firstInvalidField) {
            firstInvalidField.focus();
            firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return false;
    }
    
    // Validar email
    const emailField = form.querySelector('#customer_email');
    if (emailField) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value)) {
            if (typeof Alerts !== 'undefined') {
                Alerts.error('Email inválido', 'Por favor ingresa un email válido');
            } else {
                alert('Por favor ingresa un email válido');
            }
            emailField.focus();
            return false;
        }
    }
    
    // Validar teléfono
    const phoneField = form.querySelector('#customer_phone');
    if (phoneField && phoneField.value.length < 6) {
        if (typeof Alerts !== 'undefined') {
            Alerts.error('Teléfono inválido', 'Por favor ingresa un número de teléfono válido');
        } else {
            alert('Por favor ingresa un número de teléfono válido');
        }
        phoneField.focus();
        return false;
    }
    
    // Confirmación final
    if (typeof Alerts !== 'undefined') {
        Alerts.confirm(
            '¿Confirmar pedido?',
            'Estás a punto de realizar tu pedido. ¿Deseas continuar?',
            'Sí, realizar pedido',
            'Revisar datos'
        ).then((result) => {
            if (result.isConfirmed) {
                Alerts.loading('Procesando tu pedido...', 'Por favor espera un momento');
                form.submit();
            }
        });
    } else {
        if (confirm('¿Confirmar pedido?')) {
            form.submit();
        }
    }
    
    return false;
}
