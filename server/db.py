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
    
# Add these functions to your db.py

def crear_tabla_sugerencias():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        crear_tabla = """
        CREATE TABLE IF NOT EXISTS sugerencias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            tipo ENUM('pregunta', 'cuestionario') NOT NULL,
            titulo VARCHAR(200),
            pregunta TEXT,
            respuesta_1 VARCHAR(200),
            respuesta_2 VARCHAR(200),
            respuesta_3 VARCHAR(200),
            respuesta_4 VARCHAR(200),
            respuesta_correcta INT,
            descripcion TEXT,
            estado ENUM('pendiente', 'revisado', 'implementado', 'rechazado') DEFAULT 'pendiente',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE SET NULL
        )
        """
        cursor.execute(crear_tabla)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Tabla 'sugerencias' creada o ya existe.")
    except mysql.connector.Error as err:
        print("Error al crear la tabla sugerencias:", err)

def agregar_sugerencia(user_id, tipo, titulo=None, pregunta=None, respuesta_1=None, 
                      respuesta_2=None, respuesta_3=None, respuesta_4=None, 
                      respuesta_correcta=None, descripcion=None):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        insertar_sugerencia = """
        INSERT INTO sugerencias 
        (user_id, tipo, titulo, pregunta, respuesta_1, respuesta_2, respuesta_3, respuesta_4, respuesta_correcta, descripcion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insertar_sugerencia, (
            user_id, tipo, titulo, pregunta, respuesta_1, 
            respuesta_2, respuesta_3, respuesta_4, respuesta_correcta, descripcion
        ))
        
        cnx.commit()
        last_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return last_id
    except mysql.connector.Error as err:
        print("Error al agregar sugerencia:", err)
        return None

def obtener_sugerencias_por_usuario(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, tipo, titulo, pregunta, estado, fecha_creacion
            FROM sugerencias 
            WHERE user_id = %s 
            ORDER BY fecha_creacion DESC
        """, (user_id,))
        
        sugerencias = cursor.fetchall()
        cursor.close()
        cnx.close()
        return sugerencias
    except mysql.connector.Error as err:
        print("Error al obtener sugerencias:", err)
        return None
    
    # Add these functions to your db.py

def crear_tabla_leaderboard():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        crear_tabla = """
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            quiz_name VARCHAR(100) NOT NULL,
            difficulty INT NOT NULL,
            correct_answers INT NOT NULL,
            total_questions INT NOT NULL,
            score INT NOT NULL,
            remaining_health INT NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            INDEX idx_score (score DESC),
            INDEX idx_user_id (user_id),
            INDEX idx_quiz_difficulty (quiz_name, difficulty)
        )
        """
        cursor.execute(crear_tabla)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Tabla 'leaderboard' creada o ya existe.")
    except mysql.connector.Error as err:
        print("Error al crear la tabla leaderboard:", err)

def agregar_resultado_leaderboard(user_id, quiz_name, difficulty, correct_answers, total_questions, remaining_health):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        # Calculate score (you can adjust this formula)
        base_score = correct_answers * 100
        difficulty_multiplier = difficulty  # 1, 2, or 3
        health_bonus = remaining_health * 10
        
        score = (base_score * difficulty_multiplier) + health_bonus
        
        insertar_resultado = """
        INSERT INTO leaderboard 
        (user_id, quiz_name, difficulty, correct_answers, total_questions, score, remaining_health)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insertar_resultado, (
            user_id, quiz_name, difficulty, correct_answers, 
            total_questions, score, remaining_health
        ))
        
        cnx.commit()
        last_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return last_id
    except mysql.connector.Error as err:
        print("Error al agregar resultado al leaderboard:", err)
        return None

def obtener_leaderboard_top(limit=50, quiz_filter=None, difficulty_filter=None):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        
        query = """
        SELECT 
            lb.score,
            lb.quiz_name,
            lb.difficulty,
            lb.correct_answers,
            lb.total_questions,
            lb.remaining_health,
            lb.completed_at,
            u.nombre as user_name
        FROM leaderboard lb
        JOIN usuarios u ON lb.user_id = u.id
        """
        
        conditions = []
        params = []
        
        if quiz_filter:
            conditions.append("lb.quiz_name = %s")
            params.append(quiz_filter)
        
        if difficulty_filter:
            conditions.append("lb.difficulty = %s")
            params.append(difficulty_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY lb.score DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        cursor.close()
        cnx.close()
        return resultados
    except mysql.connector.Error as err:
        print("Error al obtener leaderboard:", err)
        return None

def obtener_mejor_puntuacion_usuario(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                MAX(score) as best_score,
                COUNT(*) as games_played,
                AVG(score) as average_score
            FROM leaderboard 
            WHERE user_id = %s
        """, (user_id,))
        
        stats = cursor.fetchone()
        cursor.close()
        cnx.close()
        return stats
    except mysql.connector.Error as err:
        print("Error al obtener estadísticas del usuario:", err)
        return None