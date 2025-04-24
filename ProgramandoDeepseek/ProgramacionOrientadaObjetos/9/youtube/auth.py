from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Definir el alcance de la API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
# Variable global
credenciales_path = 'token.json'

def autenticar_usuario():
    creds = None

    # Archivo para guardar credenciales (simula cookies persistentes)
    #credenciales_path = 'token.json'

    # Si ya existen credenciales persistentes, las cargamos
    if os.path.exists(credenciales_path):
        creds = Credentials.from_authorized_user_file(credenciales_path, SCOPES)
        print("Credenciales cargadas desde token.json")
    else:
        # Si no hay credenciales, iniciar el flujo de OAuth2
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)  # Abre navegador para login

        # Guardar credenciales para uso futuro
        with open(credenciales_path, 'w') as token_file:
            token_file.write(creds.to_json())
        print("Credenciales guardadas en token.json")

    return creds

def cerrar_sesion_usuario():
    # Archivo de credenciales (token.json)
    #credenciales_path = 'token.json'

    # Verificar si el archivo existe
    if os.path.exists(credenciales_path):
        os.remove(credenciales_path)  # Eliminar el archivo
        print("Sesión cerrada. Credenciales eliminadas.")
    else:
        print("No hay sesión activa para cerrar.")