from werkzeug.security import generate_password_hash

password = "my_password"
hashed_password = generate_password_hash(password)
print(hashed_password)
print(len(hashed_password))  # Esto te dará la longitud del hash generado