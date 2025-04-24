from googleapiclient.discovery import build

def obtener_estadisticas_youtube(creds):
    # Construir el cliente de la API
        youtube = build('youtube', 'v3', credentials=creds)

        # Hacer una solicitud a la API para obtener datos del canal
        request = youtube.channels().list(
            part='snippet,statistics',
            mine=True
        )
        response = request.execute()

        # Imprimir los datos del canal
        for item in response['items']:
            print(f"Nombre del canal: {item['snippet']['title']}")
            print(f"Suscriptores: {item['statistics']['subscriberCount']}")
            print(f"Visualizaciones totales: {item['statistics']['viewCount']}")
