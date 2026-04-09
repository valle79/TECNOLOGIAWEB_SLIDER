"""
Admin panel controller
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models.wine import Wine
from models.order import Order
from services.cart_service import CartService
from utils.file_upload import save_wine_image, delete_wine_image

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('Acceso denegado. Se requieren permisos de administrador', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard"""
    stats = Order.get_statistics()
    recent_orders = Order.get_all(limit=10)
    cart_count = CartService.get_cart_count()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         cart_count=cart_count)


@admin_bp.route('/wines')
@admin_required
def wines():
    """Manage wines"""
    wines = Wine.get_all(limit=100)
    cart_count = CartService.get_cart_count()
    
    return render_template('admin/wines.html',
                         wines=wines,
                         cart_count=cart_count)


@admin_bp.route('/wines/add', methods=['GET', 'POST'])
@admin_required
def add_wine():
    """Add new wine"""
    if request.method == 'GET':
        cart_count = CartService.get_cart_count()
        return render_template('admin/wine_form.html',
                             wine=None,
                             cart_count=cart_count)
    
    # Handle image upload
    image_url = request.form.get('image_url')  # Keep URL field as fallback
    
    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename != '':
            uploaded_url = save_wine_image(file)
            if uploaded_url:
                image_url = uploaded_url
            else:
                flash('Error al subir la imagen. Usando URL proporcionada.', 'warning')
    
    wine_data = {
        'name': request.form.get('name'),
        'wine_type': request.form.get('wine_type'),
        'price': float(request.form.get('price')),
        'country': request.form.get('country'),
        'region': request.form.get('region'),
        'year': int(request.form.get('year')) if request.form.get('year') else None,
        'grape_variety': request.form.get('grape_variety'),
        'alcohol_content': float(request.form.get('alcohol_content')) if request.form.get('alcohol_content') else None,
        'description': request.form.get('description'),
        'stock': int(request.form.get('stock', 0)),
        'image_url': image_url,
        'is_featured': bool(request.form.get('is_featured'))  # Fixed: converts to boolean
    }
    
    wine_id = Wine.create(wine_data)
    
    if wine_id:
        flash('Vino agregado exitosamente', 'success')
        return redirect(url_for('admin.wines'))
    else:
        flash('Error al agregar el vino', 'error')
        return redirect(url_for('admin.add_wine'))


@admin_bp.route('/wines/edit/<wine_id>', methods=['GET', 'POST'])
@admin_required
def edit_wine(wine_id):
    """Edit wine"""
    wine = Wine.get_by_id(wine_id)
    
    if not wine:
        flash('Vino no encontrado', 'error')
        return redirect(url_for('admin.wines'))
    
    if request.method == 'GET':
        cart_count = CartService.get_cart_count()
        return render_template('admin/wine_form.html',
                             wine=wine,
                             cart_count=cart_count)
    
    # Handle image upload
    image_url = request.form.get('image_url')  # Keep URL field as fallback
    old_image_url = wine.get('image_url')
    
    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename != '':
            uploaded_url = save_wine_image(file)
            if uploaded_url:
                # Delete old image if it was uploaded (not a default/external URL)
                if old_image_url and old_image_url.startswith('/static/images/wines/'):
                    delete_wine_image(old_image_url)
                image_url = uploaded_url
            else:
                flash('Error al subir la imagen. Manteniendo imagen anterior.', 'warning')
                image_url = old_image_url
    elif not image_url:
        # If no new file and no URL provided, keep the old image
        image_url = old_image_url
    
    wine_data = {
        'name': request.form.get('name'),
        'wine_type': request.form.get('wine_type'),
        'price': float(request.form.get('price')),
        'country': request.form.get('country'),
        'region': request.form.get('region'),
        'year': int(request.form.get('year')) if request.form.get('year') else None,
        'grape_variety': request.form.get('grape_variety'),
        'alcohol_content': float(request.form.get('alcohol_content')) if request.form.get('alcohol_content') else None,
        'description': request.form.get('description'),
        'stock': int(request.form.get('stock', 0)),
        'image_url': image_url,
        'is_featured': bool(request.form.get('is_featured'))  # Fixed: converts to boolean
    }
    
    success = Wine.update(wine_id, wine_data)
    
    if success:
        flash('Vino actualizado exitosamente', 'success')
        return redirect(url_for('admin.wines'))
    else:
        flash('Error al actualizar el vino', 'error')
        return redirect(url_for('admin.edit_wine', wine_id=wine_id))


@admin_bp.route('/wines/delete/<wine_id>', methods=['POST'])
@admin_required
def delete_wine(wine_id):
    """Delete wine"""
    success = Wine.delete(wine_id)
    
    if success:
        flash('Vino eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el vino', 'error')
    
    return redirect(url_for('admin.wines'))


@admin_bp.route('/orders')
@admin_required
def orders():
    """Manage orders"""
    status_filter = request.args.get('status')
    filters = {'status': status_filter} if status_filter else None
    
    orders = Order.get_all(filters=filters, limit=100)
    cart_count = CartService.get_cart_count()
    
    return render_template('admin/orders.html',
                         orders=orders,
                         current_status=status_filter,
                         cart_count=cart_count)


@admin_bp.route('/orders/<order_id>')
@admin_required
def order_detail(order_id):
    """View order details"""
    order = Order.get_by_id(order_id)
    
    if not order:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('admin.orders'))
    
    cart_count = CartService.get_cart_count()
    
    return render_template('admin/order_detail.html',
                         order=order,
                         cart_count=cart_count)


@admin_bp.route('/orders/<order_id>/update-status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    new_status = request.form.get('status')
    
    if not new_status:
        flash('Estado requerido', 'error')
        return redirect(url_for('admin.order_detail', order_id=order_id))
    
    success = Order.update_status(order_id, new_status)
    
    if success:
        flash('Estado del pedido actualizado', 'success')
    else:
        flash('Error al actualizar el estado', 'error')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))
