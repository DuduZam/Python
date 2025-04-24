import math
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Encabezado centrado en la parte superior del PDF.
        self.set_font("Arial", "B", 12)
        self.cell(190, 10, "Tabla de Funciones Integradas de Python", border=0, ln=1, align="C")
        self.ln(5)

    def table_row(self, data, col_widths, line_height):
        """
        Dibuja una fila de la tabla con celdas de ancho fijo, calculando la altura
        necesaria para envolver el texto.
        
        Parámetros:
          data       : Lista de textos para cada celda.
          col_widths : Lista con el ancho (en mm) para cada celda.
          line_height: Altura de línea (en mm).
        """
        # Calcular el número máximo de líneas requeridas en cada celda
        max_lines = 1
        for i, text in enumerate(data):
            lines = text.split("\n")
            total_lines = 0
            for line in lines:
                # Calculamos cuántas líneas requiere este contenido
                w = self.get_string_width(line)
                total_lines += math.ceil(w / col_widths[i]) if col_widths[i] > 0 else 1
            max_lines = max(max_lines, total_lines)
        row_height = line_height * max_lines

        # Si la fila sobrepasa el final de la página, agregamos una nueva
        if self.get_y() + row_height > self.page_break_trigger:
            self.add_page(self.cur_orientation)

        x_start = self.get_x()
        y_start = self.get_y()

        for i, text in enumerate(data):
            x_current = x_start + sum(col_widths[:i])
            self.set_xy(x_current, y_start)
            self.multi_cell(col_widths[i], line_height, text, border=1, align="L")
        self.set_xy(x_start, y_start + row_height)

# Crear el PDF y configurar página y fuente
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", "", 9)

# Definir las tres columnas: 
#   - Ancho para "Nombre": 25 mm
#   - Ancho para "Definición y parámetros": 110 mm
#   - Ancho para "Ejemplo": 55 mm
col_widths = [25, 110, 55]
headers = ["Nombre", "Definición y parámetros", "Ejemplo"]

# Dibujar la fila de encabezados (en negrita)
pdf.set_font("Arial", "B", 9)
pdf.table_row(headers, col_widths, line_height=5)

# Restaurar la fuente normal para los datos
pdf.set_font("Arial", "", 9)

# Datos de las funciones (cada sublista es una fila de la tabla con 3 columnas)
rows = [
    ["abs()", "Retorna el valor absoluto de un número. Parámetro: num. Retorno: num absoluto.", "-num = num"],
    ["all()", "Retorna True si todos los elementos del iterable son verdaderos. Parámetro: iterable.", "iterable = bool"],
    ["any()", "Retorna True si al menos un elemento del iterable es verdadero. Parámetro: iterable.", "iterable = bool"],
    ["bin()", "Convierte un entero a cadena binaria. Parámetro: num. Retorno: str.", "num = str"],
    ["bool()", "Convierte un valor a booleano. Parámetro: num/str. Retorno: bool.", "num/str = bool"],
    ["chr()", "Convierte un entero a su carácter Unicode. Parámetro: num. Retorno: str.", "num = str"],
    ["divmod()", "Retorna una tupla (cociente, residuo) de la división entre dos números. Parámetros: num, num.", "(num, num) = (num, num)"],
    ["enumerate()", "Devuelve objeto enumerado (índice, valor) de un iterable. Parámetros: iterable, índice opcional.", "[iterable] = [(0, num), (1, num)] (Ej: [10,20] -> (0,10),(1,20))"],
    ["eval()", "Evalúa una cadena como expresión Python. Parámetro: str. Retorno: resultado.", "str = num/str"],
    ["filter()", "Filtra elementos de un iterable según una función. Parámetros: función, iterable.", "iterable = [filtered]"],
    ["len()", "Retorna la longitud de un objeto. Parámetro: iterable/str. Retorno: num.", "iterable/str = num"],
    ["map()", "Aplica una función a cada elemento de un iterable. Parámetros: función, iterable.", "iterable = [mapped]"],
    ["max()", "Retorna el valor máximo de un iterable o entre argumentos. Parámetro: iterable o múltiples.", "iterable = num"],
    ["min()", "Retorna el valor mínimo de un iterable o entre argumentos. Parámetro: iterable o múltiples.", "iterable = num"],
    ["round()", "Redondea un número a un número de decimales. Parámetros: num, dígitos opcional.", "num = num"],
    ["sorted()", "Retorna una nueva lista ordenada a partir de un iterable. Parámetros: iterable, opcionales.", "iterable = [sorted]"],
    ["type()", "Retorna el tipo del objeto. Parámetro: objeto. Retorno: tipo.", "obj = tipo"],
    ["zip()", "Combina varios iterables en tuplas. Parámetros: iterables. Retorno: iterador de tuplas.", "iterables = [(tuplas)]"]
]

# Dibujar cada fila de la tabla
for row in rows:
    pdf.table_row(row, col_widths, line_height=5)

# Guardar el PDF
pdf.output("Funciones_Python_Corregido_Final.pdf")
print("PDF generado correctamente: 'Funciones_Python_Corregido_Final.pdf'")
