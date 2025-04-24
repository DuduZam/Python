import tkinter as tk
from tkinter import simpledialog, messagebox
import datetime
import time
from threading import Thread
import pygame
import os
from typing import List

# Inicializa pygame
pygame.init()

# Ruta del sonido
RUTA_MUSICA = "C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\ProgramandoDeepseek\\ProgramacionOrientadaObjetos\\music.mp3"

# Lista de alarmas con tipo explícito
alarmas: List[datetime.datetime] = []

def añadir_alarma() -> None:
    """
    Solicita al usuario una hora (HH:MM) y la agrega a la lista de alarmas si es válida.
    """
    respuesta = simpledialog.askstring("Nueva Alarma", "Ingrese la hora (HH:MM:SS) en formato 24 horas:")
    if respuesta:
        try:
            hora, minuto, segundo = map(int, respuesta.split(":"))
            ahora = datetime.datetime.now()
            nueva_alarma = ahora.replace(hour=hora, minute=minuto, second=segundo, microsecond=0)

            if nueva_alarma < ahora:
                nueva_alarma += datetime.timedelta(days=1)

            alarmas.append(nueva_alarma)
            actualizar_lista()
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto. Use HH:MM (ej. 14:30).")  # type: ignore


def actualizar_lista() -> None:
    """
    Muestra todas las alarmas programadas en el marco visual.
    """
    for widget in marco_alarmas.winfo_children():
        widget.destroy()

    for alarma in sorted(alarmas):
        etiqueta = tk.Label(
            marco_alarmas,
            text=f"Alarma: {alarma.strftime('%H:%M:%S')}",
            bg="lightgray",
            font=("Arial", 12),
            pady=5
        )
        etiqueta.pack(pady=3, padx=5, fill="x")

def verificar_alarmas() -> None:
    """
    Verifica si alguna alarma debe sonar.
    """
    while True:
        ahora = datetime.datetime.now().replace(microsecond=0)
        for alarma in list(alarmas):  # Se hace copia segura
            if ahora >= alarma:
                alarmas.remove(alarma)
                ventana.after(0, mostrar_ventana_emergente)
                ventana.after(0, actualizar_lista)
                break
        time.sleep(1)

def mostrar_ventana_emergente() -> None:
    """
    Muestra la alerta y permite desactivar la alarma.
    """
    def desactivar_alarma() -> None:
        """
        Detiene la música y cierra la ventana emergente si se desactiva la alarma.
        """
        if deslizable.get() == 1:  # Si el deslizable está completamente a la derecha (1)
            pygame.mixer.music.stop()
            ventana_emergente.destroy()

    ventana_emergente = tk.Toplevel(ventana)
    ventana_emergente.title("¡Alarma!")
    ventana_emergente.geometry("300x180")
    ventana_emergente.grab_set()

    tk.Label(
        ventana_emergente,
        text="¡Deslice para apagar la alarma!",
        font=("Arial", 12)
    ).pack(pady=15)

    # Creamos el deslizable personalizado
    canvas = tk.Canvas(ventana_emergente, width=250, height=50, bg="#d3d3d3")
    canvas.pack(pady=10)

    # Definimos el botón deslizante
    deslizable_rect = canvas.create_rectangle(0, 0, 50, 50, fill="#4CAF50", outline="black", width=2)
    canvas.create_text(125, 25, text="Slide to Unlock", font=("Arial", 10), fill="white")

    def on_drag(event: tk.Event) -> None:
        """
        Mueve el rectángulo a medida que el usuario arrastra el mouse.
        """
        if event.x >= 0 and event.x <= 200:  # Aseguramos que no se salga del rango
            canvas.coords(deslizable_rect, event.x - 25, 0, event.x + 25, 50)

        if event.x >= 200:  # Si el deslizable llega al final
            canvas.coords(deslizable_rect, 200 - 25, 0, 200 + 25, 50)
            canvas.itemconfig(deslizable_rect, fill="#f44336")  # Cambiamos color cuando se desbloquea

    def on_release(event: tk.Event) -> None:
        """
        Resetea la posición del deslizable si no se ha llegado al final.
        """
        if event.x < 200:
            canvas.coords(deslizable_rect, 0, 0, 50, 50)
            canvas.itemconfig(deslizable_rect, fill="#4CAF50")  # Restauramos el color

    canvas.bind("<B1-Motion>", on_drag)  # Arrastre del deslizable
    canvas.bind("<ButtonRelease-1>", on_release)  # Cuando se suelta el botón

    if os.path.exists(RUTA_MUSICA):
        try:
            pygame.mixer.music.load(RUTA_MUSICA)
            pygame.mixer.music.play(loops=-1)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reproducir el sonido:\n{e}")  # type: ignore
    else:
        messagebox.showwarning("Aviso", "No se encontró el archivo de sonido.")  # type: ignore

# ---------------------- INTERFAZ PRINCIPAL ----------------------

ventana = tk.Tk()
ventana.title("Gestor de Alarmas")
ventana.geometry("400x600")
ventana.resizable(False, False)

marco_alarmas = tk.Frame(ventana, bg="white")
marco_alarmas.pack(pady=10, padx=10, fill="both", expand=True)

boton_añadir = tk.Button(
    ventana,
    text="+",
    font=("Arial", 18),
    fg="white",
    bg="green",
    command=añadir_alarma
)
boton_añadir.place(x=10, y=540, width=50, height=50)

# Hilo para verificar las alarmas
Thread(target=verificar_alarmas, daemon=True).start()

ventana.mainloop()
