import tkinter as tk
from PIL import Image, ImageTk
import os

class SubReaper(tk.Frame):
    def __init__(self, parent):
        """
        Clase que representa la interfaz de SubReaper.
        """
        super().__init__(parent)
        self.parent = parent
        self.color_predeterminado = tk.Label(self).cget("bg")
        self.pack(fill=tk.BOTH, expand=True)
        
        # Necesitamos mantener referencias a las imágenes
        self.imagenes = []
        self._create_widgets()

    def _create_widgets(self):                
        # Obtener dimensiones del área principal (padre)
        ancho_area_principal = self.parent.winfo_width()
        alto_area_principal = self.parent.winfo_height()
        
        #################### INICIO ENCABEZADO ####################
        # Encabezado (10% del alto del área principal)
        encabezadosr = tk.Frame(self, height=alto_area_principal // 10)
        encabezadosr.pack(side=tk.TOP, fill=tk.X, pady=12)
        encabezadosr.propagate(False)
        
        # Label de texto
        titulo_texto = tk.Label(encabezadosr, text="Sub-Reaper", font=("Inter-SemiBold", 20))
        titulo_texto.place(relx=0.05, rely=0.5, anchor=tk.W) # 5% desde la izquierda, centrado verticalmente
        
        # Imagen de subreaper.png
        titulo_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\subreaper.png").resize((70, 70)))
        titulo_imagen_label = tk.Label(encabezadosr, image=titulo_imagen)
        titulo_imagen_label.image = titulo_imagen # Guarda una referencia a la imagen
        titulo_imagen_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # 20% desde la izquierda, centrado verticalmente
        
        # Botón de actualización
        actualizar_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\refresh.png").resize((40, 40)))
        actualizar_boton = tk.Button(encabezadosr, image=actualizar_imagen, bd=0, highlightthickness=0, activebackground=self.color_predeterminado)
        actualizar_boton.image = actualizar_imagen # Guarda una referencia a la imagen
        actualizar_boton.place(relx=0.7, rely=0.5, anchor=tk.CENTER) # 85% desde la izquierda, centrado verticalmente
        
        # Botón "Un-Sub"
        unsub_boton = tk.Button(encabezadosr, text="   Un-Sub   ", font=("Inter-SemiBold", 16), bg="#2C2C2C", fg=self.color_predeterminado, bd=0, highlightthickness=0, activebackground="#2C2C2C",activeforeground=self.color_predeterminado)
        unsub_boton.place(relx=0.925, rely=0.5, anchor=tk.E) # 95% desde la izquierda, centrado verticalmente
        #################### FIN ENCABEZADO ####################
        
        ############### ZONA INFERIOR (Contenedor + Paginación) ###############
        # Frame para organizar contenedor y paginación (debajo del encabezado)
        zona_inferior = tk.Frame(self)
        zona_inferior.pack(fill=tk.BOTH, expand=True)
        
        # Contenedor de canales (75% del ancho del área principal)
        ancho_contenedor = int(ancho_area_principal * 0.70)
        # Contenedor de canales 
        contenedor_canales = tk.Canvas(zona_inferior, width= ancho_contenedor)    
        contenedor_canales.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 20), padx=(80, 0)) # agregar , padx=(20, 0) para padding de la izquierda
        #contenedor_canales.propagate(False) # Evita que el Frame ajuste su tamaño a sus widgets internos
        
        # Tamaño de tarjetas (20% del contenedor, relación 1:1)
        ancho_tarjeta = ancho_contenedor // 5
        alto_tarjeta = ancho_tarjeta  # Para relación 1:1
        # Frame interno para el contenido del Canvas
        frame_canales = tk.Frame(contenedor_canales)
        contenedor_canales.create_window((0, 0), window=frame_canales, anchor=tk.NW)
        
        # Configurar el scroll (permite el limite superior e inferior del scroll)
        def configurar_scroll(event):
            contenedor_canales.configure(scrollregion=contenedor_canales.bbox("all"))

        frame_canales.bind("<Configure>", configurar_scroll)

        # Permite movimiento con la rueda del mouse
        def scroll_mouse(event): 
            contenedor_canales.yview_scroll(int(-1 * (event.delta / 120)), "units")

        contenedor_canales.bind_all("<MouseWheel>", scroll_mouse)
        
        # 2. Tamaño de la imagen (80% del ancho/alto de la tarjeta, para dejar márgenes)
        imagen_ancho = int(ancho_tarjeta * 0.8)  # 80% del ancho de la tarjeta
        imagen_alto = int(alto_tarjeta * 0.8)    # 80% del alto de la tarjeta
        # Tarjetas de canales (50 canales)
        for i in range(50):
            tarjeta = tk.Frame(frame_canales, width=ancho_tarjeta, height=alto_tarjeta, bd=1, relief=tk.SOLID)
            tarjeta.grid(row=i // 5, column=i % 5, padx=10, pady=10)

            # Imagen del canal (ejemplo)
            imagen_canal = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\youtube.png").resize((imagen_ancho, imagen_alto)))
            imagen_canal_label = tk.Label(tarjeta, image=imagen_canal)
            imagen_canal_label.image = imagen_canal # Guarda una referencia a la imagen
            imagen_canal_label.pack()

            # Título del canal (ejemplo)
            titulo_canal = tk.Label(tarjeta, text=f"Canal {i+1}")
            titulo_canal.pack()

            # Cantidad de suscriptores (ejemplo)
            suscriptores_canal = tk.Label(tarjeta, text="1000 suscriptores")
            suscriptores_canal.pack()
        ############### FIN CONTENEDOR ###############
        
        ############### INICIO PAGINACION ############### 
        # Paginación (5% del alto del área principal)    
        paginacion = tk.Frame(zona_inferior, width=int(ancho_area_principal * 0.20), bg="#f0f0f0")
        paginacion.pack(side=tk.RIGHT, fill=tk.Y)
        
        flecha_atras_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\anterior.png").resize((55, 55)))
        flecha_atras_boton = tk.Button(paginacion, image=flecha_atras_imagen, bd=0, highlightthickness=0, activebackground="#f0f0f0")
        flecha_atras_boton.image = flecha_atras_imagen # Guarda una referencia a la imagen
        flecha_atras_boton.place(relx=0.5, rely=0.3, anchor=tk.CENTER) # Centrado verticalmente
        # Flecha para avanzar de página
        flecha_siguiente_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\siguiente.png").resize((55, 55)))
        flecha_siguiente_boton = tk.Button(paginacion, image=flecha_siguiente_imagen, bd=0, highlightthickness=0, activebackground="#f0f0f0")
        flecha_siguiente_boton.image = flecha_siguiente_imagen # Guarda una referencia a la imagen
        flecha_siguiente_boton.place(relx=0.5, rely=0.7, anchor=tk.CENTER) # Centrado verticalmente
        ############### FIN PAGINACION ###############

        

    def reaper_action(self):
        print("¡Acción de SubReaper ejecutada!")