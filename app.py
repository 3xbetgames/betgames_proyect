from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb

from config import config
from src.models.ModelUser import ModelUser
from src.models.entities.User import User

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

# Configuración de CSRF
app.config.from_object(config['development'])
csrf = CSRFProtect(app)

# Configuración de MySQL
MYSQL_HOST = config['development'].MYSQL_HOST
MYSQL_USER = config['development'].MYSQL_USER
MYSQL_PASSWORD = config['development'].MYSQL_PASSWORD
MYSQL_DB = config['development'].MYSQL_DB
MYSQL_PORT = config['development'].MYSQL_PORT

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    return MySQLdb.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        port=MYSQL_PORT
    )

# Configuración de Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = ModelUser.get_by_id(conn, user_id)
    conn.close()
    return user

@app.before_first_request
def initialize_database():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Crear la tabla users si no existe
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
          id INT AUTO_INCREMENT PRIMARY KEY,
          username VARCHAR(50) NOT NULL UNIQUE,
          password VARCHAR(255) NOT NULL,
          fullname VARCHAR(100),
          email VARCHAR(100),
          document_type VARCHAR(10),
          identity_number VARCHAR(50),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabla 'users' creada o ya existe.")
    except Exception as ex:
        print(f"Error al inicializar la base de datos: {ex}")
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = User(0, username, password)  # ID no es necesario para la instancia User
        logged_user = ModelUser.login(conn, user)
        conn.close()

        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>This is a protected view, only for authenticated users.</h1>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  # Correcto
        fullname = request.form['fullname']
        email = request.form['email']
        document_type = request.form['document_type']
        identity_number = request.form['identity_number']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """INSERT INTO users (username, password, fullname, email, document_type, identity_number) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (username, password, fullname, email, document_type, identity_number))
            conn.commit()
            flash('User registered successfully!')
            conn.close()
            return redirect(url_for('login'))
        except Exception as ex:
            flash(f"Error in registration: {ex}")
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')


@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def status_404(error):
    return "<h1>Page not found</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)  # Para facilitar la depuración









# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mysqldb import MySQL
# from flask_wtf.csrf import CSRFProtect
# from flask_login import LoginManager, login_user, logout_user, login_required
# from werkzeug.security import generate_password_hash

# from config import config
# from src.models.ModelUser import ModelUser
# from src.models.entities.User import User

# app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

# # Configuración de CSRF
# app.config.from_object(config['development'])
# csrf = CSRFProtect(app)

# # Configuración de MySQL
# app.config['MYSQL_HOST'] = config['development'].MYSQL_HOST
# app.config['MYSQL_USER'] = config['development'].MYSQL_USER
# app.config['MYSQL_PASSWORD'] = config['development'].MYSQL_PASSWORD
# app.config['MYSQL_DB'] = config['development'].MYSQL_DB
# app.config['MYSQL_PORT'] = config['development'].MYSQL_PORT

# db = MySQL(app)
# cursor = db.connection.cursor()
# print(cursor)
# # Configuración de Login
# login_manager_app = LoginManager(app)
# login_manager_app.login_view = 'login'

# @login_manager_app.user_loader
# def load_user(id):
#     return ModelUser.get_by_id(db, id)

# @app.before_first_request
# def initialize_database():
#     try:
#         cursor = db.connection.cursor()
#         # Crear la tabla `user` si no existe
#         create_table_query = '''
#         CREATE TABLE IF NOT EXISTS `user` (
#           `id` smallint(3) UNSIGNED NOT NULL AUTO_INCREMENT,
#           `username` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
#           `password` char(128) COLLATE utf8_unicode_ci NOT NULL,
#           `fullname` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
#           `email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
#           `document_type` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
#           `identity_number` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
#           PRIMARY KEY (`id`)
#         );
#         '''
#         cursor.execute(create_table_query)
#         db.connection.commit()
#         print("Tabla 'user' creada o ya existe.")
#     except Exception as ex:
#         print(f"Error al inicializar la base de datos: {ex}")

# @app.route('/')
# def index():
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = User(0, request.form['username'], request.form['password'])
#         logged_user = ModelUser.login(db, user)
#         if logged_user and logged_user.password:
#             login_user(logged_user)
#             return redirect(url_for('home'))
#         else:
#             flash("Invalid username or password")
#             return render_template('auth/login.html')
#     return render_template('auth/login.html')

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# @app.route('/home')
# def home():
#     return render_template('home.html')

# @app.route('/protected')
# @login_required
# def protected():
#     return "<h1>This is a protected view, only for authenticated users.</h1>"

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Obtener los datos del formulario
#         username = request.form['username']
#         password = generate_password_hash(request.form['password'])
#         fullname = request.form['fullname']
#         email = request.form['email']
#         document_type = request.form['document_type']
#         identity_number = request.form['identity_number']
        
#         try:
#             # Verificar si db no es None
#             if db is None:
#                 print("db is None during registration.")
                
#             # Crear un cursor para ejecutar las consultas
#             cursor = db.connection.cursor()
            
#             # Consulta SQL para insertar un nuevo usuario
#             sql = """INSERT INTO user (username, password, fullname, email, document_type, identity_number) 
#                      VALUES (%s, %s, %s, %s, %s, %s)"""
                     
#             # Ejecutar la consulta con los datos del formulario
#             cursor.execute(sql, (username, password, fullname, email, document_type, identity_number))
            
#             # Confirmar los cambios en la base de datos
#             db.connection.commit()
            
#             # Mostrar un mensaje de éxito y redirigir a la página de inicio de sesión
#             flash('User registered successfully!')
#             return redirect(url_for('login'))
            
#         except Exception as ex:
#             # Mostrar un mensaje de error si ocurre una excepción
#             flash(f"Error in registration: {ex}")
#             return render_template('auth/register.html')
    
#     # Renderizar la página de registro si la solicitud es GET
#     return render_template('auth/register.html')


# #####################################################################################################

# def status_401(error):
#     return redirect(url_for('login'))

# def status_404(error):
#     return "<h1>Page not found</h1>", 404

# if __name__ == '__main__':
#     app.config.from_object(config['development'])
#     csrf.init_app(app)
#     app.register_error_handler(401, status_401)
#     app.register_error_handler(404, status_404)
#     app.run(debug=True)  # Para facilitar la depuración
