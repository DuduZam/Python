from datetime import datetime
import locale

# Configura el idioma para los nombres de los días y meses
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Para español

# Crea un objeto datetime
fecha_hora = datetime(2025, 4, 18, 10, 46, 10)

# Formatea la fecha y hora
formato_personalizado = fecha_hora.strftime('%A, %d de %B de %Y %H:%M:%S').capitalize()

print(formato_personalizado)