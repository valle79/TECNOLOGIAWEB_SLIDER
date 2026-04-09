"""
Authentication routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User
from services import CartService
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'GET':
        cart_count = CartService.get_cart_count()
        return render_template('login.html', cart_count=cart_count)

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Email y contraseña son requeridos', 'error')
        return redirect(url_for('auth.login'))

    user = User.verify_password(email, password)

    if user:
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        session['user_name'] = user['full_name']
        session['is_admin'] = user.get('is_admin', False)

        flash(f'Bienvenido, {user["full_name"]}!', 'success')

        # Redirect to admin panel if admin
        if user.get('is_admin'):
            return redirect(url_for('admin.dashboard'))

        # Redirect to checkout if cart has items
        if CartService.get_cart_count() > 0:
            return redirect(url_for('order.checkout'))

        return redirect(url_for('main.index'))
    else:
        flash('Email o contraseña incorrectos', 'error')
        return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if request.method == 'GET':
        cart_count = CartService.get_cart_count()
        return render_template('register.html', cart_count=cart_count)

    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    full_name = request.form.get('full_name')
    phone = request.form.get('phone')

    # Validation
    if not all([email, password, confirm_password, full_name]):
        flash('Todos los campos son requeridos', 'error')
        return redirect(url_for('auth.register'))

    if not validate_email(email):
        flash('Email inválido', 'error')
        return redirect(url_for('auth.register'))

    if password != confirm_password:
        flash('Las contraseñas no coinciden', 'error')
        return redirect(url_for('auth.register'))

    if len(password) < 6:
        flash('La contraseña debe tener al menos 6 caracteres', 'error')
        return redirect(url_for('auth.register'))

    # Check if user exists
    existing_user = User.get_by_email(email)
    if existing_user:
        flash('El email ya está registrado', 'error')
        return redirect(url_for('auth.register'))

    # Create user
    user_id = User.create(email, password, full_name, phone)

    if user_id:
        flash('Registro exitoso. Por favor inicia sesión', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('Error al crear la cuenta', 'error')
        return redirect(url_for('auth.register'))


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        flash('Debes iniciar sesión', 'warning')
        return redirect(url_for('auth.login'))

    user = User.get_by_id(session['user_id'])
    cart_count = CartService.get_cart_count()

    return render_template('profile.html', user=user, cart_count=cart_count)
