"""
User model for database operations
"""
from typing import Optional, Dict
from .database import Database
import bcrypt
import logging

logger = logging.getLogger(__name__)


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
