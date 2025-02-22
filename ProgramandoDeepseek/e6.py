import pyodbc
import random
import datetime

print("\nSEXTO EJERCICIO PYTHON DEEPSEEK\nSistema de gestión para una biblioteca")

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_name;DATABASE=BibliotecaDB;UID=user;PWD=password"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

class Libro:
    def __init__(self, titulo, autor, año_publicacion):
        self.titulo = titulo
        self.autor = autor
        self.año_publicacion = año_publicacion
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"'{self.titulo}' por {self.autor} ({self.año_publicacion}) - {estado}"

    def prestar(self):
        if self.disponible:
            self.disponible = False
            return True  # Libro prestado con éxito
        else:
            return False  # Libro no disponible

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            return True  # Libro devuelto con éxito
        else:
            return False  # Libro ya estaba disponible


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.id_usuario = self.generar_id_unico()  # Generar ID único automáticamente
        self.libros_prestados = []  # Lista para almacenar los libros prestados

    def generar_id_unico(self):
        fecha_actual = datetime.datetime.now().strftime("%d%m%Y")  # Fecha en formato DDMMYYYY
        numero_aleatorio = f"{random.randint(0, 9999):04d}"  # Número aleatorio de 4 dígitos
        return f"{fecha_actual}{self.nombre[:3]}{numero_aleatorio}"  # ID único

    def __str__(self):
        return f"Usuario: {self.nombre}, ID: {self.id_usuario}"

    def prestar_libro(self, libro):
        if libro.prestar():
            self.libros_prestados.append(libro)
            return True  # Libro prestado con éxito
        else:
            return False  # Libro no disponible

    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            if libro.devolver():
                self.libros_prestados.remove(libro)
                return True  # Libro devuelto con éxito
        return False  # Libro no estaba prestado al usuario


class Biblioteca:
    def __init__(self):
        pass

    def añadir_libro(self, libro):
        cursor.execute("INSERT INTO Libros (titulo, autor, año_publicacion, disponible) VALUES (?, ?, ?, ?)", 
                       libro.titulo, libro.autor, libro.año_publicacion, libro.disponible)
        conn.commit()
        return f"El libro '{libro.titulo}' ha sido añadido a la biblioteca."

    def registrar_usuario(self, usuario):
        cursor.execute("INSERT INTO Usuarios (id, nombre) VALUES (?, ?)", usuario.id_usuario, usuario.nombre)
        conn.commit()
        return f"El usuario '{usuario.nombre}' ha sido registrado en la biblioteca con ID: {usuario.id_usuario}."

    def prestar_libro(self, id_usuario, titulo_libro):
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        libro = next((l for l in self.libros if l.titulo == titulo_libro), None)

        if usuario and libro:
            if usuario.prestar_libro(libro):
                return f"El libro '{libro.titulo}' ha sido prestado a {usuario.nombre}."
            else:
                return f"El libro '{libro.titulo}' no está disponible."
        else:
            return "Usuario o libro no encontrado."

    def devolver_libro(self, id_usuario, titulo_libro):
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        libro = next((l for l in self.libros if l.titulo == titulo_libro), None)

        if usuario and libro:
            if usuario.devolver_libro(libro):
                return f"El libro '{libro.titulo}' ha sido devuelto por {usuario.nombre}."
            else:
                return f"El libro '{libro.titulo}' no estaba prestado a {usuario.nombre}."
        else:
            return "Usuario o libro no encontrado."

    def mostrar_libros_disponibles(self):
        cursor.execute("SELECT titulo, autor, año_publicacion FROM Libros WHERE disponible = 1")
        disponibles = cursor.fetchall()
        if disponibles:
            return "Libros disponibles en la biblioteca:\n" + "\n".join([f"'{fila[0]}' por {fila[1]} ({fila[2]}) - Disponible" for fila in disponibles])
        else:
            return "No hay libros disponibles en la biblioteca."

    def mostrar_libros_prestados_usuario(self, id_usuario):
        cursor.execute("SELECT L.titulo, L.autor, L.año_publicacion FROM Libros L JOIN Prestamos P ON L.id = P.id_libro WHERE P.id_usuario = ? AND P.fecha_devolucion IS NULL", id_usuario)
        prestados = cursor.fetchall()
        if prestados:
            return f"Libros prestados a {id_usuario}:\n" + "\n".join([f"'{fila[0]}' por {fila[1]} ({fila[2]}) - Prestado" for fila in prestados])
        else:
            return f"{id_usuario} no tiene libros prestados."


# Crear una biblioteca
mi_biblioteca = Biblioteca()

# Menú interactivo
while True:
    print("\n--- Menú de la Biblioteca ---")
    print("1. Añadir libro a la biblioteca")
    print("2. Añadir usuario")
    print("3. Prestar libro")
    print("4. Devolver libro")
    print("5. Libros prestados del usuario")
    print("6. Libros disponibles")
    print("7. Salir")

    opcion = input("Elige una opción (1-7): ")

    if opcion == "1":  # Añadir libro
        entrada = input("Introduce el libro en formato 'Título, Autor, Año': ")
        try:
            titulo, autor, año = [parte.strip() for parte in entrada.split(",")]
            año = int(año)  # Convertir el año a entero
            libro = Libro(titulo, autor, año)
            print(mi_biblioteca.añadir_libro(libro))
        except ValueError:
            print("Formato incorrecto. Usa 'Título, Autor, Año'.")    

    elif opcion == "2":  # Añadir usuario
        nombre = input("Introduce el nombre del usuario: ")
        usuario = Usuario(nombre)  # El ID se genera automáticamente
        print(mi_biblioteca.registrar_usuario(usuario))

    elif opcion == "3":  # Prestar libro
        id_usuario = input("Introduce el ID del usuario: ")
        titulo_libro = input("Introduce el título del libro a prestar: ")
        print(mi_biblioteca.prestar_libro(id_usuario, titulo_libro))

    elif opcion == "4":  # Devolver libro
        id_usuario = input("Introduce el ID del usuario: ")
        titulo_libro = input("Introduce el título del libro a devolver: ")
        print(mi_biblioteca.devolver_libro(id_usuario, titulo_libro))

    elif opcion == "5":  # Libros prestados del usuario
        id_usuario = input("Introduce el ID del usuario: ")
        print(mi_biblioteca.mostrar_libros_prestados_usuario(id_usuario))

    elif opcion == "6":  # Libros disponibles
        print(mi_biblioteca.mostrar_libros_disponibles())

    elif opcion == "7":  # Salir
        print("¡Gracias por usar el sistema de gestión de la biblioteca!")
        break

    else:
        print("Opción no válida. Por favor, elige una opción del 1 al 7.")