import MySQLdb
from .entities.User import User

class ModelUser:

    @classmethod
    def create_user_table(cls, conn):
        """Crea la tabla de usuarios si no existe, ajustando el tamaño de la columna password."""
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,  -- Cambiar a VARCHAR(255)
                    fullname VARCHAR(100),
                    email VARCHAR(100),
                    document_type VARCHAR(10),
                    identity_number VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("Tabla 'users' creada/verificada correctamente.")
        except MySQLdb.Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            cursor.close()

    @classmethod
    def register_user(cls, conn, username, password, fullname, email, document_type, identity_number):
        """Registra un nuevo usuario en la base de datos."""
        cursor = conn.cursor()
        try:
            hashed_password = User.create_hash(password)  # Genera el hash de la contraseña
            cursor.execute("""
                INSERT INTO users (username, password, fullname, email, document_type, identity_number)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, hashed_password, fullname, email, document_type, identity_number))
            conn.commit()
            print("Usuario registrado exitosamente.")
        except MySQLdb.Error as e:
            print(f"Error al registrar el usuario: {e}")
        finally:
            cursor.close()

    @classmethod
    def get_by_id(cls, conn, id):
        """Obtiene un usuario por su ID."""
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            user = cursor.fetchone()
            return User(**user) if user else None
        except MySQLdb.Error as e:
            print(f"Error al obtener el usuario: {e}")
            return None
        finally:
            cursor.close()

    @classmethod
    def login(cls, conn, user):
        """Obtiene un usuario por su nombre de usuario y contraseña."""
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
            user_data = cursor.fetchone()
            return User(**user_data) if user_data else None
        except MySQLdb.Error as e:
            print(f"Error al obtener el usuario: {e}")
            return None
        finally:
            cursor.close()
