"""
Shopping cart routes
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from services import CartService

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('/')
def view_cart():
    """View shopping cart"""
    cart_items = CartService.get_cart_items()
    cart_total = CartService.get_cart_total()
    cart_count = CartService.get_cart_count()

    return render_template('cart.html',
                         cart_items=cart_items,
                         cart_total=cart_total,
                         cart_count=cart_count)


@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json() if request.is_json else request.form

    wine_id = data.get('wine_id')
    quantity = int(data.get('quantity', 1))

    if not wine_id:
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'Wine ID is required'
            }), 400
        flash('Error: ID de vino requerido', 'error')
        return redirect(request.referrer or url_for('main.index'))

    success = CartService.add_item(wine_id, quantity)

    if request.is_json:
        if success:
            return jsonify({
                'success': True,
                'cart_count': CartService.get_cart_count(),
                'cart_total': CartService.get_cart_total()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el producto al carrito'
            }), 400
    else:
        if success:
            flash('Producto agregado al carrito', 'success')
        else:
            flash('No se pudo agregar el producto al carrito', 'error')
        return redirect(request.referrer or url_for('main.index'))


@cart_bp.route('/update', methods=['POST'])
def update_cart():
    """Update cart item quantity"""
    data = request.get_json() if request.is_json else request.form

    wine_id = data.get('wine_id')
    quantity = int(data.get('quantity', 1))

    if not wine_id:
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'Wine ID is required'
            }), 400
        flash('Error: ID de vino requerido', 'error')
        return redirect(url_for('cart.view_cart'))

    success = CartService.update_item(wine_id, quantity)

    if request.is_json:
        if success:
            return jsonify({
                'success': True,
                'cart_count': CartService.get_cart_count(),
                'cart_total': CartService.get_cart_total()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el carrito'
            }), 400
    else:
        if success:
            flash('Carrito actualizado', 'success')
        else:
            flash('No se pudo actualizar el carrito', 'error')
        return redirect(url_for('cart.view_cart'))


@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.get_json() if request.is_json else request.form

    wine_id = data.get('wine_id')

    if not wine_id:
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'Wine ID is required'
            }), 400
        flash('Error: ID de vino requerido', 'error')
        return redirect(url_for('cart.view_cart'))

    success = CartService.remove_item(wine_id)

    if request.is_json:
        if success:
            return jsonify({
                'success': True,
                'cart_count': CartService.get_cart_count(),
                'cart_total': CartService.get_cart_total()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el producto'
            }), 400
    else:
        if success:
            flash('Producto eliminado del carrito', 'success')
        else:
            flash('No se pudo eliminar el producto', 'error')
        return redirect(url_for('cart.view_cart'))


@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    """Clear all items from cart"""
    CartService.clear_cart()

    if request.is_json:
        return jsonify({
            'success': True,
            'cart_count': 0,
            'cart_total': 0
        })
    else:
        flash('Carrito vaciado', 'success')
        return redirect(url_for('cart.view_cart'))


@cart_bp.route('/api/cart')
def api_cart():
    """API endpoint to get cart data"""
    return jsonify({
        'success': True,
        'items': CartService.get_cart_items(),
        'total': CartService.get_cart_total(),
        'count': CartService.get_cart_count()
    })
