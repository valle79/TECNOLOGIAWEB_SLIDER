"""
Business logic services
"""
from typing import Dict, List, Optional
from flask import session
from models import Wine, Order
from config import Config


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
    def validate_cart() -> tuple:
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


class OrderService:
    """Service for processing orders"""

    @staticmethod
    def calculate_shipping(country: str) -> float:
        """Calculate shipping cost based on country"""
        is_international = country.lower() != Config.LOCAL_COUNTRY.lower()

        if is_international:
            return Config.INTERNATIONAL_SHIPPING_RATE
        else:
            return Config.LOCAL_SHIPPING_RATE

    @staticmethod
    def create_order_from_cart(customer_data: Dict, user_id: Optional[str] = None) -> Optional[str]:
        """
        Create an order from current cart

        Args:
            customer_data: Customer information
            user_id: Optional user ID if logged in

        Returns:
            Order ID if successful, None otherwise
        """
        # Validate cart
        is_valid, error_message = CartService.validate_cart()
        if not is_valid:
            raise ValueError(error_message)

        cart_items = CartService.get_cart_items()

        # Calculate totals
        subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
        shipping_cost = OrderService.calculate_shipping(customer_data['shipping_country'])
        total = subtotal + shipping_cost

        is_international = customer_data['shipping_country'].lower() != Config.LOCAL_COUNTRY.lower()

        # Prepare order data
        order_data = {
            'user_id': user_id,
            'customer_name': customer_data['customer_name'],
            'customer_email': customer_data['customer_email'],
            'customer_phone': customer_data.get('customer_phone'),
            'shipping_address': customer_data['shipping_address'],
            'shipping_city': customer_data['shipping_city'],
            'shipping_country': customer_data['shipping_country'],
            'is_international': is_international,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'total': total,
            'status': 'pending',
            'payment_method': customer_data.get('payment_method', 'pending'),
            'notes': customer_data.get('notes')
        }

        # Prepare order items
        items = []
        for cart_item in cart_items:
            items.append({
                'wine_id': cart_item['wine_id'],
                'wine_name': cart_item['name'],
                'wine_price': cart_item['price'],
                'quantity': cart_item['quantity'],
                'subtotal': cart_item['price'] * cart_item['quantity']
            })

        # Create order
        order_id = Order.create(order_data, items)

        if order_id:
            # Update stock for each item
            for item in items:
                Wine.update_stock(item['wine_id'], item['quantity'])

            # Clear cart
            CartService.clear_cart()

        return order_id

    @staticmethod
    def get_order_summary(order_id: str) -> Optional[Dict]:
        """Get order summary with formatted data"""
        order = Order.get_by_id(order_id)

        if not order:
            return None

        return {
            'order_id': order['id'],
            'customer_name': order['customer_name'],
            'customer_email': order['customer_email'],
            'customer_phone': order.get('customer_phone', ''),
            'shipping_address': order['shipping_address'],
            'shipping_city': order['shipping_city'],
            'shipping_country': order['shipping_country'],
            'is_international': order['is_international'],
            'subtotal': float(order['subtotal']),
            'shipping_cost': float(order['shipping_cost']),
            'total': float(order['total']),
            'status': order['status'],
            'payment_method': order.get('payment_method', ''),
            'notes': order.get('notes', ''),
            'order_items': order.get('items', []),
            'created_at': order['created_at']
        }
