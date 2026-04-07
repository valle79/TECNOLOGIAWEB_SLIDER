"""
Database connection and management for MySQL
"""
import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager with connection pooling for MySQL"""
    
    _pool = None
    
    @classmethod
    def initialize(cls, db_config):
        """
        Initialize the connection pool
        
        Args:
            db_config: Dictionary with database configuration
                - host: Database host
                - port: Database port
                - user: Database user
                - password: Database password
                - database: Database name
        """
        try:
            cls._pool = pooling.MySQLConnectionPool(
                pool_name="wine_pool",
                pool_size=10,
                pool_reset_session=True,
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                autocommit=False
            )
            logger.info("MySQL connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    @classmethod
    @contextmanager
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._pool is None:
            raise Exception("Database pool not initialized. Call Database.initialize() first.")
        
        conn = cls._pool.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    @classmethod
    @contextmanager
    def get_cursor(cls, dictionary=True):
        """Get a cursor from a pooled connection"""
        with cls.get_connection() as conn:
            cursor = conn.cursor(dictionary=dictionary)
            try:
                yield cursor
            finally:
                cursor.close()
    
    @classmethod
    def close_all(cls):
        """Close all connections in the pool"""
        if cls._pool:
            # MySQL connector doesn't have closeall, connections are managed automatically
            cls._pool = None
            logger.info("Database connection pool closed")
