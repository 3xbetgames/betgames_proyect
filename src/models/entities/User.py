from werkzeug.security import check_password_hash
from flask_login import UserMixin

# Definición de la clase User que hereda de UserMixin
class User(UserMixin):

    # Constructor de la clase User que inicializa los atributos del usuario
    def __init__(self, id, username, password, fullname="", email="", document_type="", identity_number="") -> None:
        # Atributos del usuario
        self.id = id  # Identificador único del usuario
        self.username = username  # Nombre de usuario
        self.password = password  # Contraseña cifrada (hash)
        self.fullname = fullname  # Nombre completo del usuario (opcional)
        self.email = email  # Correo electrónico del usuario (opcional)
        self.document_type = document_type  # Tipo de documento del usuario (opcional)
        self.identity_number = identity_number  # Número de identificación (opcional)

    # Método de clase para verificar la contraseña
    @classmethod
    def check_password(cls, hashed_password, password):
        # Utiliza check_password_hash para comparar la contraseña cifrada con la ingresada
        # Devuelve True si coinciden, False en caso contrario
        return check_password_hash(hashed_password, password)
