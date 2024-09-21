import MySQLdb

# Configuración de la base de datos
MYSQL_HOST = 'junction.proxy.rlwy.net'  # Host de la base de datos remota
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'gkbfaifYAKAymXfFcdfQvazabsbwDOzr'
MYSQL_DB = 'railway'
MYSQL_PORT = 24326  # Puerto de la instancia remota

try:
    # Establecer la conexión a la base de datos
    db = MySQLdb.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        port=MYSQL_PORT
    )
    
    # Crear un cursor para realizar la consulta
    cursor = db.cursor()
    
    # Ejecutar una consulta para obtener la versión de MySQL
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    
    # Imprimir la versión de la base de datos
    print(f"Conexión exitosa. Versión de la base de datos: {version[0]}")

except MySQLdb.Error as e:
    print(f"Error al conectar a la base de datos: {e}")

finally:
    # Cerrar el cursor y la conexión
    if cursor:
        cursor.close()
    if db:
        db.close()
