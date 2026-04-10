#!/usr/bin/env python
"""
Script para probar la configuración de Cloudinary
Ejecutar: python test_cloudinary.py
"""
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_cloudinary_setup():
    """Test básico de Cloudinary"""
    
    print("=" * 60)
    print("🧪 PRUEBA DE CONFIGURACIÓN CLOUDINARY")
    print("=" * 60)
    
    # 1. Verificar variables de entorno
    print("\n1️⃣ Verificando variables de entorno...")
    
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    if cloud_name:
        print(f"   ✅ CLOUDINARY_CLOUD_NAME: {cloud_name}")
    else:
        print("   ❌ CLOUDINARY_CLOUD_NAME: NO CONFIGURADA")
        return False
    
    if api_key:
        print(f"   ✅ CLOUDINARY_API_KEY: {api_key[:10]}...")
    else:
        print("   ❌ CLOUDINARY_API_KEY: NO CONFIGURADA")
        return False
    
    if api_secret:
        print(f"   ✅ CLOUDINARY_API_SECRET: {api_secret[:10]}...")
    else:
        print("   ❌ CLOUDINARY_API_SECRET: NO CONFIGURADA")
        return False
    
    # 2. Importar Cloudinary
    print("\n2️⃣ Importando módulo cloudinary...")
    try:
        import cloudinary
        import cloudinary.api
        print("   ✅ Módulo cloudinary importado correctamente")
    except ImportError as e:
        print(f"   ❌ Error al importar cloudinary: {e}")
        print("   Solución: pip install cloudinary>=1.36.0")
        return False
    
    # 3. Configurar Cloudinary
    print("\n3️⃣ Configurando Cloudinary...")
    try:
        from cloudinary_config import CloudinaryConfig
        CloudinaryConfig.initialize()
        print("   ✅ Cloudinary configurado correctamente")
    except Exception as e:
        print(f"   ❌ Error al configurar Cloudinary: {e}")
        return False
    
    # 4. Probar conexión
    print("\n4️⃣ Probando conexión a Cloudinary...")
    try:
        from cloudinary_service import health_check
        if health_check():
            print("   ✅ Conexión exitosa a Cloudinary")
        else:
            print("   ❌ Fallo en health check")
            return False
    except Exception as e:
        print(f"   ❌ Error en prueba de conexión: {e}")
        return False
    
    # 5. Información de cuenta
    print("\n5️⃣ Información de la cuenta Cloudinary...")
    try:
        usage = cloudinary.api.usage()
        print(f"   ✅ Almacenamiento usado: {usage['bytes_used'] / (1024*1024):.2f} MB")
        print(f"   ✅ Créditos: {usage.get('credits_used', 'N/A')}")
    except Exception as e:
        print(f"   ⚠️  No se pudo obtener información: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ¡TODO FUNCIONA CORRECTAMENTE!")
    print("=" * 60)
    return True


def test_file_upload():
    """Test de subida de archivo"""
    
    print("\n" + "=" * 60)
    print("🖼️  PRUEBA DE SUBIDA DE ARCHIVO")
    print("=" * 60)
    
    try:
        from cloudinary_service import upload_wine_image, delete_wine_image
        from io import BytesIO
        from PIL import Image
        
        # Crear imagen de prueba
        print("\n1️⃣ Creando imagen de prueba...")
        img = Image.new('RGB', (200, 200), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        img_io.name = 'test.jpg'
        
        print("   ✅ Imagen de prueba creada")
        
        # Subir a Cloudinary
        print("\n2️⃣ Subiendo imagen a Cloudinary...")
        result = upload_wine_image(img_io, wine_name='Test Wine')
        
        if result:
            print(f"   ✅ Imagen subida exitosamente")
            print(f"      URL: {result['url']}")
            print(f"      Public ID: {result['public_id']}")
            
            # Eliminar
            print("\n3️⃣ Eliminando imagen de prueba...")
            if delete_wine_image(result['public_id']):
                print(f"   ✅ Imagen eliminada correctamente")
            else:
                print(f"   ❌ No se pudo eliminar la imagen")
        else:
            print("   ❌ Error al subir imagen")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print("\n")
    
    # Test básico
    if not test_cloudinary_setup():
        print("\n❌ Revisión de configuración fallida")
        sys.exit(1)
    
    # Test de subida
    try:
        test_file_upload()
    except Exception as e:
        print(f"\n⚠️  Prueba de subida no disponible: {e}")
    
    print("\n✨ Pruebas completadas\n")
