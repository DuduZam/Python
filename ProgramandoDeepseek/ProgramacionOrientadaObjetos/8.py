from typing import List

class Usuario:
    nesecidades = ["caca"]
    # nesecidades: List[str] como poner el tipo de dato que sera la lista
    
    def __init__(self,nombre: str):
        self.nombre_pila = nombre
        
    def info_usuario(self):
        # Dividir en el penúltimo y último elemento
        if len(self.nesecidades) > 1:
            necesidades_formateadas = ", ".join(self.nesecidades[:-1]) + " y " + self.nesecidades[-1]
        else:
            necesidades_formateadas = self.nesecidades[0]  # Si hay solo una necesidad
        
        return f"El usuario: {self.nombre_pila} hace {necesidades_formateadas}."
    
    @classmethod
    def añadir_nesecidades(cls, nuevas_nesecidades: List[str]) -> List[str]:
        # Usamos cls para trabajar con el atributo de clase
        cls.nesecidades.extend(nuevas_nesecidades)
        return cls.nesecidades
    
persona = Usuario("Kebel")
persona.añadir_nesecidades(["pis"])
#persona.añadir_nesecidades(["comer"])

print(persona.info_usuario())

persona.añadir_nesecidades(["Bañar","cañar","canchis canchis"])

print(persona.info_usuario())