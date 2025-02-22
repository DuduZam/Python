import pyodbc
import datetime
import random

class ConexionBD:
    connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-A2S73Q8;DATABASE=BibliotecaDB;UID=sa;PWD=imilla555"

    @staticmethod
    def conectar():
        """Método estático para conectar a la base de datos."""
        try:
            conn = pyodbc.connect(ConexionBD.connection_string)
            return conn
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None

# Clase Libro
class Libro:
    def __init__(self, titulo, autor, año_publicacion, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.año_publicacion = año_publicacion
        self.disponible = True  # El libro siempre estará disponible al momento de su creación        
        self.eliminado = 0

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"'{self.titulo}' por {self.autor} ({self.año_publicacion}) - {estado}"

    def guardar(self):
        # Ahora no se inserta 'disponible', ya que se maneja automáticamente en la BD
        cursor.execute("""
            INSERT INTO Libros (titulo, autor, año_publicacion)
            VALUES (?, ?, ?)
        """, self.titulo, self.autor, self.año_publicacion)
        conn.commit()

        # Obtener el ID del libro recién insertado para registrar el cambio
        cursor.execute("SELECT @@IDENTITY AS id_libro")
        row = cursor.fetchone()
        id_libro = row.id_libro if row else None

        # Insertar el cambio en el historial de libros (registro de creación)
        if id_libro:
            cursor.execute("""
                INSERT INTO Historial_Libros (id_libro, fecha_cambio, detalle)
                VALUES (?, ?, ?)
            """, id_libro, datetime.datetime.now(), "Creación de libro")
            conn.commit()    

    def modificar(self, nuevo_titulo=None, nuevo_autor=None, nuevo_año=None):
    cambios = []

    if nuevo_titulo and nuevo_titulo != self.titulo:
        self.titulo = nuevo_titulo
        cambios.append(f"Se cambió el título a '{self.titulo}'.")

    if nuevo_autor and nuevo_autor != self.autor:
        self.autor = nuevo_autor
        cambios.append(f"Se cambió el autor a '{self.autor}'.")

    if nuevo_año and nuevo_año != self.año_publicacion:
        self.año_publicacion = nuevo_año
        cambios.append(f"Se cambió el año de publicación a {self.año_publicacion}.")

    if cambios:
        conn = ConexionBD.conectar()  # Establecer conexión
        if conn:  # Verificar que la conexión se haya establecido correctamente
            cursor = conn.cursor()  # Obtener el cursor a partir de la conexión
            cursor.execute(""" 
                UPDATE Libros
                SET titulo = ?, autor = ?, año_publicacion = ?
                WHERE id = ?
            """, self.titulo, self.autor, self.año_publicacion, self.id)
            conn.commit()

            # Registrar los cambios en el historial
            for detalle in cambios:
                cursor.execute("""
                    INSERT INTO Historial_Libros (id_libro, fecha_cambio, detalle)
                    VALUES (?, ?, ?)
                """, self.id, datetime.datetime.now(), detalle)
            conn.commit()

            conn.close()  # Cerrar la conexión al final

            return f"El libro '{self.titulo}' ha sido modificado. Cambios realizados: " + " ".join(cambios)
        else:
            return "Error al conectar con la base de datos."

    else:
        return "No se realizaron cambios al libro."    

    def eliminar_libro(self):
        if self.eliminado == 1:
            return "El libro ya está marcado como eliminado."

        # Marcar el libro como eliminado en la base de datos
        cursor.execute("""
            UPDATE Libros
            SET eliminado = 1
            WHERE id = ?
        """, self.id)
        conn.commit()

        # Registrar el cambio en el historial de cambios
        cursor.execute("""
            INSERT INTO Historial_Libros (id_libro, fecha, detalle)
            VALUES (?, ?, ?)
        """, self.id, datetime.datetime.now(), "Eliminación lógica de libro")
        conn.commit()

        self.eliminado = 1  # Actualizar el atributo eliminado en la instancia
        return f"El libro '{self.titulo}' ha sido eliminado lógicamente."

    @classmethod
    def buscar_por_titulo(cls, titulo):
        cursor.execute("SELECT * FROM Libros WHERE titulo = ? AND eliminado = 0", titulo)
        row = cursor.fetchone()
        if row:
            return cls(row.titulo, row.autor, row.año_publicacion, row.id, row.disponible)
        return None

    @classmethod
    def buscar_por_id(cls, libro_id):
        conn = ConexionBD.conectar()  # Usar el método estático
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, autor, año_publicacion FROM Libros WHERE id = ?", (libro_id,))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                return cls(resultado[1], resultado[2], resultado[3], resultado[0])  
        return None

# Clase Usuario
class Usuario:
    def __init__(self, nombre, id_usuario=None):
        self.nombre = nombre
        self.id_usuario = id_usuario if id_usuario else self.generar_id_unico()

    def generar_id_unico(self):
        fecha_actual = datetime.datetime.now().strftime("%d%m%Y")  # Fecha en formato DDMMYYYY
        numero_aleatorio = f"{random.randint(0, 9999):04d}"  # Número aleatorio de 4 dígitos
        return f"{fecha_actual}{self.nombre[:3].upper()}{numero_aleatorio}"  # ID único

    def __str__(self):
        return f"Usuario: {self.nombre}, ID: {self.id_usuario}"

    def guardar(self):
        # Guardar usuario en la base de datos
        cursor.execute("""
            INSERT INTO Usuarios (id, nombre)
            VALUES (?, ?)
        """, self.id_usuario, self.nombre)
        conn.commit()

        # Registrar el cambio en el historial de usuarios (creación)
        cursor.execute("""
            INSERT INTO Historial_Usuarios (id_usuario, fecha, detalle)
            VALUES (?, ?, ?)
        """, self.id_usuario, datetime.datetime.now(), "Registro de usuario")
        conn.commit()

    def actualizar(self, nuevo_nombre):
        self.nombre = nuevo_nombre
        cursor.execute("""
            UPDATE Usuarios
            SET nombre = ?
            WHERE id = ?
        """, self.nombre, self.id_usuario)
        conn.commit()

        # Registrar el cambio en el historial de usuarios (modificación)
        cursor.execute("""
            INSERT INTO Historial_Usuarios (id_usuario, fecha, detalle)
            VALUES (?, ?, ?)
        """, self.id_usuario, datetime.datetime.now(), f"Modificación del nombre a '{self.nombre}'")
        conn.commit()

    def eliminar(self):
        cursor.execute("""
            UPDATE Usuarios
            SET eliminado = 1
            WHERE id = ?
        """, self.id_usuario)
        conn.commit()

        # Registrar el cambio en el historial de usuarios (eliminación lógica)
        cursor.execute("""
            INSERT INTO Historial_Usuarios (id_usuario, fecha, detalle)
            VALUES (?, ?, ?)
        """, self.id_usuario, datetime.datetime.now(), "Eliminación lógica de usuario")
        conn.commit()

    @classmethod
    def buscar_por_id(cls, id_usuario):
        cursor.execute("SELECT * FROM Usuarios WHERE id = ?", id_usuario)
        row = cursor.fetchone()
        if row:
            return cls(row.nombre, row.id)
        return None

# Clase Biblioteca
class Biblioteca:
    def añadir_libro(self, libro):
        libro.guardar()
        return f"El libro '{libro.titulo}' ha sido añadido a la biblioteca."

    def registrar_usuario(self, usuario):
        usuario.guardar()
        return f"El usuario '{usuario.nombre}' ha sido registrado en la biblioteca con ID: {usuario.id_usuario}."

    def prestar_libro(self, id_usuario, titulo_libro):
        usuario = Usuario.buscar_por_id(id_usuario)
        libro = Libro.buscar_por_titulo(titulo_libro)

        if usuario and libro and libro.disponible:
            cursor.execute("""
                INSERT INTO Prestamos (id_usuario, id_libro, fecha_prestamo)
                VALUES (?, ?, ?)
            """, usuario.id_usuario, libro.id, datetime.datetime.now())
            cursor.execute("UPDATE Libros SET disponible = 0 WHERE id = ?", libro.id)
            conn.commit()
            return f"El libro '{libro.titulo}' ha sido prestado a {usuario.nombre}."
        else:
            return "Usuario o libro no encontrado, o el libro no está disponible."

    def devolver_libro(self, id_usuario, titulo_libro):
        usuario = Usuario.buscar_por_id(id_usuario)
        libro = Libro.buscar_por_titulo(titulo_libro)

        if usuario and libro:
            cursor.execute("""
                UPDATE Prestamos
                SET fecha_devolucion = ?
                WHERE id_usuario = ? AND id_libro = ? AND fecha_devolucion IS NULL
            """, datetime.datetime.now(), usuario.id_usuario, libro.id)
            cursor.execute("UPDATE Libros SET disponible = 1 WHERE id = ?", libro.id)
            conn.commit()
            return f"El libro '{libro.titulo}' ha sido devuelto por {usuario.nombre}."
        else:
            return "Usuario o libro no encontrado."

    def historial_cambios_libro(self, id_libro):
        cursor.execute("""
            SELECT * FROM HistorialLibros WHERE id_libro = ?
        """, id_libro)
        cambios = cursor.fetchall()
        if cambios:
            return "\n".join([f"Fecha: {cambio.fecha}, Cambio: {cambio.cambio}"
                              for cambio in cambios])
        else:
            return "No hay historial de cambios para este libro."

    def historial_cambios_usuario(self, id_usuario):
        cursor.execute("""
            SELECT * FROM HistorialUsuarios WHERE id_usuario = ?
        """, id_usuario)
        cambios = cursor.fetchall()
        if cambios:
            return "\n".join([f"Fecha: {cambio.fecha}, Cambio: {cambio.cambio}"
                              for cambio in cambios])
        else:
            return "No hay historial de cambios para este usuario."

    # Método para mostrar todos los libros con filtro de disponibilidad
    def mostrar_libros(self, disponibilidad=None):
        if disponibilidad is not None:
            # Filtrar según disponibilidad (0 para no disponible, 1 para disponible)
            cursor.execute("SELECT * FROM Libros WHERE disponible = ? AND eliminado = 0", disponibilidad)
        else:
            # Mostrar todos los libros sin filtrar por disponibilidad
            cursor.execute("SELECT * FROM Libros WHERE eliminado = 0")

        libros = cursor.fetchall()
        
        if libros:
            # Retornar los libros encontrados con detalles
            return "\n".join([f"ID: {libro.id}, Título: {libro.titulo}, Autor: {libro.autor}, Año: {libro.año_publicacion}, Disponible: {'Sí' if libro.disponible else 'No'}"
                              for libro in libros])
        else:
            return "No hay libros disponibles en la biblioteca."

def menu():
    biblioteca = Biblioteca()
    while True:
        print("\n--- Menú de la Biblioteca ---")
        print("BIBLIOTECA")
        print("1. Añadir libro a la biblioteca")
        print("2. Modificar libro de la biblioteca")
        print("3. Eliminación lógica de un libro")
        print("4. Historial de cambios del libro")
        print("5. Historial de cambios del usuario")
        print("6. Mostrar todos los libros")
        print("USUARIO")
        print("7. Añadir usuario")
        print("8. Modificar usuario")
        print("9. Eliminar lógica usuario")
        print("10. Prestar libro")
        print("11. Devolver libro")
        print("12. Historial de préstamos del usuario")
        print("13. Libros prestados del usuario actuales")
        print("14. Salir")

        opcion = input("Elige una opción (1-14): ")

        # Procesar las opciones del menú
        if opcion == "1":
            entrada = input("Introduce el libro en formato 'Título, Autor, Año': ")
            try:
                titulo, autor, año = [parte.strip() for parte in entrada.split(",")]
                año = int(año)  # Convertir el año a entero
                libro = Libro(titulo, autor, año)
                print(biblioteca.añadir_libro(libro))
            except ValueError:
                print("Formato incorrecto. Usa 'Título, Autor, Año'.")
                
        elif opcion == "2":
            libro_id = int(input("Introduce el ID del libro a modificar: "))
            nuevo_titulo = input("Nuevo título (deja en blanco para no cambiar): ")
            nuevo_autor = input("Nuevo autor (deja en blanco para no cambiar): ")
            nuevo_año = input("Nuevo año de publicación (deja en blanco para no cambiar): ")
            nuevo_año = int(nuevo_año) if nuevo_año else None
            libro = Libro.buscar_por_id(libro_id)  # Método para buscar libro por ID
            if libro:
                print(libro.modificar(nuevo_titulo, nuevo_autor, nuevo_año))
            else:
                print("Libro no encontrado.")

        elif opcion == "3":
            libro_id = int(input("Introduce el ID del libro a eliminar lógicamente: "))
            libro = Libro.buscar_por_id(libro_id)  # Método para buscar libro por ID
            if libro:
                print(libro.eliminar_libro())  # Método para eliminar libro lógicamente
            else:
                print("Libro no encontrado.")

        elif opcion == "4":
            libro_id = int(input("Introduce el ID del libro para ver su historial de cambios: "))
            print(biblioteca.historial_cambios_libro(libro_id))

        elif opcion == "5":
            usuario_id = input("Introduce el ID del usuario para ver su historial de cambios: ")
            print(biblioteca.historial_cambios_usuario(usuario_id))

        elif opcion == "6":
            filtro = input("¿Deseas filtrar por disponibilidad? (S/N): ").strip().upper()
            if filtro == "S":
                disponibilidad = input("Introduce '1' para disponibles o '0' para no disponibles: ").strip()
                if disponibilidad in ["1", "0"]:
                    print(biblioteca.mostrar_libros(int(disponibilidad)))
                else:
                    print("Opción no válida.")
            else:
                print(biblioteca.mostrar_libros())

        elif opcion == "7":
            nombre = input("Introduce el nombre del nuevo usuario: ")
            usuario = Usuario(nombre)
            print(biblioteca.registrar_usuario(usuario))

        elif opcion == "8":
            usuario_id = input("Introduce el ID del usuario a modificar: ")
            nuevo_nombre = input("Introduce el nuevo nombre del usuario: ")
            usuario = Usuario.buscar_por_id(usuario_id)
            if usuario:
                usuario.actualizar(nuevo_nombre)
                print(f"El nombre del usuario ha sido actualizado a '{nuevo_nombre}'.")
            else:
                print("Usuario no encontrado.")

        elif opcion == "9":
            usuario_id = input("Introduce el ID del usuario a eliminar lógicamente: ")
            usuario = Usuario.buscar_por_id(usuario_id)
            if usuario:
                usuario.eliminar()  # Elimina el usuario lógicamente
                print(f"El usuario '{usuario.nombre}' ha sido eliminado lógicamente.")
            else:
                print("Usuario no encontrado.")

        elif opcion == "10":
            usuario_id = input("Introduce el ID del usuario: ")
            titulo_libro = input("Introduce el título del libro a prestar: ")
            print(biblioteca.prestar_libro(usuario_id, titulo_libro))

        elif opcion == "11":
            usuario_id = input("Introduce el ID del usuario: ")
            titulo_libro = input("Introduce el título del libro a devolver: ")
            print(biblioteca.devolver_libro(usuario_id, titulo_libro))

        elif opcion == "12":
            usuario_id = input("Introduce el ID del usuario para ver su historial de préstamos: ")
            print(biblioteca.historial_prestamos_usuario(usuario_id))

        elif opcion == "13":
            usuario_id = input("Introduce el ID del usuario para ver los libros prestados actualmente: ")
            print(biblioteca.libros_prestados_usuario(usuario_id))

        elif opcion == "14":
            print("¡Gracias por usar el sistema de gestión de la biblioteca!")
            break

        else:
            print("Opción no válida. Por favor, elige una opción del 1 al 14.")


menu()