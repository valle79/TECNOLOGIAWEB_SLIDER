# Guía de Instalación - Vinos del Valle E-commerce (MySQL)

## Paso 1: Instalar MySQL

### Windows:
1. Descargar MySQL desde: https://dev.mysql.com/downloads/installer/
2. Ejecutar el instalador
3. Seleccionar "Developer Default"
4. Durante la instalación, configurar:
   - Root password (recordar esta contraseña)
   - Puerto: 3306 (por defecto)
5. Completar la instalación

### Verificar instalación:
```bash
mysql --version
```

## Paso 2: Crear la Base de Datos

### Opción A: Usando MySQL Workbench (Recomendado)
1. Abrir MySQL Workbench
2. Conectarse al servidor local
3. Abrir el archivo `database_mysql.sql`
4. Ejecutar el script completo (⚡ icono de rayo)

### Opción B: Usando línea de comandos
```bash
mysql -u root -p < database_mysql.sql
```

## Paso 3: Configurar Variables de Entorno

El archivo `.env` ya está creado. Edítalo con tus credenciales:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=TU_PASSWORD_AQUI
DB_NAME=wine_ecommerce
```

## Paso 4: Instalar Dependencias Python

```bash
# Desinstalar psycopg2 si está instalado
pip uninstall psycopg2-binary -y

# Instalar nuevas dependencias
pip install -r requirements.txt
```

## Paso 5: Ejecutar la Aplicación

```bash
python app.py
```

Visita: `http://localhost:5000`

## Credenciales por Defecto

**Administrador:**
- Email: `admin@vinosdelvalle.com`
- Contraseña: `admin123`

## Solución de Problemas

### Error: "Access denied for user 'root'@'localhost'"
- Verificar que la contraseña en `.env` sea correcta
- Verificar que MySQL esté corriendo

### Error: "Unknown database 'wine_ecommerce'"
- Ejecutar el script `database_mysql.sql`
- Verificar que la base de datos se creó: `SHOW DATABASES;`

### Error: "Can't connect to MySQL server"
- Verificar que MySQL esté corriendo
- En Windows: Servicios → MySQL80 → Iniciar
- Verificar el puerto en `.env` (por defecto 3306)

### Verificar que MySQL está corriendo:
```bash
# Windows (PowerShell como administrador)
Get-Service MySQL80

# Si no está corriendo, iniciarlo:
Start-Service MySQL80
```

## Comandos Útiles MySQL

### Conectarse a MySQL:
```bash
mysql -u root -p
```

### Ver bases de datos:
```sql
SHOW DATABASES;
```

### Usar la base de datos:
```sql
USE wine_ecommerce;
```

### Ver tablas:
```sql
SHOW TABLES;
```

### Ver datos de vinos:
```sql
SELECT * FROM wines;
```

### Ver usuarios:
```sql
SELECT email, full_name, is_admin FROM users;
```

## Estructura de la Base de Datos

- **users** - Usuarios del sistema
- **wines** - Catálogo de vinos
- **orders** - Pedidos
- **order_items** - Detalles de pedidos

## Próximos Pasos

1. Verificar que la aplicación corre correctamente
2. Iniciar sesión con las credenciales de administrador
3. Agregar más vinos desde el panel admin
4. Personalizar el contenido según tus necesidades
