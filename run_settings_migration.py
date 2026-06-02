from database import Database
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    try:
        # ✅ Crear diccionario de configuración
        db_config = {
            "host": Config.DB_HOST,
            "port": Config.DB_PORT,
            "user": Config.DB_USER,
            "password": Config.DB_PASSWORD,
            "database": Config.DB_NAME
        }

        # ✅ Pasarlo como UN solo argumento
        Database.initialize(db_config)

        # Leer SQL
        with open('migrations/add_settings_table.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Ejecutar SQL
        with Database.get_cursor() as cursor:
            for statement in sql_script.split(';'):
                statement = statement.strip()
                if statement:
                    logger.info(f"Executing: {statement[:80]}...")
                    cursor.execute(statement)

        logger.info("✅ Settings migration completed successfully!")

    except Exception as e:
        logger.error(f"❌ Error running migration: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise

if __name__ == '__main__':
    run_migration()