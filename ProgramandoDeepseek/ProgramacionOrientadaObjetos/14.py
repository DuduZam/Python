import csv
from typing import Callable, List, Dict
from datetime import datetime

# 1. Función para leer datos de un archivo CSV
def leer_csv(ruta_archivo: str) -> List[Dict[str, str]]:
    """
    Lee un archivo CSV y devuelve una lista de diccionarios.
    Cada fila del CSV se convierte en un diccionario con claves basadas en el encabezado.
    """
    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

# 2. Función para aplicar operaciones dinámicas
def procesar_datos(datos: List[Dict[str, str]], funcion: Callable[[List[Dict[str, str]]], float]) -> float:
    """
    Aplica una función personalizada a los datos y devuelve el resultado.
    """
    return funcion(datos)

# 3. Función para calcular el promedio de ventas
def calcular_promedio_ventas(datos: List[Dict[str, str]]) -> float:
    """
    Calcula el promedio de las ventas de los datos proporcionados.
    """
    ventas = [float(fila["Ventas"]) for fila in datos]
    return sum(ventas) / len(ventas)

# 4. Función para sumar las ventas por categoría
def ventas_por_categoria(datos: List[Dict[str, str]]) -> Dict[str, float]:
    """
    Calcula las ventas totales agrupadas por categoría.
    """
    categorias = {}
    for fila in datos:
        categoria = fila["Categoría"]
        venta = float(fila["Ventas"])
        categorias[categoria] = categorias.get(categoria, 0) + venta
    return categorias

# 5. Función para generar un informe
def generar_informe(datos: List[Dict[str, str]]) -> str:
    """
    Genera un informe estructurado a partir de los datos.
    """
    promedio = calcular_promedio_ventas(datos)
    ventas_categorias = ventas_por_categoria(datos)

    informe = (
        f"Informe Financiero\n"
        f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Promedio de ventas: ${promedio:.2f}\n"
        f"Ventas por categoría:\n"
    )
    for categoria, total in ventas_categorias.items():
        informe += f"- {categoria}: ${total:.2f}\n"

    return informe

# 6. Función para guardar el informe
def guardar_informe(ruta_archivo: str, contenido: str) -> None:
    """
    Guarda el informe en un archivo de texto.
    """
    with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    print(f"Informe guardado en: {ruta_archivo}")

# 7. Flujo principal
if __name__ == "__main__":
    # Ruta del archivo CSV
    ruta_csv = "C:\\Users\\lloca\\Desktop\\GITHUB\\PYTHON\\ProgramandoDeepseek\\ProgramacionOrientadaObjetos\\ventas_14.csv"  # Asegúrate de tener un archivo CSV con columnas: Ventas, Categoría
    try:
        # Leer datos del CSV
        datos = leer_csv(ruta_csv)

        # Generar y mostrar informe
        informe = generar_informe(datos)
        print(informe)

        # Guardar el informe en un archivo
        guardar_informe("informe_financiero.txt", informe)

    except Exception as e:
        print(f"Error: {e}")
