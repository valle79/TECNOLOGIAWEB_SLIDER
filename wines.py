"""
Wine catalog routes
"""
from flask import Blueprint, render_template, request, jsonify
from models import Wine
from services import CartService

wine_bp = Blueprint('wine', __name__, url_prefix='/wines')


@wine_bp.route('/')
def catalog():
    """Wine catalog page with filters"""
    # Get filter parameters
    wine_type = request.args.get('type')
    country = request.args.get('country')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)

    # Build filters
    filters = {}
    if wine_type:
        filters['wine_type'] = wine_type
    if country:
        filters['country'] = country
    if min_price:
        filters['min_price'] = min_price
    if max_price:
        filters['max_price'] = max_price
    if search:
        filters['search'] = search

    # Get wines
    per_page = 12
    offset = (page - 1) * per_page
    wines = Wine.get_all(filters=filters, limit=per_page, offset=offset)

    # Get filter options
    wine_types = Wine.get_wine_types()
    countries = Wine.get_countries()

    cart_count = CartService.get_cart_count()

    return render_template('catalog.html',
                         wines=wines,
                         wine_types=wine_types,
                         countries=countries,
                         current_filters=filters,
                         page=page,
                         cart_count=cart_count)


@wine_bp.route('/<wine_id>')
def detail(wine_id):
    """Wine detail page"""
    wine = Wine.get_by_id(wine_id)

    if not wine:
        return render_template('404.html'), 404

    cart_count = CartService.get_cart_count()

    return render_template('wine_detail.html',
                         wine=wine,
                         cart_count=cart_count)


@wine_bp.route('/api/wines')
def api_wines():
    """API endpoint to get wines"""
    filters = {}

    if request.args.get('type'):
        filters['wine_type'] = request.args.get('type')
    if request.args.get('country'):
        filters['country'] = request.args.get('country')
    if request.args.get('min_price'):
        filters['min_price'] = float(request.args.get('min_price'))
    if request.args.get('max_price'):
        filters['max_price'] = float(request.args.get('max_price'))

    wines = Wine.get_all(filters=filters)

    return jsonify({
        'success': True,
        'wines': wines
    })


@wine_bp.route('/api/wines/<wine_id>')
def api_wine_detail(wine_id):
    """API endpoint to get wine details"""
    wine = Wine.get_by_id(wine_id)

    if not wine:
        return jsonify({
            'success': False,
            'error': 'Wine not found'
        }), 404

    return jsonify({
        'success': True,
        'wine': wine
    })
