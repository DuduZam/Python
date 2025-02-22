print("\nQUINTO EJERCICIO PYTHON DEEPSEEK")

class Vehiculo:
    def __init__(self, marca, modelo, año):
        self.marca = marca
        self.modelo = modelo
        self.año = año

    def descripcion(self):
        return f"{self.marca} {self.modelo} ({self.año})"


class Coche(Vehiculo):
    def __init__(self, marca, modelo, año, color):
        super().__init__(marca, modelo, año)
        self.color = color

    def descripcion(self):
        return f"{super().descripcion()}, Color: {self.color}"


class Moto(Vehiculo):
    def __init__(self, marca, modelo, año, cilindrada):
        super().__init__(marca, modelo, año)
        self.cilindrada = cilindrada

    def descripcion(self):
        return f"{super().descripcion()}, Cilindrada: {self.cilindrada}cc."

class Camion(Vehiculo):
    def __init__(self, marca, modelo, año, capacidad_carga):
        super().__init__(marca, modelo, año)
        self.capacidad_carga = capacidad_carga

    def descripcion(self):
        return f"{super().descripcion()}, Capacidad de carga: {self.capacidad_carga} toneladas."

class Flota:
    def __init__(self):
        self.coches = []

    def añadir_coche(self, coche):
        self.coches.append(coche)

    def __str__(self):
        return f'Flota con {len(self.coches)} coches: {", ".join(str(coche) for coche in self.coches)}'
    

class Garaje(Flota):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    # Sobrescribe el método __str__ aquí


# Crear objetos
mi_coche = Coche("Toyota", "Corolla", 2020, "Rojo")
mi_moto = Moto("Honda", "CBR", 2019, 600)
mi_camion = Camion("Volvo", "FH16", 2021, 40)

# Usar polimorfismo
for vehiculo in [mi_coche, mi_moto, mi_camion]:
    print(vehiculo.descripcion())