# Importación de librerías necesarias
from reportlab.pdfgen import canvas  # Para generar el PDF
from reportlab.lib.pagesizes import A4  # Tamaño de hoja estándar
from reportlab.lib import colors  # Manejo de colores
from datetime import datetime  # Para trabajar con fechas
import calendar  # Para funcionalidades de calendario
import locale  # Para configuración regional

# Configurar el locale a español de España (para nombres de meses y días en español)
locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")

# Configuración principal del documento
year = 2025  # Año del calendario
pdf = canvas.Canvas(f"calendario_{year}.pdf", pagesize=A4)  # Crear objeto PDF
width, height = A4  # Dimensiones del papel A4
calendar.setfirstweekday(calendar.MONDAY)  # La semana empieza en lunes

# Configuración de turnos rotativos
NOMBRES = ["EDUARDO" , "PEPE" , "SEBASTIAN" , "WARA"]  # Orden de turnos
FECHA_INICIO = datetime(year, 3, 24)  # Fecha de inicio de los turnos

# Parámetros de diseño del calendario
MARGEN_X = 50  # Margen horizontal izquierdo
MARGEN_Y_SUPERIOR = 120  # Margen superior para el grid
ANCHO_CELDA = 70  # Ancho de cada celda del calendario
ALTO_CELDA = 60  # Alto de cada celda del calendario
COLOR_CABECERA = colors.HexColor("#3F51B5")  # Azul para la cabecera
COLOR_TEXTO = colors.black  # Color principal del texto

def dibujar_estructura(y_inicio):
    """
    Dibuja la estructura de la cuadrícula del calendario.
    y_inicio: Posición vertical donde comienza el grid
    """
    # Líneas verticales (7 columnas + 1 para cerrar)
    for x in [MARGEN_X + i * ANCHO_CELDA for i in range(8)]:
        pdf.line(x, y_inicio, x, y_inicio - 6 * ALTO_CELDA)
    
    # Líneas horizontales (6 filas: 1 cabecera + 5 semanas)
    for i in range(7):
        y = y_inicio - i * ALTO_CELDA
        pdf.line(MARGEN_X, y, MARGEN_X + 7 * ANCHO_CELDA, y)

def crear_mes(mes, año):
    """Genera una página del calendario para un mes específico"""
    pdf.setPageSize(A4)  # Asegurar tamaño de página
    
    # Título del mes (ej: "MARZO 2025")
    pdf.setFont("Helvetica-Bold", 24)
    titulo = datetime(año, mes, 1).strftime("%B %Y").upper()
    pdf.drawCentredString(width/2, height - 50, titulo)
    
    # Posicionamiento inicial del grid
    y_grid_start = height - MARGEN_Y_SUPERIOR  # Posición Y inicial del grid
    y_cabecera = y_grid_start - ALTO_CELDA + 45  # Ajuste vertical para cabecera
    
    # Cabecera con días de la semana
    pdf.setFont("Helvetica-Bold", 14)
    pdf.setFillColor(COLOR_CABECERA)
    for i, dia in enumerate(["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]):
        x = MARGEN_X + i * ANCHO_CELDA + 10  # +10 para margen interno
        pdf.drawString(x, y_cabecera, dia)
    
    # Dibujar estructura de cuadrícula
    pdf.setStrokeColor(colors.HexColor("#E0E0E0"))  # Color gris claro
    dibujar_estructura(y_grid_start - ALTO_CELDA)  # Ajustar posición
    
    # Rellenar números y turnos
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(COLOR_TEXTO)
    semanas = calendar.monthcalendar(año, mes)  # Obtener semanas del mes
    
    for semana_num, semana in enumerate(semanas):  # Iterar semanas
        for dia_num, dia in enumerate(semana):  # Iterar días de la semana
            if dia != 0:  # Saltar días vacíos (días de otros meses)
                # Posicionamiento del número del día
                x = MARGEN_X + dia_num * ANCHO_CELDA + 10
                y = y_grid_start - (semana_num + 2) * ALTO_CELDA + 40
                pdf.drawString(x, y, str(dia))

                # Calcular turno rotativo
                fecha_actual = datetime(año, mes, dia)
                if fecha_actual >= FECHA_INICIO:
                    # Cálculo de días desde el inicio
                    dias_diferencia = (fecha_actual - FECHA_INICIO).days
                    # Selección del turno usando módulo 4
                    turno = NOMBRES[dias_diferencia % 4]
                    
                    # Escribir nombre del turno (fuente más pequeña)
                    pdf.setFont("Helvetica", 8)
                    pdf.drawString(x, y - 12, turno)  # 12 puntos debajo del número
                    pdf.setFont("Helvetica", 12)  # Restaurar fuente original

    pdf.showPage()  # Finalizar página actual

# Generar los meses de marzo (3) a agosto (8)
for mes in range(3, 9):
    crear_mes(mes, year)

# Guardar el archivo PDF generado
pdf.save()