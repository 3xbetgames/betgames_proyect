import MySQLdb

# Configuración de la base de datos
MYSQL_HOST = 'autorack.proxy.rlwy.net'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'aUJCbMrDpEfkcWjaOXuWmcyvpkwZLBbx'
MYSQL_DB = 'railway'
MYSQL_PORT = 16342

try:
    # Conectar a la base de datos
    db = MySQLdb.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        port=MYSQL_PORT
    )
    
    cursor = db.cursor()

    # Crear la tabla 'usuarios'
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users_2 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        email VARCHAR(100)
    )
    """
    
    cursor.execute(create_table_query)
    db.commit()  # Aplicar cambios en la base de datos
    print("Tabla 'usuarios' creada exitosamente.")
    
except MySQLdb.Error as e:
    print(f"Error al crear la tabla: {e}")

finally:
    if cursor:
        cursor.close()
    if db:
        db.close()
