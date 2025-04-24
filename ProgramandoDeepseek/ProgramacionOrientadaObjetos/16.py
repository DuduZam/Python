import time
from typing import Callable, Any
# Decorador básico
def mi_decorador(funcion_parametro: Callable[..., Any])-> Callable[..., Any]:
    """
    Decorador que mide el tiempo de ejecución de una función y registra mensajes antes y después.
    """
    def nueva_funcion(*args: Any, **kwargs: Any) -> Any:
        inicio = time.time()
        print(f"La función {funcion_parametro.__name__.capitalize()} ha comenzado a ejecutarse.")
        resultado = funcion_parametro(*args, **kwargs)  # Ejecutamos la función original y capturamos su resultado
        fin = time.time()
        dif = fin - inicio
        print(f"La función {funcion_parametro.__name__.capitalize()} ha terminado de ejecutarse. Duración: {dif} seg.")
        return resultado  # Devolvemos el resultado de la función original
    return nueva_funcion

# Función decorada
@mi_decorador
def sumar(*args: int) -> int:
    """
    Suma todos los números pasados como argumentos.
    """
    return sum(args)

# Llamada a la función
resultado = sumar(1, 2, 3, 4, 5)  # Capturamos el resultado de la suma
print(f"El resultado de la suma es: {resultado}")
