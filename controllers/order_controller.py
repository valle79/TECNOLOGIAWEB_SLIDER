"""
Order processing controller
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from services.order_service import OrderService
from services.cart_service import CartService
from models.order import Order

order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/checkout')
def checkout():
    """Checkout page"""
    cart_items = CartService.get_cart_items()
    cart_total = CartService.get_cart_total()
    cart_count = CartService.get_cart_count()
    
    if not cart_items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('wine.catalog'))
    
    # Get user data if logged in
    user_data = {}
    if 'user_id' in session:
        user_data = {
            'email': session.get('user_email'),
            'name': session.get('user_name')
        }
    
    return render_template('checkout.html',
                         cart_items=cart_items,
                         cart_total=cart_total,
                         cart_count=cart_count,
                         user_data=user_data)


@order_bp.route('/create', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.form
    
    # Validate required fields
    required_fields = ['customer_name', 'customer_email', 'shipping_address', 
                      'shipping_city', 'shipping_country']
    
    for field in required_fields:
        if not data.get(field):
            flash(f'Campo requerido: {field}', 'error')
            return redirect(url_for('order.checkout'))
    
    # Prepare customer data
    customer_data = {
        'customer_name': data.get('customer_name'),
        'customer_email': data.get('customer_email'),
        'customer_phone': data.get('customer_phone'),
        'shipping_address': data.get('shipping_address'),
        'shipping_city': data.get('shipping_city'),
        'shipping_country': data.get('shipping_country'),
        'payment_method': data.get('payment_method', 'pending'),
        'notes': data.get('notes')
    }
    
    try:
        user_id = session.get('user_id')
        order_id = OrderService.create_order_from_cart(customer_data, user_id)
        
        if order_id:
            flash('¡Pedido creado exitosamente!', 'success')
            return redirect(url_for('order.confirmation', order_id=order_id))
        else:
            flash('Error al crear el pedido', 'error')
            return redirect(url_for('order.checkout'))
            
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('order.checkout'))
    except Exception as e:
        flash('Error al procesar el pedido', 'error')
        return redirect(url_for('order.checkout'))


@order_bp.route('/confirmation/<order_id>')
def confirmation(order_id):
    """Order confirmation page"""
    order = OrderService.get_order_summary(order_id)
    
    if not order:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('main.index'))
    
    cart_count = CartService.get_cart_count()
    
    return render_template('order_confirmation.html',
                         order=order,
                         cart_count=cart_count)


@order_bp.route('/my-orders')
def my_orders():
    """View user's orders"""
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver tus pedidos', 'warning')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    orders = Order.get_all(filters={'user_id': user_id})
    cart_count = CartService.get_cart_count()
    
    return render_template('my_orders.html',
                         orders=orders,
                         cart_count=cart_count)


@order_bp.route('/<order_id>')
def order_detail(order_id):
    """View order details"""
    order = OrderService.get_order_summary(order_id)
    
    if not order:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('main.index'))
    
    # Check if user owns this order (if logged in)
    if 'user_id' in session:
        user_orders = Order.get_all(filters={'user_id': session['user_id']})
        order_ids = [o['id'] for o in user_orders]
        if order_id not in order_ids:
            flash('No tienes permiso para ver este pedido', 'error')
            return redirect(url_for('main.index'))
    
    cart_count = CartService.get_cart_count()
    
    return render_template('order_detail.html',
                         order=order,
                         cart_count=cart_count)


@order_bp.route('/api/calculate-shipping', methods=['POST'])
def api_calculate_shipping():
    """API endpoint to calculate shipping cost"""
    data = request.get_json()
    country = data.get('country')
    
    if not country:
        return jsonify({
            'success': False,
            'error': 'Country is required'
        }), 400
    
    shipping_cost = OrderService.calculate_shipping(country)
    cart_total = CartService.get_cart_total()
    
    return jsonify({
        'success': True,
        'shipping_cost': shipping_cost,
        'subtotal': cart_total,
        'total': cart_total + shipping_cost
    })
