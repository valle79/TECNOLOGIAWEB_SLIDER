"""
Order model for database operations
"""
from typing import List, Dict, Optional
from .database import Database
import logging

logger = logging.getLogger(__name__)


class Order:
    """Order model for CRUD operations"""
    
    @staticmethod
    def create(order_data: Dict, items: List[Dict]) -> Optional[str]:
        """
        Create a new order with items
        
        Args:
            order_data: Dictionary with order information
            items: List of order items
            
        Returns:
            Order ID if successful, None otherwise
        """
        order_query = """
            INSERT INTO orders (
                user_id, customer_name, customer_email, customer_phone,
                shipping_address, shipping_city, shipping_country,
                is_international, subtotal, shipping_cost, total,
                status, payment_method, notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        item_query = """
            INSERT INTO order_items (
                order_id, wine_id, wine_name, wine_price, quantity, subtotal
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            with Database.get_cursor() as cursor:
                # Insert order
                cursor.execute(order_query, (
                    order_data.get('user_id'),
                    order_data['customer_name'],
                    order_data['customer_email'],
                    order_data.get('customer_phone'),
                    order_data['shipping_address'],
                    order_data['shipping_city'],
                    order_data['shipping_country'],
                    order_data['is_international'],
                    order_data['subtotal'],
                    order_data['shipping_cost'],
                    order_data['total'],
                    order_data.get('status', 'pending'),
                    order_data.get('payment_method'),
                    order_data.get('notes')
                ))
                
                result = cursor.fetchone()
                if not result:
                    return None
                
                order_id = result['id']
                
                # Insert order items
                for item in items:
                    cursor.execute(item_query, (
                        order_id,
                        item['wine_id'],
                        item['wine_name'],
                        item['wine_price'],
                        item['quantity'],
                        item['subtotal']
                    ))
                
                return order_id
                
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None
    
    @staticmethod
    def get_by_id(order_id: str) -> Optional[Dict]:
        """Get an order by ID with its items"""
        order_query = """
            SELECT id, user_id, customer_name, customer_email, customer_phone,
                   shipping_address, shipping_city, shipping_country,
                   is_international, subtotal, shipping_cost, total,
                   status, payment_method, notes, created_at, updated_at
            FROM orders
            WHERE id = %s
        """
        
        items_query = """
            SELECT id, wine_id, wine_name, wine_price, quantity, subtotal
            FROM order_items
            WHERE order_id = %s
        """
        
        try:
            with Database.get_cursor() as cursor:
                cursor.execute(order_query, (order_id,))
                order = cursor.fetchone()
                
                if not order:
                    return None
                
                cursor.execute(items_query, (order_id,))
                order['items'] = cursor.fetchall()
                
                return order
                
        except Exception as e:
            logger.error(f"Error fetching order {order_id}: {e}")
            return None
    
    @staticmethod
    def get_all(filters: Optional[Dict] = None, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get all orders with optional filters"""
        query = """
            SELECT id, user_id, customer_name, customer_email,
                   shipping_country, is_international, total,
                   status, created_at
            FROM orders
            WHERE 1=1
        """
        params = []
        
        if filters:
            if filters.get('status'):
                query += " AND status = %s"
                params.append(filters['status'])
            
            if filters.get('is_international') is not None:
                query += " AND is_international = %s"
                params.append(filters['is_international'])
            
            if filters.get('user_id'):
                query += " AND user_id = %s"
                params.append(filters['user_id'])
        
        query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return []
    
    @staticmethod
    def update_status(order_id: str, status: str) -> bool:
        """Update order status"""
        query = "UPDATE orders SET status = %s WHERE id = %s"
        
        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (status, order_id))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating order status {order_id}: {e}")
            return False
    
    @staticmethod
    def get_statistics() -> Dict:
        """Get order statistics"""
        query = """
            SELECT 
                COUNT(*) as total_orders,
                COALESCE(SUM(total), 0) as total_revenue,
                SUM(CASE WHEN is_international THEN 1 ELSE 0 END) as international_orders,
                COALESCE(SUM(CASE WHEN is_international THEN total ELSE 0 END), 0) as international_revenue,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_orders
            FROM orders
            WHERE status != 'cancelled'
        """
        
        wines_query = "SELECT COUNT(*) as total_wines FROM wines"
        
        try:
            with Database.get_cursor() as cursor:
                # Get order stats
                cursor.execute(query)
                stats = cursor.fetchone() or {}
                
                # Get wine count
                cursor.execute(wines_query)
                wine_stats = cursor.fetchone() or {}
                
                # Merge stats and ensure all values are not None
                result = {
                    'total_orders': stats.get('total_orders', 0) or 0,
                    'total_revenue': float(stats.get('total_revenue', 0) or 0),
                    'international_orders': stats.get('international_orders', 0) or 0,
                    'international_revenue': float(stats.get('international_revenue', 0) or 0),
                    'pending_orders': stats.get('pending_orders', 0) or 0,
                    'total_wines': wine_stats.get('total_wines', 0) or 0
                }
                
                return result
        except Exception as e:
            logger.error(f"Error fetching order statistics: {e}")
            return {
                'total_orders': 0,
                'total_revenue': 0.0,
                'international_orders': 0,
                'international_revenue': 0.0,
                'pending_orders': 0,
                'total_wines': 0
            }
