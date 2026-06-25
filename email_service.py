import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def is_configured() -> bool:
        return bool(Config.MAIL_USERNAME and Config.MAIL_PASSWORD and Config.MAIL_SERVER)

    @staticmethod
    def send_order_confirmation(order: dict, cart_items: list) -> bool:
        if not EmailService.is_configured():
            logger.warning("Email not configured. Skipping order confirmation email.")
            return False

        try:
            customer_email = order.get('customer_email')
            customer_name = order.get('customer_name', 'Cliente')
            order_id = order.get('order_id', '')
            order_id_short = order_id[:8] if order_id else 'N/A'
            created_at = order.get('created_at', '')
            if hasattr(created_at, 'strftime'):
                created_at = created_at.strftime('%d/%m/%Y %H:%M')

            subject = f"Pedido #{order_id_short} Confirmado - Vinos del Valle"

            items_html = ''
            for item in cart_items:
                qty = item.get('quantity', 0)
                label = 'caja' if item.get('is_box') else 'unidad'
                items_html += f"""
                <tr>
                    <td style="padding:10px;border-bottom:1px solid #eee;">{item.get('name', '')}</td>
                    <td style="padding:10px;border-bottom:1px solid #eee;text-align:center;">{qty} {label}(s)</td>
                    <td style="padding:10px;border-bottom:1px solid #eee;text-align:right;">S/ {item.get('price', 0):.2f}</td>
                    <td style="padding:10px;border-bottom:1px solid #eee;text-align:right;">S/ {(item.get('price', 0) * qty):.2f}</td>
                </tr>"""

            html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;background:#f5f5f5;margin:0;padding:20px;">
    <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
        <div style="background:linear-gradient(135deg,#7f1d1d,#991b1b);padding:30px;text-align:center;">
            <img src="https://res.cloudinary.com/dyxf6yb4b/image/upload/v1740163985/sanroque.png" alt="San Roque" style="height:60px;margin-bottom:10px;">
            <h1 style="color:#fff;margin:10px 0 0;font-size:24px;">¡Pedido Confirmado!</h1>
        </div>
        <div style="padding:30px;">
            <p style="font-size:16px;color:#333;">Hola <strong>{customer_name}</strong>,</p>
            <p style="color:#555;">Gracias por tu compra. Hemos recibido tu pedido y lo procesaremos pronto.</p>

            <div style="background:#f9f9f9;border-radius:8px;padding:20px;margin:20px 0;">
                <h2 style="font-size:18px;color:#7f1d1d;margin:0 0 15px;">Resumen del Pedido</h2>
                <table style="width:100%;border-collapse:collapse;">
                    <tr>
                        <td style="padding:5px 0;color:#666;">N° Pedido</td>
                        <td style="padding:5px 0;text-align:right;font-weight:bold;">#{order_id_short}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0;color:#666;">Fecha</td>
                        <td style="padding:5px 0;text-align:right;">{created_at}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px 0;color:#666;">Estado</td>
                        <td style="padding:5px 0;text-align:right;"><span style="background:#fef3c7;color:#92400e;padding:3px 10px;border-radius:12px;font-size:13px;">Pendiente</span></td>
                    </tr>
                </table>
            </div>

            <h2 style="font-size:18px;color:#7f1d1d;margin:20px 0 10px;">Productos</h2>
            <table style="width:100%;border-collapse:collapse;">
                <thead>
                    <tr style="background:#f3f3f3;">
                        <th style="padding:10px;text-align:left;">Producto</th>
                        <th style="padding:10px;text-align:center;">Cantidad</th>
                        <th style="padding:10px;text-align:right;">Precio</th>
                        <th style="padding:10px;text-align:right;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" style="padding:10px;text-align:right;font-weight:bold;">Subtotal</td>
                        <td style="padding:10px;text-align:right;">S/ {order.get('subtotal', 0):.2f}</td>
                    </tr>
                    <tr>
                        <td colspan="3" style="padding:5px 10px;text-align:right;color:#666;">Envío</td>
                        <td style="padding:5px 10px;text-align:right;">S/ {order.get('shipping_cost', 0):.2f}</td>
                    </tr>
                    <tr>
                        <td colspan="3" style="padding:10px;text-align:right;font-size:18px;font-weight:bold;color:#7f1d1d;">Total</td>
                        <td style="padding:10px;text-align:right;font-size:18px;font-weight:bold;color:#7f1d1d;">S/ {order.get('total', 0):.2f}</td>
                    </tr>
                </tfoot>
            </table>

            <div style="background:#f9f9f9;border-radius:8px;padding:20px;margin:20px 0;">
                <h2 style="font-size:18px;color:#7f1d1d;margin:0 0 15px;">Dirección de Envío</h2>
                <p style="margin:3px 0;color:#555;">{order.get('customer_name', '')}</p>
                <p style="margin:3px 0;color:#555;">{order.get('shipping_address', '')}</p>
                <p style="margin:3px 0;color:#555;">{order.get('shipping_city', '')}, {order.get('shipping_country', '')}</p>
            </div>

            <p style="color:#555;margin-top:20px;">Si tienes alguna pregunta, responde a este correo o contáctanos.</p>
            <p style="color:#999;font-size:13px;border-top:1px solid #eee;padding-top:15px;margin-top:15px;">
                Vinos del Valle - Vitivinícola San Roque<br>
                Envíos a todo el Perú y exportación internacional.
            </p>
        </div>
    </div>
</body>
</html>"""

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = Config.MAIL_USERNAME
            msg['To'] = customer_email
            msg.attach(MIMEText(html, 'html', 'utf-8'))

            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT, timeout=30) as server:
                server.starttls()
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                server.sendmail(Config.MAIL_USERNAME, customer_email, msg.as_string())

            logger.info(f"Order confirmation email sent to {customer_email} for order {order_id_short}")
            return True

        except Exception as e:
            logger.error(f"Failed to send order email: {e}")
            return False
