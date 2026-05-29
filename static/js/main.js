// Main JavaScript for Wine E-commerce

// ========================================
// CONFIGURACIÓN DE SWEETALERT2
// ========================================
const SwalConfig = {
    customClass: {
        popup: 'rounded-xl shadow-2xl',
        title: 'text-2xl font-bold',
        confirmButton: 'bg-red-900 hover:bg-red-800 text-white font-bold py-2 px-6 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl',
        cancelButton: 'bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded-lg transition-all duration-200 ml-2'
    },
    buttonsStyling: false
};

// ========================================
// UTILIDADES DE ALERTAS
// ========================================
const Alerts = {
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

    error: (title, text = '') => {
        return Swal.fire({
            ...SwalConfig,
            icon: 'error',
            title: title,
            text: text,
            confirmButtonText: 'Entendido'
        });
    },

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

// Cart functionality
const CartManager = {
    // Add item to cart via AJAX
    addToCart: async function(wineId, quantity = 1) {
        try {
            Alerts.loading('Agregando al carrito...', 'Por favor espera');
            
            const response = await fetch('/cart/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    wine_id: wineId,
                    quantity: quantity
                })
            });
            
            const data = await response.json();
            
            Swal.close();
            
            if (data.success) {
                this.updateCartCount(data.cart_count);
                Alerts.toast('¡Producto agregado al carrito!', 'success');
            } else {
                Alerts.error('Error', data.error || 'No se pudo agregar el producto');
            }
        } catch (error) {
            console.error('Error:', error);
            Swal.close();
            Alerts.error('Error de conexión', 'No se pudo agregar el producto al carrito');
        }
    },
    
    // Update cart item quantity
    updateQuantity: async function(wineId, quantity) {
        try {
            Alerts.loading('Actualizando cantidad...', 'Por favor espera');
            
            const response = await fetch('/cart/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    wine_id: wineId,
                    quantity: quantity
                })
            });
            
            const data = await response.json();
            
            Swal.close();
            
            if (data.success) {
                this.updateCartCount(data.cart_count);
                this.updateCartTotal(data.cart_total);
                Alerts.toast('Cantidad actualizada', 'success');
                
                // Recargar la página para actualizar los totales
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
                
                return true;
            } else {
                Alerts.error('Error', data.error || 'No se pudo actualizar la cantidad');
                return false;
            }
        } catch (error) {
            console.error('Error:', error);
            Swal.close();
            Alerts.error('Error de conexión', 'No se pudo actualizar el carrito');
            return false;
        }
    },
    
    // Remove item from cart
    removeItem: async function(wineId, wineName = 'este producto') {
        const result = await Alerts.confirm(
            '¿Eliminar producto?',
            `¿Estás seguro de eliminar "${wineName}" del carrito?`,
            'Sí, eliminar',
            'Cancelar'
        );
        
        if (!result.isConfirmed) {
            return;
        }
        
        try {
            Alerts.loading('Eliminando producto...', 'Por favor espera');
            
            const response = await fetch('/cart/remove', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    wine_id: wineId
                })
            });
            
            const data = await response.json();
            
            Swal.close();
            
            if (data.success) {
                this.updateCartCount(data.cart_count);
                this.updateCartTotal(data.cart_total);
                
                // Remove item from DOM
                const itemElement = document.querySelector(`[data-wine-id="${wineId}"]`);
                if (itemElement) {
                    itemElement.style.opacity = '0';
                    itemElement.style.transform = 'translateX(-100%)';
                    itemElement.style.transition = 'all 0.3s ease';
                    setTimeout(() => itemElement.remove(), 300);
                }
                
                Alerts.toast('Producto eliminado del carrito', 'success');
                
                // Si no quedan items, recargar la página
                if (data.cart_count === 0) {
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                }
            } else {
                Alerts.error('Error', data.error || 'No se pudo eliminar el producto');
            }
        } catch (error) {
            console.error('Error:', error);
            Swal.close();
            Alerts.error('Error de conexión', 'No se pudo eliminar el producto');
        }
    },
    
    // Update cart count in navbar
    updateCartCount: function(count) {
        const cartCountElements = document.querySelectorAll('.cart-count');
        cartCountElements.forEach(el => {
            el.textContent = count;
            if (count > 0) {
                el.classList.remove('hidden');
            } else {
                el.classList.add('hidden');
            }
        });
    },
    
    // Update cart total
    updateCartTotal: function(total) {
        const cartTotalElements = document.querySelectorAll('.cart-total');
        cartTotalElements.forEach(el => {
            el.textContent = `S/ ${total.toFixed(2)}`;
        });
    },
    
    // Show notification (deprecated - usar Alerts.toast)
    showNotification: function(message, type = 'info') {
        if (type === 'success') {
            Alerts.toast(message, 'success');
        } else if (type === 'error') {
            Alerts.toast(message, 'error');
        } else {
            Alerts.toast(message, 'info');
        }
    }
};

// Checkout functionality
const CheckoutManager = {
    // Calculate shipping based on country
    calculateShipping: async function(country) {
        try {
            const response = await fetch('/orders/api/calculate-shipping', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    country: country
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateShippingCost(data.shipping_cost);
                this.updateTotal(data.total);
            }
        } catch (error) {
            console.error('Error calculating shipping:', error);
        }
    },
    
    // Update shipping cost display
    updateShippingCost: function(cost) {
        const shippingElements = document.querySelectorAll('.shipping-cost');
        shippingElements.forEach(el => {
            el.textContent = `S/ ${cost.toFixed(2)}`;
        });
    },
    
    // Update total display
    updateTotal: function(total) {
        const totalElements = document.querySelectorAll('.order-total');
        totalElements.forEach(el => {
            el.textContent = `S/ ${total.toFixed(2)}`;
        });
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Country selector for shipping calculation
    const countrySelect = document.getElementById('shipping_country');
    if (countrySelect) {
        countrySelect.addEventListener('change', function() {
            CheckoutManager.calculateShipping(this.value);
        });
    }
    
    // Quantity inputs in cart
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const wineId = this.dataset.wineId;
            const quantity = parseInt(this.value);
            const maxStock = parseInt(this.max);
            
            if (quantity > maxStock) {
                Alerts.warning('Stock insuficiente', `Solo hay ${maxStock} unidades disponibles`);
                this.value = maxStock;
                return;
            }
            
            if (quantity < 1) {
                this.value = 1;
                return;
            }
            
            CartManager.updateQuantity(wineId, quantity);
        });
    });
    
    // Remove buttons in cart
    const removeButtons = document.querySelectorAll('.remove-item-btn');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const wineId = this.dataset.wineId;
            const wineName = this.dataset.wineName || 'este producto';
            CartManager.removeItem(wineId, wineName);
        });
    });
    
    // Mobile menu toggle - PROFESIONAL Y ROBUSTO
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        // Click en el botón hamburguesa
        mobileMenuButton.addEventListener('click', function(e) {
            e.stopPropagation();
            const isHidden = mobileMenu.classList.contains('hidden');
            
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
                document.body.style.overflow = 'hidden'; // Prevenir scroll
            } else {
                mobileMenu.classList.add('hidden');
                document.body.style.overflow = 'auto';
            }
        });
        
        // Cerrar menú al hacer click en un enlace
        const mobileMenuLinks = mobileMenu.querySelectorAll('a, button');
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
                document.body.style.overflow = 'auto';
            });
        });
        
        // Cerrar menú al hacer click fuera
        document.addEventListener('click', function(e) {
            if (!mobileMenuButton.contains(e.target) && !mobileMenu.contains(e.target)) {
                mobileMenu.classList.add('hidden');
                document.body.style.overflow = 'auto';
            }
        });
        
        // Cerrar menú con tecla ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                mobileMenu.classList.add('hidden');
                document.body.style.overflow = 'auto';
            }
        });
    }
    
    // Mobile filter toggle
    const filterToggle = document.getElementById('filter-toggle');
    const filterPanel = document.getElementById('filter-panel');
    if (filterToggle && filterPanel) {
        filterToggle.addEventListener('click', function() {
            filterPanel.classList.toggle('hidden');
        });
    }
});

// Export for use in other scripts
window.CartManager = CartManager;
window.CheckoutManager = CheckoutManager;
window.Alerts = Alerts;
