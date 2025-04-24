import tkinter as tk
from PIL import Image, ImageTk

class Sidebar(tk.Frame):
    def __init__(self, parent, alternar_interfaz, width, bg="lightgray"):
        """
        Clase para representar la barra lateral.

        :param parent: Contenedor padre, generalmente la ventana principal.
        :param width: Ancho del sidebar.
        :param bg: Color de fondo del sidebar.
        :param alternar_interfaz: Función que alterna entre interfaces en el área principal.
        """
        # Llamamos al constructor de tk.Frame y pasamos el padre y configuración.
        super().__init__(parent, width=width, bg=bg)
        # Configuramos layout y dimensiones.
        self.pack(side=tk.LEFT, fill=tk.Y)  # Ocupa el lado izquierdo y llena el alto.
        self.propagate(False)  # Evitamos que el tamaño cambie según su contenido.       
        
        self.alternar_interfaz = alternar_interfaz  # Guarda referencia a la función para alternar interfaces.
        
        # Agregamos widgets iniciales como ejemplo.
        self._create_widgets()
    
    def _create_widgets(self):
        # Logo
        logo_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\youtube.png").resize((100, 100)))
        logo = tk.Label(self, text="PurifyTube ", image=logo_imagen, bg="lightgray", compound=tk.RIGHT, font=("Inter-SemiBold", 25))
        logo.image = logo_imagen
        logo.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Botón FocusTube
        boton_focus_tube_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\AI.png").resize((80, 80)))
        boton_focus_tube = tk.Button(self, text=" FocusTube", font=("Inter-SemiBold", 18), image=boton_focus_tube_imagen, compound=tk.LEFT, bg="lightgray", bd=0, highlightthickness=0, activebackground="lightgray", command=lambda: self.alternar_interfaz("FocusTube"))
        boton_focus_tube.image = boton_focus_tube_imagen
        boton_focus_tube.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Botón Sub-Reaper
        boton_sub_reaper_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\subreaper.png").resize((80, 80)))
        boton_sub_reaper = tk.Button(self, text="Sub-Reaper ", font=("Inter-SemiBold", 18), image=boton_sub_reaper_imagen, compound=tk.RIGHT, bg="lightgray", bd=0, highlightthickness=0, activebackground="lightgray", command=lambda: self.alternar_interfaz("SubReaper"))
        boton_sub_reaper.image = boton_sub_reaper_imagen
        boton_sub_reaper.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        # Crear un Frame contenedor para los botones inferiores
        self.botones_inferiores = tk.Frame(self, bg="lightgray")
        self.botones_inferiores.place(relx=0.5, rely=0.89, anchor=tk.CENTER)
        
        self.botones_inferioresf1 = tk.Frame(self.botones_inferiores, bg="lightgray")        
        self.botones_inferioresf1.pack(pady=7)

        self.botones_inferioresf2 = tk.Frame(self.botones_inferiores, bg="lightgray")
        self.botones_inferioresf2.pack(fill=tk.X, padx=10, pady=5)
        
        # FILA 1
        # Imagen Usuario
        self.usuario_imagen_img = None #ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\LAIMAGENCANALUSUARIO.png").resize((50, 50)))
        self.usuario_imagen = tk.Label(self.botones_inferioresf1, image=self.usuario_imagen_img, bg="lightgray")
        self.usuario_imagen.image = self.usuario_imagen_img        
        self.usuario_imagen.grid(row=0, column=0, padx=10)
        
        # Nombre Usuario
        #logo_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\youtube.png").resize((100, 100)))
        self.nombre_usuario = tk.Label(self.botones_inferioresf1, text=" ", bg="lightgray", font=("Inter-SemiBold", 18))                
        self.nombre_usuario.grid(row=0, column=1, padx=10)
        
        # FILA 2
        # Botón de Información
        self.boton_info_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\info.png").resize((40, 40)))
        boton_info = tk.Button(self.botones_inferioresf2, image=self.boton_info_imagen, bg="lightgray", bd=0, highlightthickness=0, activebackground="lightgray")
        boton_info.pack(side=tk.LEFT, padx=20)        

        # Botón Subir Json
        self.boton_json_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\json.png").resize((40, 40)))
        self.boton_json = tk.Button(self.botones_inferioresf2, image=self.boton_json_imagen, bg="lightgray", bd=0, highlightthickness=0, activebackground="lightgray")
        self.boton_json.pack(side=tk.LEFT, padx=20)

        # Led ON - OFF
        self.led_off_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\apagar.png").resize((40, 40)))
        self.led_on_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\encender.png").resize((40, 40)))
        self.led = tk.Label(self.botones_inferioresf2, image=self.led_off_imagen, bg="lightgray", compound=tk.RIGHT, font=("Inter-SemiBold", 25))
        self.led.pack(side=tk.LEFT, padx=20)

        # Botón Cerrar Sesión
        self.boton_cerrarsesion_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\cerrar-sesion.png").resize((40, 40)))
        self.boton_cerrarsesion = tk.Button(self.botones_inferioresf2, image=self.boton_cerrarsesion_imagen, bg="lightgray", bd=0, highlightthickness=0, activebackground="lightgray")
        self.boton_cerrarsesion.pack(side=tk.LEFT, padx=20)
        
    def actualizar_usuario(self, nombre_us, foto_us):
        self.nombre_usuario.config(text=nombre_us)        
        self.usuario_imagen_img = ImageTk.PhotoImage(foto_us)
        self.usuario_imagen.config(image=self.usuario_imagen_img)
        self.usuario_imagen.image = self.usuario_imagen_img
        #self.usuario_imagen.config(image=self.usuario_imagen_img)
        
    def deshabilitar_inicio_sesion(self, encendido=True):
        if encendido:
            self.boton_json.config(state="disabled")
            self.led.config(image=self.led_on_imagen)
        else:
            self.boton_json.config(state="normal")
            self.led.config(image=self.led_off_imagen)
    