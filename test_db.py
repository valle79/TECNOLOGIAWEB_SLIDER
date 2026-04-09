"""
Test database connection and create tables with detailed error reporting
"""
import mysql.connector
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'wine_ecommerce')
}

print("=" * 60)
print("🔧 TEST DE CONEXIÓN A BASE DE DATOS")
print("=" * 60)
print(f"\n📋 Configuración:")
print(f"  Host: {db_config['host']}")
print(f"  Puerto: {db_config['port']}")
print(f"  Usuario: {db_config['user']}")
print(f"  Base de datos: {db_config['database']}")

print("\n🔄 Intentando conectar...")
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("✅ ¡CONEXIÓN EXITOSA!")
    
    # Test: Ver versión de MySQL
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"   MySQL versión: {version[0]}")
    
    # Test: Ver tablas existentes
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"   Tablas existentes: {len(tables)}")
    for table in tables:
        print(f"     - {table[0]}")
    
    if len(tables) == 0:
        print("\n⚠️  No hay tablas. Creando...")
        
        # Create users table
        users_table = """
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
        """
        
        try:
            cursor.execute(users_table)
            conn.commit()
            print("   ✅ Tabla 'users' creada")
        except Exception as e:
            print(f"   ❌ Error creando tabla 'users': {e}")
            traceback.print_exc()
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as err:
    print(f"\n❌ ERROR DE CONEXIÓN MYSQL:")
    if err.errno == 2003:
        print("   No se puede conectar con el servidor MySQL")
        print("   Verifica:")
        print("     - Host y puerto correctos")
        print("     - Firewall/red permite conexión")
        print("     - Servidor MySQL está activo")
    elif err.errno == 1045:
        print("   Error de autenticación (usuario/contraseña)")
        print("   Verifica las credenciales en .env")
    elif err.errno == 1049:
        print("   Base de datos no existe")
        print("   Verifica DB_NAME en .env")
    else:
        print(f"   Código de error: {err.errno}")
        print(f"   Mensaje: {err.msg}")
    traceback.print_exc()
    
except Exception as e:
    print(f"\n❌ ERROR INESPERADO: {e}")
    traceback.print_exc()

print("\n" + "=" * 60)
