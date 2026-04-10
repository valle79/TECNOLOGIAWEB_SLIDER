"""
Admin panel routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import Wine, Order
from services import CartService, OrderService
import cloudinary_service
import logging

logger = logging.getLogger(__name__)

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

    return render_template('admin_dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         cart_count=cart_count)


@admin_bp.route('/wines')
@admin_required
def wines():
    """Manage wines"""
    wines = Wine.get_all(limit=100)
    cart_count = CartService.get_cart_count()

    return render_template('admin_wines.html',
                         wines=wines,
                         cart_count=cart_count)


@admin_bp.route('/wines/add', methods=['GET', 'POST'])
@admin_required
def add_wine():
    """Add new wine"""
    if request.method == 'GET':
        cart_count = CartService.get_cart_count()
        return render_template('admin_wine_form.html',
                             wine=None,
                             cart_count=cart_count)

    # Handle image upload to Cloudinary
    image_url = request.form.get('image_url')  # Keep URL field as fallback
    wine_name = request.form.get('name', 'wine')

    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename != '':
            # Upload to Cloudinary
            upload_result = cloudinary_service.upload_wine_image(
                file, 
                wine_name=wine_name,
                auto_optimize=True
            )
            
            if upload_result:
                # Store secure_url (encrypted/safe for HTTPS)
                image_url = upload_result['secure_url']
                logger.info(f"Image uploaded to Cloudinary: {upload_result['public_id']}")
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
        'is_featured': bool(request.form.get('is_featured'))
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
        return render_template('admin_wine_form.html',
                             wine=wine,
                             cart_count=cart_count)

    # Handle image upload to Cloudinary
    image_url = request.form.get('image_url')  # Keep URL field as fallback
    old_image_url = wine.get('image_url')
    wine_name = request.form.get('name', 'wine')

    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename != '':
            # Upload new image to Cloudinary
            upload_result = cloudinary_service.upload_wine_image(
                file,
                wine_name=wine_name,
                auto_optimize=True
            )
            
            if upload_result:
                # Store secure_url
                image_url = upload_result['secure_url']
                
                # Delete old image from Cloudinary if it exists
                if old_image_url:
                    public_id = cloudinary_service.extract_public_id_from_url(old_image_url)
                    if public_id:
                        cloudinary_service.delete_wine_image(public_id)
                        logger.info(f"Deleted old image: {public_id}")
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
        'is_featured': bool(request.form.get('is_featured'))
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
    # Get wine to find image URL
    wine = Wine.get_by_id(wine_id)
    
    # Delete image from Cloudinary if it exists
    if wine and wine.get('image_url'):
        public_id = cloudinary_service.extract_public_id_from_url(wine['image_url'])
        if public_id:
            cloudinary_service.delete_wine_image(public_id)
            logger.info(f"Deleted image for wine {wine_id}: {public_id}")
    
    # Delete wine from database
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

    return render_template('admin_orders.html',
                         orders=orders,
                         current_status=status_filter,
                         cart_count=cart_count)


@admin_bp.route('/orders/<order_id>')
@admin_required
def order_detail(order_id):
    """View order details"""
    order = OrderService.get_order_summary(order_id)

    if not order:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('admin.orders'))

    cart_count = CartService.get_cart_count()

    return render_template('admin_order_detail.html',
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
