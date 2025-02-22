print("\nTERCER EJERCICIO PYTHON DEEPSEEK")

class Coche:

	def __init__(self, marca, modelo, año):
		self.marca = marca
		self.modelo = modelo
		self.año = año

	def arrancar(self):
		print(f"\nEl coche {self.marca} {self.modelo} está arrancando.")

	def detener(self):
		print(f"El coche {self.marca} {self.modelo} se detuvo.")

	def informacion(self):
		print(f"El coche tiene las siguientes caracteristicas:\nMarca: {self.marca}\nModelo: {self.modelo}\nAño: {self.año}.")


mi_coche = Coche("Toyota","Corolla",2020)
mi_coche.arrancar()
mi_coche.detener()

mi_coche2 = Coche("Ford","F-150","2025")
mi_coche2.arrancar()
mi_coche2.detener()
mi_coche2.informacion()