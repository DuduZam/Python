import tkinter as tk
from PIL import Image, ImageTk

class FocusTube(tk.Frame):
    def __init__(self, parent):
        """
        Clase que representa la interfaz de FocusTube.
        """
        super().__init__(parent)
        self.parent = parent
        self.color_predeterminado = tk.Label(self).cget("bg")
        self.pack(fill=tk.BOTH, expand=True)  # Ocupa todo el espacio disponible.
        self.parent.after(100, self._create_widgets)  # Espera 100ms
        #self._create_widgets()

    def _create_widgets(self):
        # Obtener dimensiones del área principal (padre)
        #self.parent.update_idletasks()  # Fuerza la actualización geométrica
        ancho_area_principal = self.parent.winfo_width()
        alto_area_principal = self.parent.winfo_height()
        
        #################### INICIO ENCABEZADO ####################
        # Encabezado (10% del alto del área principal)
        encabezadoft = tk.Frame(self, height=alto_area_principal // 10)
        encabezadoft.pack(side=tk.TOP, fill=tk.X, pady=12)
        encabezadoft.propagate(False)
        
        # Label de texto
        titulo_texto = tk.Label(encabezadoft, text="Focus-Tube", font=("Inter-SemiBold", 20))
        titulo_texto.place(relx=0.05, rely=0.5, anchor=tk.W) # 5% desde la izquierda, centrado verticalmente
        
        # Imagen de subreaper.png
        titulo_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\AI.png").resize((70, 70)))
        titulo_imagen_label = tk.Label(encabezadoft, image=titulo_imagen)
        titulo_imagen_label.image = titulo_imagen # Guarda una referencia a la imagen
        titulo_imagen_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # 20% desde la izquierda, centrado verticalmente
        
        # Botón de actualización
        actualizar_imagen = ImageTk.PhotoImage(Image.open("C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\Proyectos\\PurifyTube\\images\\refresh.png").resize((40, 40)))
        actualizar_boton = tk.Button(encabezadoft, image=actualizar_imagen, bd=0, highlightthickness=0, activebackground=self.color_predeterminado)
        actualizar_boton.image = actualizar_imagen # Guarda una referencia a la imagen
        actualizar_boton.place(relx=0.7, rely=0.5, anchor=tk.CENTER) # 85% desde la izquierda, centrado verticalmente
        
        # Botón "Un-Sub"
        unsub_boton = tk.Button(encabezadoft, text="   Un-Sub   ", font=("Inter-SemiBold", 16), bg="#2C2C2C", fg=self.color_predeterminado, bd=0, highlightthickness=0, activebackground="#2C2C2C",activeforeground=self.color_predeterminado)
        unsub_boton.place(relx=0.925, rely=0.5, anchor=tk.E) # 95% desde la izquierda, centrado verticalmente
        #################### FIN ENCABEZADO ####################

    def focus_action(self):
        print("¡Acción de FocusTube ejecutada!")