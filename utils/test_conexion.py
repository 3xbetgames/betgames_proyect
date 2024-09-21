import mysql.connector
from mysql.connector import Error
from config import config

def test_connection():
    connection = None
    try:
        # Credenciales de la base de datos Railway
        host = 'autorack.proxy.rlwy.net'
        database = 'railway'
        user = 'root'
        password = 'HQqDHZiHCAjwdPARBqvItFayoeVrtDLv'
        port = 52547

        # Conexión a la base de datos usando las credenciales
        connection = mysql.connector.connect(
            host=host,  
            database=database,              
            user=user,                     
            password=password,  
            port=port                       
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Conectado al servidor MySQL versión {db_info}")
            cursor = connection.cursor()

            # Crear la tabla `user`
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS `user` (
              `id` smallint(3) UNSIGNED NOT NULL AUTO_INCREMENT,
              `username` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
              `password` char(102) COLLATE utf8_unicode_ci NOT NULL,
              `fullname` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
              `email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
              `document_type` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
              `identity_number` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
              PRIMARY KEY (`id`)
            );
            '''
            cursor.execute(create_table_query)
            connection.commit()
            print("Tabla 'user' creada o ya existe.")

    except Error as e:
        print(f"Error de conexión o ejecución SQL: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("La conexión MySQL se cerró")

if __name__ == "__main__":
    test_connection()
