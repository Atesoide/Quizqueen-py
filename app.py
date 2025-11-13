import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector
from server.db import crear_tabla_usuarios, agregar_usuario, obtener_usuario_por_email, obtener_usuario_por_id

# --- Configuración Inicial ---
app = Flask(__name__, template_folder='client/templates')
app.secret_key = os.environ.get('SECRET_KEY', 'una_clave_de_desarrollo_insegura') 
bcrypt = Bcrypt(app)
crear_tabla_usuarios()

# Database configuration
db_config = {
    'user': 'root',
    'password': 'toor',
    'host': '127.0.0.1',
    'database': 'quizqueen',
    'auth_plugin': 'mysql_native_password'  # Add this line
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Difficulty settings (from your Node.js code)
DIFFICULTY_SETTINGS = {
    1: {'health': 15, 'length': 5},
    2: {'health': 30, 'length': 10},
    3: {'health': 45, 'length': 15}
}

# Helper function to escape HTML (from your Node.js code) - FIXED
def escape_html(text):
    if not text:
        return ''
    html_escape_map = {
        '&': '&amp;',
        '<': '&lt;', 
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }
    
    # Python version - replace characters one by one
    result = ""
    for char in text:
        result += html_escape_map.get(char, char)
    return result

# --- Decorador de Autenticación ---
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rutas Públicas ---

@app.route('/')
def home():
    if session.get('logged_in'):
        user_id = session.get('user_id')
        user_data = obtener_usuario_por_id(user_id)
        return render_template('auth/home.html', user=user_data)
    else:
        return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# --- Rutas de Autenticación ---

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("=== SIGNUP ROUTE CALLED ===")
    
    if request.method == 'POST':
        print("=== POST REQUEST DETECTED ===")
        print("All form data:", dict(request.form))
        
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        
        print(f"Extracted values - Nombre: '{nombre}', Correo: '{correo}', Password: {'*' * len(password)}, Confirm: {'*' * len(confirm_password)}")
        
        # Validate required fields
        if not nombre:
            print("VALIDATION FAILED: No nombre")
            flash('Full name is required', 'error')
            return render_template('signup.html')
        
        if not correo:
            print("VALIDATION FAILED: No correo")
            flash('Email is required', 'error')
            return render_template('signup.html')
            
        if not password:
            print("VALIDATION FAILED: No password")
            flash('Password is required', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            print("VALIDATION FAILED: Passwords don't match")
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        print("Checking if user exists...")
        existing_user = obtener_usuario_por_email(correo)
        print(f"Existing user query result: {existing_user}")
        
        if existing_user:
            print("VALIDATION FAILED: User already exists")
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        print("Creating password hash...")
        try:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            print(f"Password hash created successfully: {password_hash[:20]}...")
        except Exception as e:
            print(f"ERROR creating password hash: {e}")
            flash('Error creating account', 'error')
            return render_template('signup.html')
        
        print("Adding user to database...")
        user_id = agregar_usuario(nombre, correo, password_hash)
        print(f"Database returned user_id: {user_id}")
        
        if user_id:
            print("SIGNUP SUCCESSFUL!")
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            print("SIGNUP FAILED: Database error")
            flash('Error creating account. Please try again.', 'error')
    else:
        print("GET request - rendering signup form")
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '')
        
        if not correo or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        user = obtener_usuario_por_email(correo)
        print(f"DEBUG - User found: {user}")  # Add this debug line
        
        if user:
            # DEBUG: Print all keys in the user dictionary
            print(f"DEBUG - User keys: {user.keys()}")
            print(f"DEBUG - User data: {user}")
            
            # Try different possible column names
            password_hash = user.get('password') or user.get('password') or user.get('password_hash')
            
            if password_hash and bcrypt.check_password_hash(password_hash, password):
                session['user_id'] = user['id']
                session['user_name'] = user['nombre']
                session['logged_in'] = True
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                print(f"DEBUG - Password check failed or no password field")
                flash('Invalid email or password', 'error')
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Quiz Routes (Converted from Node.js) ---

@app.route('/selector')
@login_required
def selector():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all quiz tables
        cursor.execute("SHOW TABLES LIKE 'cuestionario_%'")
        tables = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return render_template('quizselector.html', tables=tables)
        
    except Exception as error:
        print('Error fetching tables:', error)
        return f'Database error: {error}', 500

@app.route('/quiz')
@login_required
def quiz():
    try:
        quiz_table = request.args.get('quiz', 'cuestionario_un')
        difficulty = max(1, min(3, int(request.args.get('difficulty', 1))))
        
        print(f'Loading quiz: {quiz_table}, difficulty: {difficulty}')
        
        # Validate table name
        if not all(c.isalnum() or c == '_' for c in quiz_table):
            return 'Invalid table name', 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if table exists
        cursor.execute(f"SHOW TABLES LIKE '{quiz_table}'")
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            return f'Quiz not found: {quiz_table}', 404
        
        # Get questions
        cursor.execute(f"""
            SELECT id, pregunta, respuesta_1, respuesta_2, respuesta_3, respuesta_4, respuesta_correcta 
            FROM {quiz_table}
        """)
        questions = cursor.fetchall()
        
        print(f'Found {len(questions)} questions')
        
        # Generate HTML table for debugging (optional)
        question_table = ''
        if questions:
            question_table = '<table class="toHide" id="questionTable" border="1" cellpadding="8" cellspacing="0">' \
                '<thead><tr><th>ID</th><th>Pregunta</th><th>Respuesta 1</th><th>Respuesta 2</th>' \
                '<th>Respuesta 3</th><th>Respuesta 4</th><th>Correcta</th></tr></thead><tbody>'
            
            for row in questions:
                question_table += f'''<tr>
                    <td>{row['id']}</td>
                    <td>{escape_html(row['pregunta'])}</td>
                    <td>{escape_html(row['respuesta_1'])}</td>
                    <td>{escape_html(row['respuesta_2'])}</td>
                    <td>{escape_html(row['respuesta_3'])}</td>
                    <td>{escape_html(row['respuesta_4'])}</td>
                    <td>{row['respuesta_correcta']}</td>
                </tr>'''
            
            question_table += '</tbody></table>'
        else:
            question_table = '<p>No se encontraron resultados.</p>'
        
        cursor.close()
        conn.close()
        
        return render_template('quiz.html',
            quiz_table=quiz_table,
            difficulty=difficulty,
            health=DIFFICULTY_SETTINGS[difficulty]['health'],
            length=DIFFICULTY_SETTINGS[difficulty]['length'],
            question_table=question_table
        )
        
    except Exception as error:
        print('Error loading quiz:', error)
        return f'Error loading quiz: {error}', 500

@app.route('/quiz_results')
@login_required
def quiz_results():
    return render_template('quizresults.html')

@app.route('/leaderboards')
@login_required
def leaderboards():
    return render_template('leaderboard.html')

@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    user_data = obtener_usuario_por_id(user_id)
    return render_template('profile.html', user=user_data)

@app.route('/suggestions')
@login_required
def suggestions():
    return render_template('suggestions.html')

@app.route('/game_over')
@login_required
def game_over():
    quiz_table = request.args.get('quiz', 'cuestionario_un')
    return render_template('gameover.html', quiz_table=quiz_table)

@app.route('/settings')
@login_required 
def settings():
    user_id = session.get('user_id')
    user_data = obtener_usuario_por_id(user_id)
    return render_template('auth/settings.html', user=user_data)


@app.route('/test-db')
def test_db():
    """Test database connection and table structure"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if usuarios table exists and has data
        cursor.execute("SHOW TABLES LIKE 'usuarios'")
        table_exists = cursor.fetchone()
        print(f"Table exists: {table_exists}")
        
        # Check table structure
        cursor.execute("DESCRIBE usuarios")
        columns = cursor.fetchall()
        print("Table columns:", columns)
        
        # Check if any users exist
        cursor.execute("SELECT COUNT(*) as count FROM usuarios")
        user_count = cursor.fetchone()
        print(f"Total users: {user_count['count']}")
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'table_exists': bool(table_exists),
            'columns': columns,
            'user_count': user_count['count']
        })
        
    except Exception as e:
        print(f"Database test error: {e}")
        return f"Database error: {e}", 500


# --- API Routes for Quiz Functionality ---



@app.route('/api/questions/<quiz_table>')
@login_required
def api_questions(quiz_table):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(f"""
            SELECT id, pregunta, respuesta_1, respuesta_2, respuesta_3, respuesta_4, respuesta_correcta 
            FROM {quiz_table}
        """)
        questions = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(questions)
        
    except Exception as error:
        return jsonify({'error': str(error)}), 500

# --- Inicio del Servidor ---
if __name__ == '__main__':
    app.run(debug=True)
