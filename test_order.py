"""
Script to test order creation
"""
import mysql.connector
from dotenv import load_dotenv
import os

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

# Test insert
print("\nProbando inserción de pedido...")
try:
    cursor.execute("""
        INSERT INTO orders (
            customer_name, customer_email, customer_phone,
            shipping_address, shipping_city, shipping_country,
            is_international, subtotal, shipping_cost, total,
            status, payment_method
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        'Test User',
        'test@test.com',
        '123456789',
        'Test Address 123',
        'Lima',
        'Peru',
        False,
        100.00,
        10.00,
        110.00,
        'pending',
        'credit_card'
    ))
    
    conn.commit()
    
    # Get the inserted ID
    cursor.execute("SELECT LAST_INSERT_ID() as last_id")
    result = cursor.fetchone()
    print(f"✅ Pedido insertado con lastrowid: {cursor.lastrowid}")
    print(f"✅ LAST_INSERT_ID(): {result}")
    
    # Try to get the actual UUID
    cursor.execute("SELECT id FROM orders ORDER BY created_at DESC LIMIT 1")
    order = cursor.fetchone()
    print(f"✅ Último pedido creado: {order}")
    
    # Clean up test order
    if order:
        cursor.execute("DELETE FROM orders WHERE id = %s", (order['id'],))
        conn.commit()
        print(f"✅ Pedido de prueba eliminado")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

cursor.close()
conn.close()
