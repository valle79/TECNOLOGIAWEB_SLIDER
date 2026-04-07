"""
Wine model for database operations
"""
from typing import List, Dict, Optional
from .database import Database
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
            RETURNING id
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
