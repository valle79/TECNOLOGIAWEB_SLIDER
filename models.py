"""
Database models for Wine E-commerce
"""
from typing import List, Dict, Optional
from database import Database
import bcrypt
import logging

logger = logging.getLogger(__name__)


class Wine:
    """Wine model for CRUD operations"""

    @staticmethod
    def get_all(filters: Optional[Dict] = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Get all wines with optional filters

        Args:
            filters: Dictionary with filter criteria (wine_type, country, min_price, max_price)
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of wine dictionaries
        """
        query = """
            SELECT id, name, wine_type, price, country, region, year,
                   grape_variety, alcohol_content, description, stock,
                   image_url, is_featured, created_at
            FROM wines
            WHERE 1=1
        """
        params = []

        if filters:
            if filters.get('wine_type'):
                query += " AND wine_type = %s"
                params.append(filters['wine_type'])

            if filters.get('country'):
                query += " AND country = %s"
                params.append(filters['country'])

            if filters.get('min_price'):
                query += " AND price >= %s"
                params.append(filters['min_price'])

            if filters.get('max_price'):
                query += " AND price <= %s"
                params.append(filters['max_price'])

            if filters.get('search'):
                query += " AND (name ILIKE %s OR description ILIKE %s)"
                search_term = f"%{filters['search']}%"
                params.extend([search_term, search_term])

        query += " ORDER BY is_featured DESC, created_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching wines: {e}")
            return []

    @staticmethod
    def get_by_id(wine_id: str) -> Optional[Dict]:
        """Get a wine by ID"""
        query = """
            SELECT id, name, wine_type, price, country, region, year,
                   grape_variety, alcohol_content, description, stock,
                   image_url, is_featured, created_at
            FROM wines
            WHERE id = %s
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (wine_id,))
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching wine {wine_id}: {e}")
            return None

    @staticmethod
    def get_featured(limit: int = 6) -> List[Dict]:
        """Get featured wines"""
        query = """
            SELECT id, name, wine_type, price, country, region, year,
                   grape_variety, alcohol_content, description, stock,
                   image_url, is_featured, created_at
            FROM wines
            WHERE is_featured = TRUE AND stock > 0
            ORDER BY created_at DESC
            LIMIT %s
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (limit,))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching featured wines: {e}")
            return []

    @staticmethod
    def create(wine_data: Dict) -> Optional[str]:
        """Create a new wine"""
        query = """
            INSERT INTO wines (name, wine_type, price, country, region, year,
                             grape_variety, alcohol_content, description, stock, image_url, is_featured)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            wine_data['name'],
            wine_data['wine_type'],
            wine_data['price'],
            wine_data['country'],
            wine_data.get('region'),
            wine_data.get('year'),
            wine_data.get('grape_variety'),
            wine_data.get('alcohol_content'),
            wine_data.get('description'),
            wine_data.get('stock', 0),
            wine_data.get('image_url'),
            wine_data.get('is_featured', False)
        )

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, params)

                # Get the last inserted ID
                cursor.execute("SELECT id FROM wines WHERE id = LAST_INSERT_ID()")
                result = cursor.fetchone()
                return result['id'] if result else None
        except Exception as e:
            logger.error(f"Error creating wine: {e}")
            return None

    @staticmethod
    def update(wine_id: str, wine_data: Dict) -> bool:
        """Update a wine"""
        query = """
            UPDATE wines
            SET name = %s, wine_type = %s, price = %s, country = %s,
                region = %s, year = %s, grape_variety = %s, alcohol_content = %s,
                description = %s, stock = %s, image_url = %s, is_featured = %s
            WHERE id = %s
        """

        params = (
            wine_data['name'],
            wine_data['wine_type'],
            wine_data['price'],
            wine_data['country'],
            wine_data.get('region'),
            wine_data.get('year'),
            wine_data.get('grape_variety'),
            wine_data.get('alcohol_content'),
            wine_data.get('description'),
            wine_data.get('stock', 0),
            wine_data.get('image_url'),
            wine_data.get('is_featured', False),
            wine_id
        )

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating wine {wine_id}: {e}")
            return False

    @staticmethod
    def delete(wine_id: str) -> bool:
        """Delete a wine"""
        query = "DELETE FROM wines WHERE id = %s"

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (wine_id,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting wine {wine_id}: {e}")
            return False

    @staticmethod
    def update_stock(wine_id: str, quantity: int) -> bool:
        """Update wine stock"""
        query = """
            UPDATE wines
            SET stock = stock - %s
            WHERE id = %s AND stock >= %s
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (quantity, wine_id, quantity))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating stock for wine {wine_id}: {e}")
            return False

    @staticmethod
    def get_wine_types() -> List[str]:
        """Get all unique wine types"""
        query = "SELECT DISTINCT wine_type FROM wines ORDER BY wine_type"

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query)
                return [row['wine_type'] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching wine types: {e}")
            return []

    @staticmethod
    def get_countries() -> List[str]:
        """Get all unique countries"""
        query = "SELECT DISTINCT country FROM wines ORDER BY country"

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query)
                return [row['country'] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching countries: {e}")
            return []


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

                # Get the UUID of the last inserted order
                cursor.execute("""
                    SELECT id FROM orders
                    WHERE customer_email = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (order_data['customer_email'],))

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
            import traceback
            logger.error(traceback.format_exc())
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


class User:
    """User model for authentication and user management"""

    @staticmethod
    def create(email: str, password: str, full_name: str, phone: str = None) -> Optional[str]:
        """Create a new user"""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        query = """
            INSERT INTO users (email, password_hash, full_name, phone)
            VALUES (%s, %s, %s, %s)
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (email, password_hash, full_name, phone))

                # Get the last inserted ID
                cursor.execute("SELECT id FROM users WHERE id = LAST_INSERT_ID()")
                result = cursor.fetchone()
                return result['id'] if result else None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        """Get user by email"""
        query = """
            SELECT id, email, password_hash, full_name, phone, is_admin, created_at
            FROM users
            WHERE email = %s
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching user by email: {e}")
            return None

    @staticmethod
    def get_by_id(user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        query = """
            SELECT id, email, full_name, phone, is_admin, created_at
            FROM users
            WHERE id = %s
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching user by ID: {e}")
            return None

    @staticmethod
    def verify_password(email: str, password: str) -> Optional[Dict]:
        """Verify user password and return user data if valid"""
        user = User.get_by_email(email)

        if not user:
            return None

        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Remove password hash from returned data
            user.pop('password_hash', None)
            return user

        return None

    @staticmethod
    def update(user_id: str, user_data: Dict) -> bool:
        """Update user information"""
        query = """
            UPDATE users
            SET full_name = %s, phone = %s
            WHERE id = %s
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (
                    user_data['full_name'],
                    user_data.get('phone'),
                    user_id
                ))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            return False

    @staticmethod
    def change_password(user_id: str, new_password: str) -> bool:
        """Change user password"""
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        query = "UPDATE users SET password_hash = %s WHERE id = %s"

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (password_hash, user_id))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error changing password for user {user_id}: {e}")
            return False
