"""
Initialize database tables on Railway
"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection using Railway credentials
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'wine_ecommerce')
}

print("🔄 Conectando a Railway...")
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("✅ Conexión exitosa a Railway!")
except Exception as e:
    print(f"❌ Error al conectar: {e}")
    exit(1)

# Create tables
tables = {
    'users': """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    
    'wines': """
        CREATE TABLE IF NOT EXISTS wines (
            id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
            name VARCHAR(255) NOT NULL,
            wine_type VARCHAR(100),
            price DECIMAL(10, 2) NOT NULL,
            country VARCHAR(100),
            region VARCHAR(100),
            year INT,
            grape_variety VARCHAR(255),
            alcohol_content DECIMAL(5, 2),
            description LONGTEXT,
            stock INT DEFAULT 0,
            image_url VARCHAR(500),
            is_featured BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_name (name),
            INDEX idx_type (wine_type),
            INDEX idx_featured (is_featured)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    
    'orders': """
        CREATE TABLE IF NOT EXISTS orders (
            id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
            user_id VARCHAR(36),
            customer_name VARCHAR(255) NOT NULL,
            customer_email VARCHAR(255) NOT NULL,
            customer_phone VARCHAR(20),
            shipping_address TEXT NOT NULL,
            shipping_city VARCHAR(100) NOT NULL,
            shipping_country VARCHAR(100) NOT NULL,
            is_international BOOLEAN DEFAULT FALSE,
            payment_method VARCHAR(50),
            notes LONGTEXT,
            subtotal DECIMAL(10, 2) NOT NULL,
            shipping_cost DECIMAL(10, 2) NOT NULL,
            total DECIMAL(10, 2) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            INDEX idx_user_id (user_id),
            INDEX idx_status (status),
            INDEX idx_email (customer_email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    
    'order_items': """
        CREATE TABLE IF NOT EXISTS order_items (
            id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
            order_id VARCHAR(36) NOT NULL,
            wine_id VARCHAR(36) NOT NULL,
            wine_name VARCHAR(255) NOT NULL,
            wine_price DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL,
            subtotal DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (wine_id) REFERENCES wines(id) ON DELETE RESTRICT,
            INDEX idx_order_id (order_id),
            INDEX idx_wine_id (wine_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
}

print("\n📊 Creando tablas...")
for table_name, create_query in tables.items():
    try:
        cursor.execute(create_query)
        print(f"  ✅ Tabla '{table_name}' creada/verificada")
    except Exception as e:
        print(f"  ❌ Error al crear tabla '{table_name}': {e}")

conn.commit()
print("\n✅ ¡Iniciación de base de datos completada!")
print("\n📝 Próximos pasos:")
print("   1. Ejecuta: py create_admin.py (para crear usuario admin)")
print("   2. Ejecuta: py app.py (para iniciar la aplicación)")

cursor.close()
conn.close()
