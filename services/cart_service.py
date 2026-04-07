"""
Shopping cart service
"""
from typing import Dict, List
from flask import session
from models.wine import Wine


class CartService:
    """Service for managing shopping cart"""
    
    CART_SESSION_KEY = 'cart'
    
    @staticmethod
    def get_cart() -> Dict:
        """Get current cart from session"""
        return session.get(CartService.CART_SESSION_KEY, {})
    
    @staticmethod
    def add_item(wine_id: str, quantity: int = 1) -> bool:
        """
        Add item to cart
        
        Args:
            wine_id: Wine ID to add
            quantity: Quantity to add
            
        Returns:
            True if successful, False otherwise
        """
        # Validate wine exists and has stock
        wine = Wine.get_by_id(wine_id)
        if not wine or wine['stock'] < quantity:
            return False
        
        cart = CartService.get_cart()
        
        if wine_id in cart:
            cart[wine_id]['quantity'] += quantity
        else:
            cart[wine_id] = {
                'wine_id': wine_id,
                'name': wine['name'],
                'price': float(wine['price']),
                'image_url': wine['image_url'],
                'quantity': quantity,
                'stock': wine['stock']
            }
        
        # Ensure quantity doesn't exceed stock
        if cart[wine_id]['quantity'] > wine['stock']:
            cart[wine_id]['quantity'] = wine['stock']
        
        session[CartService.CART_SESSION_KEY] = cart
        session.modified = True
        return True
    
    @staticmethod
    def update_item(wine_id: str, quantity: int) -> bool:
        """Update item quantity in cart"""
        if quantity < 1:
            return CartService.remove_item(wine_id)
        
        cart = CartService.get_cart()
        
        if wine_id not in cart:
            return False
        
        # Validate stock
        wine = Wine.get_by_id(wine_id)
        if not wine or wine['stock'] < quantity:
            return False
        
        cart[wine_id]['quantity'] = quantity
        session[CartService.CART_SESSION_KEY] = cart
        session.modified = True
        return True
    
    @staticmethod
    def remove_item(wine_id: str) -> bool:
        """Remove item from cart"""
        cart = CartService.get_cart()
        
        if wine_id in cart:
            del cart[wine_id]
            session[CartService.CART_SESSION_KEY] = cart
            session.modified = True
            return True
        
        return False
    
    @staticmethod
    def clear_cart():
        """Clear all items from cart"""
        session[CartService.CART_SESSION_KEY] = {}
        session.modified = True
    
    @staticmethod
    def get_cart_items() -> List[Dict]:
        """Get cart items as a list"""
        cart = CartService.get_cart()
        return list(cart.values())
    
    @staticmethod
    def get_cart_total() -> float:
        """Calculate cart total"""
        cart = CartService.get_cart()
        return sum(item['price'] * item['quantity'] for item in cart.values())
    
    @staticmethod
    def get_cart_count() -> int:
        """Get total number of items in cart"""
        cart = CartService.get_cart()
        return sum(item['quantity'] for item in cart.values())
    
    @staticmethod
    def validate_cart() -> tuple[bool, str]:
        """
        Validate cart items against current stock
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        cart = CartService.get_cart()
        
        if not cart:
            return False, "El carrito está vacío"
        
        for wine_id, item in cart.items():
            wine = Wine.get_by_id(wine_id)
            
            if not wine:
                return False, f"El vino '{item['name']}' ya no está disponible"
            
            if wine['stock'] < item['quantity']:
                return False, f"Stock insuficiente para '{item['name']}'. Disponible: {wine['stock']}"
        
        return True, ""
