from datetime import datetime
class Usuario():
    """"""
    #Atributos de Clase
    hora_ultimo_inicio = None
    
    # Atributos de Instancia
    # Constructor
    def __init__(self, nombre, apellido, edad, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad        
        self.telefono = telefono
        
        self.direccion = "sin direccion"
    
    # Metodos
    def iniciar_sesion(self):
        print(f"Usuario {self.nombre} {self.apellido} ha iniciado sesion.")
        self.hora_ultimo_inicio = datetime.now().strftime("%d de %B del %Y a las %H:%Mhrs.")
        
    def cerrar_sesion(self):
        print(f"Usuario {self.nombre} {self.apellido} ha cerrado sesion.")
    
    def mostrar_info(self):
        print(f"Datos Usuario:\nNombre: {self.nombre}\nApellido: {self.apellido}\nEdad: {self.edad}\nCelular: {self.telefono}\nDireccion: {self.direccion}\nUltima Hora de Inicio de Sesion: {self.hora_ultimo_inicio}")
        
    def modificar_datos(self, nombre=None, apellido=None, edad=None, telefono=None, direccion=None):
        if nombre is not None:
            print(f"Se cambió el nombre de {self.nombre} a {nombre}.")
            self.nombre = nombre
        if apellido is not None:
            print(f"Se cambió el apellido de {self.apellido} a {apellido}.")
            self.apellido = apellido
        if edad is not None:
            print(f"Se cambió la edad de {self.edad} a {edad}.")
            self.edad = edad
        if telefono is not None:
            print(f"Se cambió el teléfono de {self.telefono} a {telefono}.")
            self.telefono = telefono
        if direccion is not None:
            print(f"Se cambió la dirección de {self.direccion} a {direccion}.")
            self.direccion = direccion
    """def cambiar_nombre_perfil(self,nuevo_nombre):
        print(f"Usuario {self.nombre} {self.apellido} se cambio el nombre a {nuevo_nombre} {self.apellido}.")
        self.nombre = nuevo_nombre"""
    
# Instanciamos un Objeto
usuario1 = Usuario("Pepe", "Zambrana", 52, 71783668) 
usuario1.direccion = "Av. Los Sargentos #74-A"

usuario2 = Usuario("Alejandra", "Chavez", 28, 63512478) 
#usuario2.direccion = "Av. Ballivian #129"

# Nos imprime su informacion en memoria
print(usuario1)
print(usuario2)

# Imprimir valores
#print(f"Usuario: {usuario1.nombre} {usuario1.apellido}\nCelular: {usuario1.telefono}")  

#usuario1.iniciar_sesion()
usuario2.iniciar_sesion()
#usuario2.cambiar_nombre_perfil("America")
#print(usuario2.nombre)
usuario2.mostrar_info()
usuario2.modificar_datos("Carmen","Nina",None,None,"Av. Mario Mercado Calle Los Eucaliptos")
#usuario2.modificar_datos(nombre="Carmen",apellido="Nina",direccion="Av. Mario Mercado Calle Los Eucaliptos")
print("Datos Modificados.\n")
usuario2.mostrar_info()

#print(f"La ultima conexion del usuario {usuario2.nombre} {usuario2.apellido} fue el {usuario2.hora_ultimo_inicio}")
usuario2.cerrar_sesion()

# Salto de linea: Alt + 92

    
    
    
            
