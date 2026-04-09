"""
Main page routes
"""
from flask import Blueprint, render_template
from models import Wine
from services import CartService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page with featured wines"""
    featured_wines = Wine.get_featured(limit=6)
    cart_count = CartService.get_cart_count()

    return render_template('index.html',
                         featured_wines=featured_wines,
                         cart_count=cart_count)


@main_bp.route('/about')
def about():
    """About page"""
    cart_count = CartService.get_cart_count()
    return render_template('about.html', cart_count=cart_count)


@main_bp.route('/contact')
def contact():
    """Contact page"""
    cart_count = CartService.get_cart_count()
    return render_template('contact.html', cart_count=cart_count)
