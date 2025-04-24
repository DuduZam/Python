# Ejemplo avanzado para entender la diferencia entre iteradores e iterables

# Un iterable es cualquier objeto que puede ser recorrido con un bucle (como listas, tuplas, etc.)
# Aquí tenemos un iterable: una lista
mi_lista = [1, 2, 3, 4, 5]

# Podemos recorrerlo directamente porque es iterable
for elemento in mi_lista:
    print(f"Elemento del iterable: {elemento}")

# Sin embargo, un iterable no es un iterador por sí mismo.
# Podemos obtener un iterador a partir de un iterable usando la función iter()
mi_iterador = iter(mi_lista)

# Un iterador es un objeto que implementa los métodos __iter__() y __next__()
# Podemos usar next() para obtener los elementos uno a uno
print("\nUsando el iterador:")
while True:
    try:
        elemento = next(mi_iterador)
        print(f"Elemento del iterador: {elemento}")
    except StopIteration:
        # Cuando no hay más elementos, se lanza StopIteration
        print("El iterador ha terminado.")
        break

# Diferencia clave:
# - Un iterable puede ser recorrido múltiples veces (por ejemplo, con varios bucles for).
# - Un iterador, una vez que se consume, no puede ser reiniciado. Necesitarías crear un nuevo iterador del iterable.

# Ejemplo práctico: Crear un iterable personalizado
class MiIterablePersonalizado:
    def __init__(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin

    def __iter__(self):
        return MiIteradorPersonalizado(self.inicio, self.fin)

class MiIteradorPersonalizado:
    def __init__(self, inicio, fin):
        self.actual = inicio
        self.fin = fin

    def __iter__(self):
        return self

    def __next__(self):
        if self.actual >= self.fin:
            raise StopIteration
        valor = self.actual
        self.actual += 1
        return valor

# Usando el iterable personalizado
print("\nUsando un iterable personalizado:")
mi_iterable = MiIterablePersonalizado(10, 15)
for numero in mi_iterable:
    print(f"Número: {numero}")