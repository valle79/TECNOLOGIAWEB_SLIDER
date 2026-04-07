"""
Order processing service
"""
from typing import Dict, List, Optional
from models.order import Order
from models.wine import Wine
from services.cart_service import CartService
from config import Config


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
            'shipping_address': order['shipping_address'],
            'shipping_city': order['shipping_city'],
            'shipping_country': order['shipping_country'],
            'is_international': order['is_international'],
            'subtotal': float(order['subtotal']),
            'shipping_cost': float(order['shipping_cost']),
            'total': float(order['total']),
            'status': order['status'],
            'items': order['items'],
            'created_at': order['created_at']
        }
