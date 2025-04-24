import os  # Importa el módulo 'os' para interactuar con el sistema operativo.
import pickle  # Importa el módulo 'pickle' para serializar y deserializar objetos de Python.
import json  # Importa el módulo 'json' para trabajar con datos JSON.
import requests # Peticiones HTTP
import tkinter as tk  # Importamos el módulo tkinter y lo renombramos como tk para mayor comodidad
from tkinter import filedialog # Abrir Seleccionador de archivos Json
from PIL import Image, ImageTk #importamos las librerias para manejar imagenes
from io import BytesIO  # Para manejar datos de imágenes en memoria temporal
# interfaces *.py
from focus_tube import FocusTube  # Importa la clase FocusTube.
from sub_reaper import SubReaper  # Importa la clase SubReaper.
from sidebar import Sidebar # Importa la clase Sidebar.
#from youtube_api import obtener_suscripciones_reales  # lo implementaremos después

# Google Authenticacion
from google_auth_oauthlib.flow import InstalledAppFlow  # Importa la clase 'InstalledAppFlow' para el flujo de autenticación OAuth 2.0.
from googleapiclient.discovery import build  # Importa la función 'build' para construir el objeto de servicio de la API de YouTube.
from google.auth.transport.requests import Request  # Importa la clase 'Request' para refrescar tokens de acceso.

def alternar_interfaz(area_principal, nombre_interfaz):
    """
    Función para alternar entre interfaces en el área principal.

    :param area_principal: Frame contenedor del área principal.
    :param nombre_interfaz: Nombre de la interfaz que se debe cargar.
    """
    # Elimina todos los widgets actuales en el área principal.
    for widget in area_principal.winfo_children():
        widget.destroy()

    # Carga la nueva interfaz según el nombre.
    if nombre_interfaz == "FocusTube":
        FocusTube(area_principal)
    elif nombre_interfaz == "SubReaper":
        SubReaper(area_principal)

def main():
    global credenciales  # Declaramos la variable credenciales como global
    # Creamos la ventana principal
    TOKEN_PATH = "tokens.pickle"
    
    ventana = tk.Tk()
    ventana.title("Purify Tube")    
    # 1. Obtener el tamaño de la pantalla
    ventana_ancho = ventana.winfo_screenwidth() # En mi caso 1280px
    ventana_alto = ventana.winfo_screenheight() # En mi caso 720px        
    # 2. Configurar la ventana para que ocupe todo el espacio disponible    
    ventana.geometry(f"{ventana_ancho}x{ventana_alto}+0+0") # geometry(anchoxalto+-pos_x+-pos_y)            
    ventana.resizable(False, False)  # Evita que se redimensione
    #ventana.attributes('-toolwindow', True)  # Opcional: Elimina iconos de maximizar/minimizar (Windows)
    ventana.state('zoomed') # le hace zoom
    
    # Color gris claro predeterminado de tkinter
    #color_predeterminado = tk.Label(ventana).cget("bg")
        
    # Creamos el Área Principal (75% del ancho de la ventana).
    area_principal = tk.Frame(ventana, width=(ventana_ancho * 3) // 4)
    area_principal.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Barra Lateral (25% del ancho)    
    barra_lateral = Sidebar(ventana, alternar_interfaz=lambda nombre: alternar_interfaz(area_principal, nombre), width=ventana_ancho // 4, bg="lightgray")
        
    # Inicialmente cargamos la interfaz FocusTube.
    FocusTube(area_principal)
    
    def autenticar_con_json():
        #SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl","https://www.googleapis.com/auth/userinfo.profile"]

        """
        Esta función se activa cuando el usuario hace clic en el botón para cargar el archivo JSON.
        Realiza la autenticación utilizando el archivo JSON cargado y guarda las credenciales en 'tokens.pickle'.
        """
        global credenciales  # Aseguramos que se usa la variable global
        # Abrir el file dialog para cargar el archivo JSON
        ruta_archivo_json = filedialog.askopenfilename(
            title="Selecciona un archivo JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        
        if ruta_archivo_json:
            try:
                # Crear el flujo de autenticación usando el archivo JSON
                flow = InstalledAppFlow.from_client_secrets_file(
                    ruta_archivo_json, 
                    SCOPES  # El scope que has definido
                )

                # Ejecutar el flujo de autenticación, el cual abrirá una ventana del navegador
                credenciales = flow.run_local_server(port=0)

                # Guardar las credenciales en el archivo tokens.pickle
                with open(TOKEN_PATH, "wb") as token_file:
                    pickle.dump(credenciales, token_file)

                # Obtener el nombre y foto del usuario autenticado
                nombre, foto_url = obtener_info_usuario(credenciales.token)
                
                # Mostrar el nombre en el Label
                 #barra_lateral.nombre_usuario.config(text=nombre)

                # Mostrar la imagen en el Label
                if foto_url:
                    try:
                        imagen_raw = requests.get(foto_url).content
                        imagen_pil = Image.open(BytesIO(imagen_raw)).resize((60, 60))
                        barra_lateral.actualizar_usuario(nombre,imagen_pil)
                         #imagen_tk = ImageTk.PhotoImage(imagen_pil)
                         #barra_lateral.usuario_imagen.config(image=imagen_tk)
                         #barra_lateral.usuario_imagen.image = imagen_tk  # ⬅️ REFERENCIA
                        #print("[✔️] Imagen de usuario cargada y mostrada")
                    except Exception as img_error:
                        print(f"[❌] Error al cargar imagen de usuario: {img_error}")
                        barra_lateral.usuario_imagen.config(image="")
                        barra_lateral.usuario_imagen.image = None
                else:
                    barra_lateral.usuario_imagen.config(image="")
                    barra_lateral.usuario_imagen.image = None

                print(f"[ ✌️ 😎 ] INICIO DE SESION EXITOSA:\n[ ✔️ ] Imagen de usuario cargada y mostrada: {foto_url}\n[ ✔️ ] Nombre mostrado: {nombre}")
                barra_lateral.deshabilitar_inicio_sesion(encendido=True)
                #barra_lateral.boton_json.config(state="disabled")
                #barra_lateral.led.config(image=barra_lateral.led_on_imagen)
                #print(f"[✔️] Nombre mostrado: {nombre}")
                
                 # Mostrar la información del usuario autenticado
                #print(f"Primera Autenticación exitosa. Usuario: {nombre}")
                #print(f"Foto de perfil: {foto_url}")

            except Exception as e:
                print(f"Error durante la autenticación: {e}")
                barra_lateral.nombre_usuario.config(text="")
                barra_lateral.usuario_imagen.config(image="")
                barra_lateral.usuario_imagen.image = None
        else:
            print("No se seleccionó ningún archivo JSON.")
            
    def obtener_info_usuario(access_token):
        """
        Recupera información básica del usuario autenticado con Google:
        nombre completo y URL de su foto de perfil.

        Parámetros:
        - access_token (str): Token de acceso válido obtenido tras autenticación.

        Retorna:
        - tuple: (nombre_usuario (str), url_foto (str or None))
        """
        try:
            # Hacemos una petición a la API de Google para obtener los datos del perfil del usuario
            response = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo?alt=json",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            # Si la respuesta fue exitosa (HTTP 200), parseamos el JSON
            if response.status_code == 200:
                datos_usuario = response.json()
                # Verificamos si los datos del usuario contienen 'name' y 'picture'
                nombre = datos_usuario.get("name", "Desconocido")
                foto_url = datos_usuario.get("picture", None)
                
                    # Imprime todo para debug
                #print("Respuesta completa del usuario:")
                #print(json.dumps(datos_usuario, indent=4, ensure_ascii=False))
                
                # Retornamos el nombre y la foto (si existe)
                return nombre, foto_url

            # Si la respuesta no fue 200, devolvemos 'Desconocido'
            else:
                print(f"Error en la respuesta: {response.status_code}")
                print(response.text)
                return "Desconocido", None

        except Exception as e:
            # Si algo falla (conexión, token inválido, etc.), mostramos el error en consola
            print(f"Error al obtener datos del usuario: {e}")
            return "Desconocido", None
            
    def verificar_sesion_activa():
        global credenciales  # Aseguramos que se usa la variable global
        # Verifica si ya existe un archivo de sesión activa
        if os.path.exists(TOKEN_PATH):
            # Abre y carga las credenciales guardadas (access y refresh token)
            with open(TOKEN_PATH, "rb") as token_file:
                credenciales = pickle.load(token_file)

            # Si las credenciales existen y el access_token sigue siendo válido
            if credenciales and credenciales.valid:
                # Obtener el nombre del usuario autenticado
                nombre, foto_url = obtener_info_usuario(credenciales.token)
                
                print(f"Sesión activa detectada. Usuario: {nombre}")                
                print(f"Foto de perfil: {foto_url}")
                
                #barra_lateral.nombre_usuario.config(text=nombre)

                if foto_url:
                    try:
                        imagen_raw = requests.get(foto_url).content
                        imagen_pil = Image.open(BytesIO(imagen_raw)).resize((60, 60))
                        barra_lateral.actualizar_usuario(nombre,imagen_pil)
                        #imagen_tk = ImageTk.PhotoImage(imagen_pil)

                        #barra_lateral.usuario_imagen.config(image=imagen_tk)
                        #barra_lateral.usuario_imagen.image = imagen_tk
                    except Exception as e:
                        print(f"[❌] Error cargando imagen: {e}")
                        barra_lateral.usuario_imagen.config(image="")
                        barra_lateral.usuario_imagen.image = None
                else:
                    barra_lateral.usuario_imagen.config(image="")
                    barra_lateral.usuario_imagen.image = None
                    
                barra_lateral.deshabilitar_inicio_sesion(encendido=True)
                #barra_lateral.boton_json.config(state="disabled")
                #barra_lateral.led.config(image=barra_lateral.led_on_imagen)
                return credenciales

            # Si el access_token está expirado, pero hay un refresh_token disponible
            elif credenciales and credenciales.expired and credenciales.refresh_token:
                # Se usa el refresh_token para obtener un nuevo access_token sin pedir login al usuario
                credenciales.refresh(Request())

                # Guardamos nuevamente las credenciales actualizadas
                with open(TOKEN_PATH, "wb") as token_file:
                    pickle.dump(credenciales, token_file)

                # Obtener la info del usuario con el nuevo token
                nombre, foto_url = obtener_info_usuario(credenciales.token)
                                
                print(f"Sesión activa actualizada. Usuario: {nombre}")                
                print(f"Foto de perfil: {foto_url}")
                
                if foto_url:
                    try:
                        imagen_raw = requests.get(foto_url).content
                        imagen_pil = Image.open(BytesIO(imagen_raw)).resize((60, 60))
                        barra_lateral.actualizar_usuario(nombre,imagen_pil)
                        #imagen_tk = ImageTk.PhotoImage(imagen_pil)
                        #barra_lateral.usuario_imagen.config(image=imagen_tk)
                        #barra_lateral.usuario_imagen.image = imagen_tk
                    except Exception as e:
                        print(f"[❌] Error cargando imagen: {e}")
                        barra_lateral.usuario_imagen.config(image="")
                        barra_lateral.usuario_imagen.image = None
                else:
                    barra_lateral.usuario_imagen.config(image="")
                    barra_lateral.usuario_imagen.image = None
                
                barra_lateral.deshabilitar_inicio_sesion(encendido=True)
                #barra_lateral.boton_json.config(state="disabled")
                #barra_lateral.led.config(image=barra_lateral.led_on_imagen)    
                return credenciales

        # Si no hay archivo de sesión o las credenciales no sirven, no hay sesión activa
        #print("No hay sesión activa. Esperando autenticación.")
        #barra_lateral.nombre_usuario.config(text="")
        #barra_lateral.usuario_imagen.config(image="")
        #barra_lateral.usuario_imagen.image = None
        return None
    
    def cerrar_sesion():
        if os.path.exists("tokens.pickle"):
            os.remove("tokens.pickle")            
            barra_lateral.nombre_usuario.config(text="")
            barra_lateral.usuario_imagen.config(image="")
            barra_lateral.usuario_imagen.image = None
            
            barra_lateral.deshabilitar_inicio_sesion(encendido=False)
            print("Sesión cerrada.")
    
    barra_lateral.boton_json.config(command=autenticar_con_json)
    barra_lateral.boton_cerrarsesion.config(command=cerrar_sesion)
    
    # Llamar a la función para verificar sesión activa al iniciar la aplicación
    credenciales = verificar_sesion_activa()
    
    canales_cliente = []        
    if credenciales:
        service = build("youtube", "v3", credentials=credenciales)
        #canales_cliente = obtener_suscripciones_reales(service)
        #app = SubReaper(root, canales=canales_cliente)
    else:
        print("No hay sesión activa. Esperando autenticación.")
    
    # Inicia el bucle principal de la aplicación tkinter
    ventana.mainloop()

if __name__ == '__main__':  # Verifica si el script se está ejecutando como el programa principal.
    main()  # Llama a la función 'main()' para ejecutar el script.