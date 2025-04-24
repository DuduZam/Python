class Vehiculo():
    """"""
    # Atributos
    color = None
    longitud_metros = None
    ruedas = 4
    
    # Metodos
    def arrancar(self):
        print("El motor ah arrancado.")
        
    def detener(self):
        print("El motor está detenido.")
        
# Objeto creado a partir de la clase
objeto_vehiculo_1 = Vehiculo()
objeto_vehiculo_2 = Vehiculo()

objeto_vehiculo_1.color = "Negro"
objeto_vehiculo_2.color = "Azul"

print(objeto_vehiculo_1.color)
print(objeto_vehiculo_2.color)