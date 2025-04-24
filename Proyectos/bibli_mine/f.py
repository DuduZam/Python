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
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
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
                    """, id_libro, datetime.datetime.now(), f"Se creó el libro: {self.titulo}")
                    conn.commit()
            except Exception as e:
                print(f"Error al guardar el libro: {e}")
            finally:
                conn.close()

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
            conn = ConexionBD.conectar()
            if conn:
                try:
                    cursor = conn.cursor()
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
                except Exception as e:
                    print(f"Error al modificar el libro: {e}")
                finally:
                    conn.close()

                return f"El libro '{self.titulo}' ha sido modificado. Cambios realizados: " + " ".join(cambios)
            else:
                return "Error al conectar con la base de datos."
        else:
            return "No se realizaron cambios al libro."

    def eliminar_libro(self):
        if self.eliminado == 1:
            return "El libro ya está marcado como eliminado."

        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Libros
                    SET eliminado = 1
                    WHERE id = ?
                """, self.id)
                conn.commit()

                cursor.execute("""
                    INSERT INTO Historial_Libros (id_libro, fecha_cambio, detalle)
                    VALUES (?, ?, ?)
                """, self.id, datetime.datetime.now(), f"El libro '{self.titulo}' ha sido eliminado.")
                conn.commit()

                self.eliminado = 1  # Actualizar el atributo eliminado en la instancia
            except Exception as e:
                print(f"Error al eliminar el libro: {e}")
            finally:
                conn.close()

            return f"El libro '{self.titulo}' ha sido eliminado."

    @classmethod
    def buscar_por_titulo(cls, titulo):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Libros WHERE titulo = ? AND eliminado = 0", titulo)
                row = cursor.fetchone()
                if row:
                    # Solo pasamos los argumentos necesarios al constructor
                    return cls(row.titulo, row.autor, row.año_publicacion, row.id)
            except Exception as e:
                print(f"Error al buscar el libro por título: {e}")
            finally:
                conn.close()
        return None

    @classmethod
    def buscar_por_id(cls, libro_id):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Incluir el campo 'eliminado' en la consulta
                cursor.execute("""
                    SELECT id, titulo, autor, año_publicacion, eliminado 
                    FROM Libros 
                    WHERE id = ?
                """, (libro_id,))
                
                resultado = cursor.fetchone()
                
                if resultado:
                    eliminado = resultado[4]  # Índice 4 corresponde a 'eliminado'
                    
                    if eliminado == 1:
                        return "eliminado"
                    else:
                        # Retorna el objeto solo si no está eliminado
                        return cls(
                            titulo=resultado[1],
                            autor=resultado[2],
                            año_publicacion=resultado[3],
                            id=resultado[0]
                        )
                else:
                    return None  # Libro no encontrado
                
            except Exception as e:
                print(f"Error al buscar el libro por ID: {e}")
                return None
            finally:
                conn.close()
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
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Usuarios (id, nombre)
                    VALUES (?, ?)
                """, self.id_usuario, self.nombre)
                conn.commit()

                cursor.execute("""
                    INSERT INTO Historial_Usuarios (id_usuario, fecha_cambio, detalle)
                    VALUES (?, ?, ?)
                """, self.id_usuario, datetime.datetime.now(), f"Se registro el usuario: '{self.nombre}'")
                conn.commit()
            except Exception as e:
                print(f"Error al guardar el usuario: {e}")
            finally:
                conn.close()

    def actualizar(self, nuevo_nombre):
        self.nombre = nuevo_nombre
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Usuarios
                    SET nombre = ?
                    WHERE id = ?
                """, self.nombre, self.id_usuario)
                conn.commit()

                cursor.execute("""
                    INSERT INTO Historial_Usuarios (id_usuario, fecha_cambio, detalle)
                    VALUES (?, ?, ?)
                """, self.id_usuario, datetime.datetime.now(), f"Modificación del nombre a: '{self.nombre}'")
                conn.commit()
            except Exception as e:
                print(f"Error al actualizar el usuario: {e}")
            finally:
                conn.close()

    def eliminar(self):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Usuarios
                    SET eliminado = 1
                    WHERE id = ?
                """, self.id_usuario)
                conn.commit()

                cursor.execute("""
                    INSERT INTO Historial_Usuarios (id_usuario, fecha_cambio, detalle)
                    VALUES (?, ?, ?)
                """, self.id_usuario, datetime.datetime.now(), f"Usuario Eliminado: '{self.nombre}'")
                conn.commit()
            except Exception as e:
                print(f"Error al eliminar el usuario: {e}")
            finally:
                conn.close()

    @classmethod
    def buscar_por_id(cls, id_usuario):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Usuarios WHERE id = ?", id_usuario)
                row = cursor.fetchone()
                if row:
                    return cls(row.nombre, row.id)
            except Exception as e:
                print(f"Error al buscar el usuario por ID: {e}")
            finally:
                conn.close()
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
        f_d = datetime.datetime.now() + datetime.timedelta(weeks=1)  # Fecha de devolución programada

        if usuario and libro:
            conn = ConexionBD.conectar()
            if conn:
                try:
                    cursor = conn.cursor()

                    # Verificar si el libro está disponible
                    cursor.execute("SELECT disponible FROM Libros WHERE id = ?", (libro.id,))
                    disponibilidad = cursor.fetchone()

                    if disponibilidad and disponibilidad.disponible == 1:
                        # Registrar el préstamo en la tabla Prestamos
                        cursor.execute("""
                            INSERT INTO Prestamos (id_usuario, id_libro, fecha_prestamo)
                            VALUES (?, ?, ?)
                        """, (usuario.id_usuario, libro.id, datetime.datetime.now()))

                        # Actualizar el estado del libro a "no disponible"
                        cursor.execute("UPDATE Libros SET disponible = 0 WHERE id = ?", (libro.id,))

                        # Registrar el cambio en Historial_Usuarios
                        cursor.execute("""
                            INSERT INTO Historial_Usuarios (id_usuario, fecha_cambio, detalle)
                            VALUES (?, ?, ?)
                        """, (usuario.id_usuario, datetime.datetime.now(), f"Préstamo del libro: '{libro.titulo}' al usuario: '{usuario.nombre}'"))

                        conn.commit()  # Confirmar todas las operaciones
                        return f"El libro '{libro.titulo}' ha sido prestado a '{usuario.nombre}'.\nFecha programada para la devolución: '{f_d}'."
                    else:
                        # Obtener el nombre del usuario que tiene el libro prestado
                        cursor.execute("""
                            SELECT u.nombre
                            FROM Prestamos p
                            JOIN Usuarios u ON p.id_usuario = u.id
                            WHERE p.id_libro = ? AND p.fecha_devolucion IS NULL
                        """, (libro.id,))
                        usuario_prestamo = cursor.fetchone()

                        if usuario_prestamo:
                            return f"El libro '{libro.titulo}' no está disponible. Lo tiene prestado el usuario: '{usuario_prestamo.nombre}'."
                        else:
                            return f"El libro '{libro.titulo}' no está disponible, pero no se pudo determinar quién lo tiene prestado."
                except Exception as e:
                    print(f"Error al prestar el libro: {e}")
                finally:
                    conn.close()
        else:
            return "Usuario o libro no encontrado."

    def devolver_libro(self, id_usuario, titulo_libro):
        usuario = Usuario.buscar_por_id(id_usuario)
        libro = Libro.buscar_por_titulo(titulo_libro)

        if usuario and libro:
            conn = ConexionBD.conectar()
            if conn:
                try:
                    # Registrar la devolucion en la tabla Prestamos
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE Prestamos
                        SET fecha_devolucion = ?
                        WHERE id_usuario = ? AND id_libro = ? AND fecha_devolucion IS NULL
                    """, datetime.datetime.now(), usuario.id_usuario, libro.id)

                    # Actualizar el estado del libro a "Disponible"                 
                    cursor.execute("UPDATE Libros SET disponible = 1 WHERE id = ?", libro.id)
                    
                    # Registrar el cambio en Historial_Usuarios
                    cursor.execute("""
                        INSERT INTO Historial_Usuarios (id_usuario, fecha_cambio, detalle)
                        VALUES (?, ?, ?)
                    """, usuario.id_usuario, datetime.datetime.now(), f"Devolucion del libro: '{libro.titulo}' de parte del usuario: '{usuario.nombre}'")

                    conn.commit() # Confirmar todas las operaciones                    
                    return f"El libro '{libro.titulo}' ha sido devuelto por {usuario.nombre}."
                except Exception as e:
                    print(f"Error al devolver el libro: {e}")
                finally:
                    conn.close()
        else:
            return "Usuario o libro no encontrado."

    def historial_cambios_libro(self, id_libro):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM Historial_Libros WHERE id_libro = ?
                """, id_libro)
                cambios = cursor.fetchall()
                if cambios:
                    return "\n".join([f"Fecha: {cambio.fecha_cambio}, Cambio: {cambio.detalle}"
                                      for cambio in cambios])
            except Exception as e:
                print(f"Error al obtener el historial de cambios del libro: {e}")
            finally:
                conn.close()
        return "No hay historial de cambios para este libro."

    def historial_prestamos_usuario(self, id_usuario):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Consulta para obtener los préstamos del usuario, incluyendo el título del libro
                cursor.execute("""
                    SELECT p.id, l.titulo, p.fecha_prestamo, p.fecha_devolucion
                    FROM Prestamos p
                    JOIN Libros l ON p.id_libro = l.id
                    WHERE p.id_usuario = ?
                    ORDER BY p.fecha_prestamo DESC
                """, id_usuario)
                prestamos = cursor.fetchall()

                if prestamos:
                    # Formatear los resultados para mostrarlos
                    historial = []
                    for prestamo in prestamos:
                        id_prestamo, titulo_libro, fecha_prestamo, fecha_devolucion = prestamo
                        estado = "Devuelto" if fecha_devolucion else "Prestado"
                        historial.append(
                            f"Préstamo ID: {id_prestamo}\n"
                            f"Libro: {titulo_libro}\n"
                            f"Fecha de préstamo: {fecha_prestamo}\n"
                            f"Fecha de devolución: {fecha_devolucion if fecha_devolucion else 'No devuelto'}\n"
                            f"Estado: {estado}\n"
                        )
                    return "\n".join(historial)
                else:
                    return "El usuario no tiene préstamos registrados."
            except Exception as e:
                print(f"Error al obtener el historial de préstamos: {e}")
                return "Error al obtener el historial de préstamos."
            finally:
                conn.close()
        return "Error al conectar con la base de datos."

    def historial_cambios_usuario(self, id_usuario):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM Historial_Usuarios WHERE id_usuario = ?
                """, id_usuario)
                cambios = cursor.fetchall()
                if cambios:
                    return "\n".join([f"Fecha: {cambio.fecha_cambio}, Cambio: {cambio.detalle}"
                                      for cambio in cambios])
            except Exception as e:
                print(f"Error al obtener el historial de cambios del usuario: {e}")
            finally:
                conn.close()
        return "No hay historial de cambios para este usuario."

    def libros_prestados_usuario(self, id_usuario):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Consulta para obtener los libros prestados y no devueltos
                cursor.execute("""
                    SELECT l.titulo, l.autor, p.fecha_prestamo
                    FROM Prestamos p
                    JOIN Libros l ON p.id_libro = l.id
                    WHERE p.id_usuario = ? AND p.fecha_devolucion IS NULL
                    ORDER BY p.fecha_prestamo DESC
                """, id_usuario)
                libros_prestados = cursor.fetchall()

                if libros_prestados:
                    # Formatear los resultados para mostrarlos
                    resultado = []
                    for libro in libros_prestados:
                        titulo, autor, fecha_prestamo = libro
                        resultado.append(
                            f"Libro: '{titulo}' - {autor}\n"                            
                            f"Fecha de préstamo: {fecha_prestamo}\n"
                        )
                    return "\n".join(resultado)
                else:
                    return "El usuario no tiene libros prestados actualmente."
            except Exception as e:
                print(f"Error al obtener los libros prestados: {e}")
                return "Error al obtener los libros prestados."
            finally:
                conn.close()
        return "Error al conectar con la base de datos."

    def mostrar_libros(self, disponibilidad=None):
        conn = ConexionBD.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                if disponibilidad is not None:
                    cursor.execute("SELECT * FROM Libros WHERE disponible = ? AND eliminado = 0", disponibilidad)
                else:
                    cursor.execute("SELECT * FROM Libros WHERE eliminado = 0")

                libros = cursor.fetchall()
                if libros:
                    return "\n".join([f"ID: {libro.id}, Título: {libro.titulo}, Autor: {libro.autor}, Año: {libro.año_publicacion}, Disponible: {'Sí' if libro.disponible else 'No'}"
                                      for libro in libros])
            except Exception as e:
                print(f"Error al mostrar los libros: {e}")
            finally:
                conn.close()
        return "No hay libros disponibles en la biblioteca."    



def menu():
    biblioteca = Biblioteca()
    while True:
        print("\n--- Menú de la Biblioteca ---")
        print("BIBLIOTECA")
        print("1. Añadir libro a la biblioteca")
        print("2. Modificar libro de la biblioteca")
        print("3. Eliminación un libro")
        print("4. Historial de cambios del libro")
        print("5. Historial de cambios del usuario")
        print("6. Mostrar todos los libros")
        print("USUARIO")
        print("7. Añadir usuario")
        print("8. Modificar usuario")
        print("9. Eliminar usuario")
        print("10. Prestar libro")
        print("11. Devolver libro")
        print("12. Historial de préstamos del usuario")
        print("13. Libros no devueltos del usuario")
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
            libro = Libro.buscar_por_id(libro_id)  # Método para buscar libro por ID
            if libro == "eliminado":
                print("Libro no encontrado.")
            else:
                nuevo_titulo = input("Nuevo título (deja en blanco para no cambiar): ")
                nuevo_autor = input("Nuevo autor (deja en blanco para no cambiar): ")
                nuevo_año = input("Nuevo año de publicación (deja en blanco para no cambiar): ")
                nuevo_año = int(nuevo_año) if nuevo_año else None
                print(libro.modificar(nuevo_titulo, nuevo_autor, nuevo_año))

        elif opcion == "3":
            libro_id = int(input("Introduce el ID del libro a eliminar lógicamente: "))
            libro = Libro.buscar_por_id(libro_id)  # Método para buscar libro por ID
            if libro == "eliminado":
                print("Libro no encontrado.")
            else:
                print(libro.eliminar_libro())  # Método para eliminar libro lógicamente

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
