"""from typing import Callable


def a() -> None:
    """
    # Función simple que imprime un mensaje.
"""
    print("Hola desde a")

def b(funcion: Callable[[], None]) -> None:
    """
    #Función que toma otra función como argumento, la ejecuta y también imprime un mensaje.
    #:param funcion: Se espera una función que no recibe argumentos y no retorna valor.
"""
    print("Hola desde b")
    funcion()  # Llamamos a la función pasada como argumento

b(a)  # Pasamos la función a() como argumento a b()"""

#######################################################

from typing import Callable

# Función de suma
def suma(a: float, b: float) -> float:
    return a + b

# Función de multiplicación
def multiplicacion(a: float, b: float) -> float:
    return a * b

# Función principal que recibe otra función y sus parámetros
def operacion(a: float, b: float, funcion: Callable[[float, float], float]) -> float:
    """
    Realiza una operación matemática entre dos números utilizando
    la función proporcionada como argumento.
    
    :param a: Primer número.
    :param b: Segundo número.
    :param funcion: Función que define la operación a realizar.
    :return: Resultado de la operación.
    """
    print(f"Aplicando la operación {funcion.__name__.capitalize()} a los números {a} y {b}.")
    return funcion(a, b)

# Uso de la función `operacion` con diferentes funciones
resultado_suma = operacion(5, 3, suma)  # Llama a la función `suma`
print(f"Resultado de la suma: {resultado_suma}")

resultado_multiplicacion = operacion(5, 3, multiplicacion)  # Llama a la función `multiplicacion`
print(f"Resultado de la multiplicación: {resultado_multiplicacion}")
