# Importación de librerías
import tkinter as tk
from tkinter import ttk, filedialog, messagebox  # Componentes GUI
from googleapiclient.discovery import build       # API de YouTube
from google_auth_oauthlib.flow import InstalledAppFlow  # Autenticación OAuth
from google.auth.transport.requests import Request  # Refresh tokens
import os  # Manejo de sistema de archivos
import pickle  # Serialización de credenciales
from PIL import Image, ImageTk  # Procesamiento de imágenes
import requests  # Descarga de thumbnails
from io import BytesIO  # Manejo de bytes para imágenes

# Permisos requeridos para la API de YouTube
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

class YouTubeUnsubscriber:
    def __init__(self, root):
        # Inicialización de la ventana principal
        self.root = root
        self.root.title("YouTube Unsubscriber")
        
        # Variables de estado
        self.credentials_path = None  # Ruta de credenciales JSON
        self.service = None  # Servicio de YouTube API
        self.images = []  # Almacenamiento de imágenes de thumbnails
        self.canvas_height = 500  # Altura fija del área de visualización
        self.y_offset = 10  # Posición vertical inicial en el canvas
        self.total_height = 0  # Altura total del contenido
        self.scroll_position = 0  # Posición actual del scroll
        
        self.create_widgets()  # Construcción de la interfaz

    def authenticate(self):
        # Manejo del flujo de autenticación OAuth2
        creds = None
        if os.path.exists("token.pickle"):
            # Cargar credenciales existentes
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refrescar token expirado
                creds.refresh(Request())
            else:
                # Iniciar nuevo flujo de autenticación
                if not self.credentials_path:
                    messagebox.showwarning("Error", "Debe seleccionar un archivo de credenciales JSON")
                    return
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    messagebox.showerror("Error de autenticación", f"No se pudo autenticar: {e}")
                    return
                
                # Guardar credenciales para futuros usos
                with open("token.pickle", "wb") as token:
                    pickle.dump(creds, token)
        
        # Crear servicio de YouTube API
        self.service = build("youtube", "v3", credentials=creds)
        self.fetch_subscriptions()  # Obtener suscripciones después de autenticar

    def load_credentials(self):
        # Diálogo para seleccionar archivo de credenciales
        self.credentials_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if self.credentials_path:
            self.authenticate()  # Iniciar autenticación
    
    def resize_image(self, image_path, width, height):
        """Redimensiona una imagen a las dimensiones especificadas."""
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height), Image.LANCZOS)  # Usa LANCZOS para mejor calidad
        return ImageTk.PhotoImage(resized_image)

    def create_widgets(self):
        # Construcción de la interfaz gráfica
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.grid(row=0, column=0)                

        # Carga de íconos (rutas absolutas temporales)
        ruta_refresh = os.path.abspath("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\YTSubReaper\\refresh.png")
        ruta_info = os.path.abspath("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\YTSubReaper\\info.png")
        # Llamar a la funcion para cambiar tamaño de imagen
        self.refresh_icon = self.resize_image(ruta_refresh, 20, 20)
        self.info_icon = self.resize_image(ruta_info, 20, 20)

        # Botón 1: Icono Informacion
        self.info_button = ttk.Button(self.frame, image=self.info_icon, command=self.show_info)
        self.info_button.grid(row=1, column=0, pady=2)  # Fila 1

        # Botón 2: Cargar Credenciales JSON
        self.upload_button = ttk.Button(self.frame, text="Cargar Credenciales JSON", command=self.load_credentials)
        self.upload_button.grid(row=1, column=1, columnspan=2, pady=2)  # Fila 1, columnspan=2

        # Botón 3: Icono Refresh
        self.refresh_button = ttk.Button(self.frame, image=self.refresh_icon, command=self.fetch_subscriptions)
        self.refresh_button.grid(row=1, column=3, pady=2)  # Fila 1

        # Canvas para mostrar suscripciones
        self.canvas = tk.Canvas(self.frame, width=500, height=self.canvas_height, bg="white")
        self.canvas.grid(row=2, column=0, columnspan=5, pady=10)  # Fila 2

        # Botón de desuscripción
        self.unsubscribe_button = ttk.Button(self.frame, text="Desuscribirse", command=self.unsubscribe_selected)
        self.unsubscribe_button.grid(row=3, column=2, pady=5)  # Fila 3        

    def fetch_subscriptions(self):
        # Obtener lista de suscripciones desde YouTube API
        if not self.service: #Primero, verifica si la aplicación ya se ha autenticado con YouTube. self.service es una variable que almacena el "servicio" de la API de YouTube, que se necesita para hacer solicitudes a la API.
            messagebox.showwarning("Error", "Debe autenticarse primero.")
            return
        
        try:
            subscriptions = []
            # Solicitud a la API
            request = self.service.subscriptions().list(part="snippet",
                                                        mine=True,
                                                        maxResults=50                                                        
                                                        )            
            # Crea una solicitud a la API de YouTube para obtener la lista de tus suscripciones.
            #part="snippet": Especifica que queremos obtener información sobre los "fragmentos" de las suscripciones (títulos, thumbnails, etc.).
            #mine=True: Indica que queremos obtener las suscripciones del usuario autenticado.
            #maxResults=50: Limita el número de resultados a 50.
            while request:
                response = request.execute() # Envía la solicitud a la API y obtiene la respuesta.
                subscriptions.extend(response.get("items", []))
                request = self.service.subscriptions().list_next(request, response)
            
            self.canvas.delete("all")
            self.images.clear()
            self.subscriptions = {}
            self.y_offset = 10
            
            for item in subscriptions:
                title = item["snippet"]["title"]
                channel_id = item["snippet"]["resourceId"]["channelId"]
                thumbnail_url = item["snippet"]["thumbnails"]["default"]["url"]
                self.subscriptions[title] = channel_id
                
                try:
                    # Descargar y mostrar thumbnail
                    response = requests.get(thumbnail_url)
                    img_data = Image.open(BytesIO(response.content))
                    img_data = img_data.resize((50, 50), Image.LANCZOS)  # Redimensionar
                    img = ImageTk.PhotoImage(img_data)
                    self.images.append(img)  # Mantener referencia
                    
                    # Crear un Frame para cada canal
                    channel_frame = ttk.Frame(self.canvas)
                    channel_frame.pack(side="top", fill="x", pady=5)

                    # Mostrar thumbnail
                    thumbnail_label = ttk.Label(channel_frame, image=img)
                    thumbnail_label.grid(row = 0 , column = 0)

                    # Mostrar título
                    title_label = ttk.Label(channel_frame, text=title)
                    title_label.grid(row = 0 , column = 1 , padx = 10)

                    # Insertar el Frame en el Canvas
                    self.canvas.create_window(0, self.y_offset, window=channel_frame, anchor="nw", width=500)
                    self.y_offset += channel_frame.winfo_reqheight() + 50
                    
                except Exception as e:
                    print(f"Error cargando imagen: {e}")
            
            # Calcular dimensiones para scroll (dentro del try...except)
            self.total_height = self.y_offset
            self.scroll_position = 0
            self.canvas.config(scrollregion=(0, 0, 500, self.total_height))
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener suscripciones: {e}")
            return

    def on_mouse_wheel(self, event):
        # Manejar evento de scroll del mouse
        step = 30  # Cantidad de desplazamiento por evento
        
        if event.delta > 0:  # Scroll hacia arriba
            if self.scroll_position > 0:
                self.scroll_position -= step
                if self.scroll_position < 0:
                    self.scroll_position = 0
        else:  # Scroll hacia abajo
            max_scroll = self.total_height - self.canvas_height
            if self.scroll_position < max_scroll:
                self.scroll_position += step
                if self.scroll_position > max_scroll:
                    self.scroll_position = max_scroll

        # Actualizar vista del canvas
        self.canvas.yview_moveto(self.scroll_position / max(1, self.total_height))

    def show_info(self):
        # Mostrar información básica
        messagebox.showinfo("Información", "Esta aplicación permite gestionar tus suscripciones de YouTube.")

    def unsubscribe_selected(self):
        # Placeholder para funcionalidad de desuscripción
        messagebox.showinfo("Info", "Función de desuscripción aún no implementada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeUnsubscriber(root)
    root.mainloop()