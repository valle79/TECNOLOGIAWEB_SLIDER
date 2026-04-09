"""
Script to create or reset admin user
"""
import mysql.connector
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

# Database connection
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'wine_ecommerce')
}

print("Conectando a la base de datos...")
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

# Check if admin exists
cursor.execute("SELECT * FROM users WHERE email = 'admin@vinosdelvalle.com'")
admin = cursor.fetchone()

if admin:
    print("Usuario admin encontrado. Eliminando...")
    cursor.execute("DELETE FROM users WHERE email = 'admin@vinosdelvalle.com'")
    conn.commit()

# Create new admin with correct password hash
print("Creando nuevo usuario admin...")
password = 'admin123'
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cursor.execute("""
    INSERT INTO users (email, password_hash, full_name, is_admin)
    VALUES (%s, %s, %s, %s)
""", ('admin@vinosdelvalle.com', password_hash, 'Administrador', True))

conn.commit()

print("✅ Usuario admin creado exitosamente!")
print("Email: admin2@vinosdelvalle.com")
print("Contraseña: admin123")

# Verify
cursor.execute("SELECT email, full_name, is_admin FROM users WHERE email = 'admin@vinosdelvalle.com'")
admin = cursor.fetchone()
print(f"\nVerificación: {admin}")

cursor.close()
conn.close()
