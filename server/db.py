# server/db.py
import mysql.connector
from mysql.connector import errorcode

# Configuración de la conexión MySQL
db_config = {
    'user': 'root',
    'password': 'toor',
    'host': 'localhost',
    'database': 'quizqueen'
}

def crear_tabla_usuarios():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        # TABLA DE USUARIOS ACTUALIZADA CON EL CAMPO password_hash
        crear_tabla = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fname VARCHAR(50) NOT NULL,
            lastname VARCHAR(50),
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL 
        )
        """
        cursor.execute(crear_tabla)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Tabla 'users' creada o ya existe.")
    except mysql.connector.Error as err:
        print("Error al crear la tabla:", err)

# La función ahora acepta y guarda el hash de la contraseña
def agregar_usuario(fname, email, password_hash): 
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        insertar_usuario = "INSERT INTO usuarios (nombre, correo, contraseña) VALUES (%s, %s,%s, %s)"
        cursor.execute(insertar_usuario, (fname, email, password_hash))
        cnx.commit()
        last_id = cursor.lastrowid # Obtener el ID del nuevo usuario
        cursor.close()
        cnx.close()
        return last_id
    except mysql.connector.Error as err:
        print("Error al agregar usuario:", err)
        return None

def obtener_usuario_por_email(email):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        cnx.close()
        return usuario
    except mysql.connector.Error as err:
        print("Error al obtener usuario:", err)
        return None

def obtener_usuario_por_id(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT id, fname, lastname, email FROM users WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        cnx.close()
        return usuario
    except mysql.connector.Error as err:
        print("Error al obtener usuario por ID:", err)
        return None