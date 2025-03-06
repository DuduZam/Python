# Importamos las librerías esenciales
from flask import Flask, jsonify, request  # Flask para el servidor web
from flask_sqlalchemy import SQLAlchemy  # ORM para bases de datos
from flask_jwt_extended import JWTManager, create_access_token  # Autenticación JWT
import cloudinary  # Para manejar almacenamiento en la nube
import cloudinary.uploader  # Subida de archivos
import os  # Manejo de variables de entorno
from datetime import timedelta  # Para manejar tiempos de expiración
from dotenv import load_dotenv  # Cargar variables de entorno desde .env
from datetime import datetime, timedelta

load_dotenv()  # Carga las variables del archivo .env

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Configuramos la base de datos usando SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # URL de la DB desde .env
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')  # Clave secreta para JWT
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # Los tokens expiran en 24h

db = SQLAlchemy(app)  # Conectamos la DB a la app
jwt = JWTManager(app)  # Inicializamos el sistema de JWT

# Configuración de Cloudinary (servicio de almacenamiento)
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Definimos el modelo de Usuario para la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único
    password = db.Column(db.String(80), nullable=False)  # Contraseña (¡debería ser un hash!)

# Ruta para registro de usuarios
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Obtenemos datos del request JSON
    # Validación básica (¡deberías agregar más!)
    new_user = User(email=data['email'], password=data['password'])  # Creamos usuario
    db.session.add(new_user)  # Añadimos a la sesión de la DB
    db.session.commit()  # Guardamos en la DB
    return jsonify({"msg": "User created"}), 201  # Respuesta exitosa

# Ruta para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()  # Buscamos usuario por email
    if user and user.password == data['password']:  # Validamos contraseña (¡usa bcrypt en producción!)
        access_token = create_access_token(identity=user.id)  # Generamos token JWT
        return jsonify(access_token=access_token)  # Devolvemos el token
    return jsonify({"msg": "Bad credentials"}), 401  # Error si credenciales son inválidas

# Ruta para subir archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    
    # Calcula la fecha de expiración (24 horas desde ahora)
    expiration_time = datetime.now() + timedelta(hours=24)
    expires_at = int(expiration_time.timestamp())  # Convertir a timestamp Unix
    
    # Sube a Cloudinary con expiración
    result = cloudinary.uploader.upload(
        file,
        resource_type="auto",
        upload_preset="family_media_auto_delete",  # Nombre de tu preset
        expires_at=expires_at  # ¡Este parámetro activa el auto-delete!
    )
    
    return jsonify({"url": result['secure_url'], "expires_at": expires_at}), 200

if __name__ == '__main__':
    db.create_all()  # Crea las tablas en la DB si no existen
    app.run(debug=True)  # Inicia el servidor en modo desarrollo