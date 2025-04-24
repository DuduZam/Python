import os  # Importa el módulo 'os' para interactuar con el sistema operativo.
import pickle  # Importa el módulo 'pickle' para serializar y deserializar objetos de Python.
import json  # Importa el módulo 'json' para trabajar con datos JSON.

from google_auth_oauthlib.flow import InstalledAppFlow  # Importa la clase 'InstalledAppFlow' para el flujo de autenticación OAuth 2.0.
from googleapiclient.discovery import build  # Importa la función 'build' para construir el objeto de servicio de la API de YouTube.
from google.auth.transport.requests import Request  # Importa la clase 'Request' para refrescar tokens de acceso.

def obtener_credenciales():
    """Obtiene y guarda las credenciales de la API de YouTube."""
    creds = None  # Inicializa la variable 'creds' como 'None'.
    # El archivo token.pickle guarda los tokens de acceso y actualización, y
    # se actualiza automáticamente cuando los tokens son válidos.
    if os.path.exists('token.pickle'):  # Verifica si el archivo 'token.pickle' existe en el directorio actual.
        with open('token.pickle', 'rb') as token:  # Abre el archivo 'token.pickle' en modo de lectura binaria ('rb').
            creds = pickle.load(token)  # Carga las credenciales desde el archivo 'token.pickle' usando 'pickle.load()'.
    # Si no hay credenciales disponibles o son inválidas, el usuario debe
    # iniciar sesión.
    if not creds or not creds.valid:  # Verifica si 'creds' es 'None' o si las credenciales no son válidas.
        if creds and creds.expired and creds.refresh_token:  # Verifica si las credenciales existen, han expirado y tienen un token de actualización.
            creds.refresh(Request())  # Refresca las credenciales usando 'creds.refresh()'.
        else:
            # Carga las credenciales desde el archivo JSON proporcionado por el usuario.
            with open('client_secret.json', 'r') as f:  # Abre el archivo 'client_secret.json' en modo de lectura ('r').
                client_config = json.load(f)  # Carga el contenido del archivo JSON usando 'json.load()'.
            # Inicia el flujo de autenticación OAuth 2.0.
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', ['https://www.googleapis.com/auth/youtube.readonly'])  # Crea un objeto 'InstalledAppFlow' desde el archivo 'client_secret.json'.
            creds = flow.run_local_server(port=0)  # Inicia el servidor local para la autenticación y obtiene las credenciales.
        # Guarda las credenciales para la próxima ejecución.
        with open('token.pickle', 'wb') as token:  # Abre el archivo 'token.pickle' en modo de escritura binaria ('wb').
            pickle.dump(creds, token)  # Guarda las credenciales en el archivo 'token.pickle' usando 'pickle.dump()'.
    return creds  # Devuelve las credenciales.

def obtener_suscripciones(youtube):
    """Obtiene la lista de suscripciones del usuario, manejando la paginación."""
    subscriptions = []  # Inicializa una lista vacía llamada 'subscriptions' para almacenar los resultados de las suscripciones.
    next_page_token = None  # Inicializa la variable 'next_page_token' como 'None'. Esta variable almacenará el token para la siguiente página de resultados.
    while True:  # Inicia un bucle 'while' infinito que se ejecutará hasta que se encuentre una condición de salida.
        request = youtube.subscriptions().list(  # Crea una solicitud para obtener la lista de suscripciones del usuario.
            part='snippet,contentDetails',  # Especifica las partes de la respuesta que se deben incluir: 'snippet' para información básica del canal y 'contentDetails' para detalles adicionales.
            mine=True,  # Indica que se deben obtener las suscripciones del usuario autenticado.
            maxResults=50,  # Especifica el número máximo de resultados por página (50 en este caso).
            pageToken=next_page_token  # Incluye el token de la página anterior si existe. Esto permite obtener las páginas subsiguientes.
        )
        response = request.execute()  # Ejecuta la solicitud y almacena la respuesta en la variable 'response'.
        for item in response['items']:  # Itera sobre cada elemento en la lista 'items' de la respuesta. Cada elemento representa una suscripción.
            channel_title = item['snippet']['title']  # Obtiene el título del canal de la suscripción actual.
            channel_id = item['snippet']['resourceId']['channelId']  # Obtiene el ID del canal de la suscripción actual.
            channel_response = youtube.channels().list(  # Crea una solicitud para obtener información del canal.
                part='statistics',  # Especifica que se deben obtener las estadísticas del canal.
                id=channel_id  # Especifica el ID del canal del que se deben obtener las estadísticas.
            ).execute()  # Ejecuta la solicitud y almacena la respuesta en la variable 'channel_response'.
            subscriber_count = channel_response['items'][0]['statistics']['subscriberCount']  # Obtiene el número de suscriptores del canal.
            subscriptions.append((channel_title, subscriber_count))  # Agrega el título del canal y el número de suscriptores a la lista 'subscriptions'.
        next_page_token = response.get('nextPageToken')  # Obtiene el token para la siguiente página de resultados, si existe.
        if not next_page_token:  # Verifica si no hay un token para la siguiente página.
            break  # Si no hay un token, significa que no hay más páginas, por lo que se sale del bucle 'while'.
    return subscriptions  # Devuelve la lista 'subscriptions', que contiene información sobre todas las suscripciones del usuario.

def mostrar_suscripciones(subscriptions):
    """Muestra la lista de suscripciones en la consola."""
    # Itera sobre la lista de suscripciones y muestra el título y el número de suscriptores de cada canal.
    for i, (title, count) in enumerate(subscriptions, 1):  # Itera sobre la lista de suscripciones.
        print(f'{i}. "{title}", "{count}" suscriptores')  # Imprime el título del canal y el número de suscriptores.

def main():
    """Función principal para ejecutar el script."""
    # Obtiene las credenciales de la API de YouTube.
    credenciales = obtener_credenciales()  # Llama a la función 'obtener_credenciales()' para obtener las credenciales.
    # Crea un objeto de servicio de YouTube.
    youtube = build('youtube', 'v3', credentials=credenciales)  # Crea un objeto de servicio de YouTube usando las credenciales.
    # Obtiene la lista de suscripciones del usuario.
    suscripciones = obtener_suscripciones(youtube)  # Llama a la función 'obtener_suscripciones()' para obtener la lista de suscripciones.
    # Muestra la lista de suscripciones en la consola.
    mostrar_suscripciones(suscripciones)  # Llama a la función 'mostrar_suscripciones()' para mostrar la lista de suscripciones.

if __name__ == '__main__':  # Verifica si el script se está ejecutando como el programa principal.
    main()  # Llama a la función 'main()' para ejecutar el script.