# server/db.py
import mysql.connector
from mysql.connector import errorcode
import bcrypt

# Configuración de la conexión MySQL
db_config = {
    'user': 'root',
    'password': 'toor',
    'host': '127.0.0.1',
    'database': 'quizqueen',
    'auth_plugin': 'mysql_native_password'  # Add this line
}

def crear_tabla_usuarios():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        # CORREGIDO: Usar los nombres de columnas correctos
        crear_tabla = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL 
        )
        """
        cursor.execute(crear_tabla)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Tabla 'usuarios' creada o ya existe.")
    except mysql.connector.Error as err:
        print("Error al crear la tabla:", err)

# CORREGIDO: Usar los nombres de columnas correctos
def agregar_usuario(nombre, correo, password_hash): 
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        # CORREGIDO: Los nombres de columnas deben coincidir con la tabla
        insertar_usuario = "INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)"
        cursor.execute(insertar_usuario, (nombre, correo, password_hash))
        cnx.commit()
        last_id = cursor.lastrowid # Obtener el ID del nuevo usuario
        cursor.close()
        cnx.close()
        return last_id
    except mysql.connector.Error as err:
        print("Error al agregar usuario:", err)
        return None

def obtener_usuario_por_email(correo):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        # CORREGIDO: Buscar en la tabla 'usuarios' no 'users'
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
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
        # CORREGIDO: Buscar en la tabla 'usuarios' no 'users'
        cursor.execute("SELECT id, nombre, correo FROM usuarios WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        cnx.close()
        return usuario
    except mysql.connector.Error as err:
        print("Error al obtener usuario por ID:", err)
        return None