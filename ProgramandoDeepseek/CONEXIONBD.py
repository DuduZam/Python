import pyodbc

print("\nPROBAR CONEXION CON LA BD")

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-A2S73Q8;DATABASE=BibliotecaDB;UID=sa;PWD=imilla555"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

def probar_conexion():
    try:
        cursor.execute("SELECT 1")
        print("Conexión exitosa a la base de datos.")
    except pyodbc.Error as e:
        print("Error en la conexión a la base de datos:", e)

# Llamar a la función de prueba de conexión
probar_conexion()

# python CONEXIONBD.py