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
