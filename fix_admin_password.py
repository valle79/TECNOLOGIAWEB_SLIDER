"""
Fix admin password - Simple version
"""
from database import Database
from config import Config
import bcrypt

def fix_admin_password():
    """Fix admin password to admin123"""
    # Initialize database
    db_config = {
        'host': Config.DB_HOST,
        'port': Config.DB_PORT,
        'user': Config.DB_USER,
        'password': Config.DB_PASSWORD,
        'database': Config.DB_NAME
    }
    Database.initialize(db_config)
    print("✅ Base de datos inicializada")
    
    password = 'admin123'
    email = 'admin@vinosdelvalle.com'
    
    # Generate new hash
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    print(f"\n🔧 Actualizando contraseña para {email}...")
    print(f"📝 Nuevo hash: {password_hash[:50]}...")
    
    try:
        with Database.get_cursor() as cursor:
            # Update password
            cursor.execute(
                "UPDATE users SET password_hash = %s, is_admin = 1 WHERE email = %s",
                (password_hash, email)
            )
            
            print(f"✅ Contraseña actualizada exitosamente!")
            print(f"\n📋 Credenciales:")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            
            # Verify
            cursor.execute("SELECT email, is_admin FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user:
                print(f"\n✅ Usuario verificado:")
                print(f"   Email: {user['email']}")
                print(f"   Is Admin: {user['is_admin']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("="*60)
    print("🔐 ARREGLANDO CONTRASEÑA DE ADMIN")
    print("="*60)
    fix_admin_password()
    print("="*60)
