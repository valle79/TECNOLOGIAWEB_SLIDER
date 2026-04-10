"""
Main page routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Wine
from services import CartService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    featured_wines = Wine.get_featured(limit=6)
    cart_count = CartService.get_cart_count()

    return render_template(
        'index.html',
        featured_wines=featured_wines,
        cart_count=cart_count
    )


@main_bp.route('/about')
def about():
    cart_count = CartService.get_cart_count()
    return render_template('about.html', cart_count=cart_count)


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    cart_count = CartService.get_cart_count()

    if request.method == 'POST':

        # 🛡️ Anti-spam
        if request.form.get("website"):
            return "Spam detectado", 400

        # 📥 Datos
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # ✅ Validación
        if not name or not email or not subject or not message:
            flash('Completa los campos obligatorios', 'error')
            return redirect(url_for('main.contact'))

        # 🔥 LOG (luego reemplazar por BD o email)
        print("📩 Nuevo mensaje:")
        print(f"Nombre: {name}")
        print(f"Email: {email}")
        print(f"Teléfono: {phone}")
        print(f"Asunto: {subject}")
        print(f"Mensaje: {message}")

        flash('Mensaje enviado correctamente', 'success')
        return redirect(url_for('main.contact'))

    return render_template('contact.html', cart_count=cart_count)