import os
from flask import Flask, render_template, request, redirect, url_for, session, flash  # Added flash import
from flask_bcrypt import Bcrypt
from server.db import crear_tabla_usuarios, agregar_usuario, obtener_usuario_por_email, obtener_usuario_por_id

# --- Configuración Inicial ---
app = Flask(__name__, template_folder='client/templates')
# CLAVE SECRETA: NECESARIA PARA CIFRAR LAS COOKIES DE SESIÓN
app.secret_key = os.environ.get('SECRET_KEY', 'una_clave_de_desarrollo_insegura') 
bcrypt = Bcrypt(app)
# Ejecutamos la creación de la tabla al inicio (si no existe)
crear_tabla_usuarios() 

# --- Decorador de Autenticación (Middleware) ---
def login_required(f):
    """Decorador para restringir el acceso si no hay sesión activa."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            # Si no hay sesión, redirige al login
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rutas Públicas (Enrutamiento Estático) ---

@app.route('/about')
def about():
    # Estas vistas usan el navbar público si la sesión está cerrada
    return render_template('about.html')

@app.route('/contact')
def contact():
    # Estas vistas usan el navbar público si la sesión está cerrada
    return render_template('contact.html')

# --- Rutas de Autenticación (Login/Signup) ---

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Use .get() to avoid BadRequestKeyError
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')
        confirm_password = request.form.get('confirmPassword', '')
        
        # Validate required fields
        if not nombre:
            flash('Full name is required', 'error')
            return render_template('signup.html')
        
        if not correo:
            flash('Email is required', 'error')
            return render_template('signup.html')
            
        if not contraseña:
            flash('Password is required', 'error')
            return render_template('signup.html')
        
        # Check if passwords match
        if contraseña != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        # Check if user already exists
        existing_user = obtener_usuario_por_email(correo)
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        # FIXED: Use flask_bcrypt correctly
        password_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')
        
        # Add user to database
        user_id = agregar_usuario(nombre, correo, password_hash)
        if user_id:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error creating account. Please try again.', 'error')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Use .get() to avoid BadRequestKeyError
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')
        
        if not correo or not contraseña:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        # Get user from database
        user = obtener_usuario_por_email(correo)
        # FIXED: Use flask_bcrypt correctly
        if user and bcrypt.check_password_hash(user['contraseña'], contraseña):
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            session['logged_in'] = True  # Added this missing session variable
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Changed to 'home' route
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Cierra la sesión (elimina todas las claves)
    session.clear()
    # Redirige al login
    return redirect(url_for('login'))


# --- Rutas Protegidas y Dinámicas ---

@app.route('/')
def home():
    # 1. Verificar si la sesión está abierta
    if session.get('logged_in'):
        # SESIÓN ABIERTA: Mostrar contenido privado (home.html)
        user_id = session.get('user_id')
        user_data = obtener_usuario_por_id(user_id)
        
        # Renderiza la vista de sesión
        return render_template('auth/home.html', user=user_data)
    else:
        # SESIÓN CERRADA: Mostrar contenido público (index.html)
        # Asumimos que index.html es la página pública de bienvenida
        return render_template('index.html')


@app.route('/settings')
@login_required 
def settings():
    user_id = session.get('user_id')
    user_data = obtener_usuario_por_id(user_id)
    
    # RENDERIZA LA NUEVA PLANTILLA DENTRO DE AUTH/
    return render_template('auth/settings.html', user=user_data)


# --- Inicio del Servidor ---
if __name__ == '__main__':
    app.run(debug=True)

