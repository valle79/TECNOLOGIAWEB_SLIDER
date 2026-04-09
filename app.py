"""
Wine E-commerce Application

Professional e-commerce system for wine sales in Peru and international export.
Built with Flask, MySQL, and modern web technologies.
"""

from flask import Flask
from config import config
from database import Database
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize database
    try:
        db_config = {
            'host': app.config['DB_HOST'],
            'port': app.config['DB_PORT'],
            'user': app.config['DB_USER'],
            'password': app.config['DB_PASSWORD'],
            'database': app.config['DB_NAME']
        }
        Database.initialize(db_config)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    # Register blueprints
    from main import main_bp
    from wines import wine_bp
    from cart import cart_bp
    from orders import order_bp
    from auth import auth_bp
    from admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(wine_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        from services import CartService
        return render_template('404.html', cart_count=CartService.get_cart_count()), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        from services import CartService
        logger.error(f"Internal server error: {error}")
        return render_template('500.html', cart_count=CartService.get_cart_count()), 500
    
    # Context processor for global template variables
    @app.context_processor
    def inject_globals():
        from services import CartService
        from flask import session
        return {
            'cart_count': CartService.get_cart_count(),
            'is_logged_in': 'user_id' in session,
            'is_admin': session.get('is_admin', False),
            'user_name': session.get('user_name')
        }
    
    # Cleanup on shutdown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        pass
    
    return app

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(env)
    
    # Run server
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(env == 'development'))
