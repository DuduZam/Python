print("\nCUARTO EJERCICIO PYTHON DEEPSEEK")

class Coche:
    def __init__(self, marca, modelo, año, color):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.color = color

    def info_coche(self):
        print(f"Información del coche:\nMarca: {self.marca}\nModelo: {self.modelo}\nAño: {self.año}\nColor: {self.color}.")

    def ver_año(self, año):
        return self.año == año  # Devuelve True si el año coincide


class Flota:
    def __init__(self):
        self.coches = []  # Lista vacía para almacenar coches

    def añadir_coche(self, coche):
        if not isinstance(coche.año, int):  # Validar que el año sea un número entero
            print(f"Error: El año del coche {coche.marca} {coche.modelo} no es válido.")
        else:
            self.coches.append(coche)
            print(f"Coche {coche.marca} {coche.modelo} añadido a la flota.")

    def mostrar_coches(self):
        if not self.coches:
            print("No hay coches en la flota.")
        else:
            print("\n--- Coches en la flota ---")
            for coche in self.coches:
                coche.info_coche()

    def buscar_por_marca(self, marca):
        coches_encontrados = [coche for coche in self.coches if coche.marca.lower() == marca.lower()]
        if coches_encontrados:
            print(f"\n--- Coches de la marca {marca} encontrados ---")
            for i, coche in enumerate(coches_encontrados, start=1):
                print(f"{i}.")
                coche.info_coche()
        else:
            print(f"No se encontraron coches de la marca {marca}.")

    def mostrar_coches_año(self, año):
        coches_encontrados = [coche for coche in self.coches if coche.ver_año(año)]
        if coches_encontrados:
            print(f"\n--- Coches del año {año} encontrados ---")
            for i, coche in enumerate(coches_encontrados, start=1):
                print(f"{i}.")
                coche.info_coche()
        else:
            print(f"No se encontraron coches del año {año}.")

    def cant_coches(self):
        return len(self.coches)


# Crear una flota
mi_flota = Flota()

# Añadir coches a la flota
mi_flota.añadir_coche(Coche("Toyota", "Corolla", 2020, "Rojo"))
mi_flota.añadir_coche(Coche("Ford", "Mustang", 2018, "Azul"))
mi_flota.añadir_coche(Coche("Toyota", "Camry", 2020, "Negro"))
mi_flota.añadir_coche(Coche("Honda", "Civic", 2019, "Blanco"))

# Mostrar todos los coches
mi_flota.mostrar_coches()

# Buscar coches por marca
mi_flota.buscar_por_marca("Toyota")

# Mostrar coches de un año específico
mi_flota.mostrar_coches_año(2020)

# Calcular el número total de coches
print(f"\nTotal de coches en la flota: {mi_flota.cant_coches()}")