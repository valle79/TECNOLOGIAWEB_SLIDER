// Main JavaScript for Wine E-commerce

// Cart functionality
const CartManager = {
    // Add item to cart via AJAX
    addToCart: async function(wineId, quantity = 1) {
        try {
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
            
            if (data.success) {
                this.updateCartCount(data.cart_count);
                this.showNotification('Producto agregado al carrito', 'success');
            } else {
                this.showNotification(data.error || 'Error al agregar producto', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error al agregar producto', 'error');
        }
    },
    
    // Update cart item quantity
    updateQuantity: async function(wineId, quantity) {
        try {
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
            
            if (data.success) {
                this.updateCartCount(data.cart_count);
                this.updateCartTotal(data.cart_total);
                return true;
            } else {
                this.showNotification(data.error || 'Error al actualizar carrito', 'error');
                return false;
            }
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error al actualizar carrito', 'error');
            return false;
        }
    },
    
    // Remove item from cart
    removeItem: async function(wineId) {
        if (!confirm('¿Estás seguro de eliminar este producto?')) {
            return;
        }
        
        try {
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
            
            if (data.success) {
                this.updateCartCount(data.cart_count);
                this.updateCartTotal(data.cart_total);
                // Remove item from DOM
                const itemElement = document.querySelector(`[data-wine-id="${wineId}"]`);
                if (itemElement) {
                    itemElement.remove();
                }
                this.showNotification('Producto eliminado', 'success');
            } else {
                this.showNotification(data.error || 'Error al eliminar producto', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error al eliminar producto', 'error');
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
    
    // Show notification
    showNotification: function(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-20 right-4 z-50 p-4 rounded-lg shadow-lg ${
            type === 'success' ? 'bg-green-500' :
            type === 'error' ? 'bg-red-500' :
            'bg-blue-500'
        } text-white`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
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
            CartManager.updateQuantity(wineId, quantity);
        });
    });
    
    // Remove buttons in cart
    const removeButtons = document.querySelectorAll('.remove-item-btn');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const wineId = this.dataset.wineId;
            CartManager.removeItem(wineId);
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
