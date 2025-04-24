# Herencia
class Ciudadano:
    def __init__(self,nombre , profesion):
        self.nombre = nombre
        self.profesion = profesion
        
    def saludar(self):
        return f"Hola soy {self.nombre}.\nMi Profesión es {self.profesion}"
        
class Medico(Ciudadano):
    def __init__(self,nombre,especializacion):
        super().__init__(nombre,"Medico")
        
        self.especializacion = especializacion
    
    def saludar(self):
        super().saludar()  # Usa super() para obtener el saludo base
        return f"{super().saludar()} {self.especializacion}."
    
a = Medico("Favio","Cirujano")
b = Ciudadano("Alfredo","Arquitecto")

print(a.saludar())
#b.saludar()
