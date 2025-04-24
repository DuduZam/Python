from typing import Callable, Any

def decoradora(funcion_parametro: Callable[..., float]) -> Callable[..., float]:
    def nueva_funcion(*args: float, **kwargs: Any) -> float:
        # Ejecutamos la función decorada y obtenemos el resultado
        resultado: float = funcion_parametro(*args, **kwargs)
        
        # Seleccionamos el símbolo correspondiente a la operación
        if funcion_parametro.__name__ == "suma":
            simbolo = " + "
        elif funcion_parametro.__name__ == "resta":
            simbolo = " - "
        elif funcion_parametro.__name__ == "multiplicacion":
            simbolo = " x "
        elif funcion_parametro.__name__ == "division":
            simbolo = " / "
        else:
            simbolo = " ? "

        # Creamos la cadena de los argumentos para mostrar el detalle de la operación
        if args:  # Verificamos que haya argumentos
            argumentos = simbolo.join(map(str, args))
            print(f"La {funcion_parametro.__name__.capitalize()} de {argumentos} = {resultado}")
        else:
            print(f"La {funcion_parametro.__name__.capitalize()} no tiene argumentos para operar.")
        
        return resultado
    return nueva_funcion

@decoradora
def suma(*args: float) -> float:
    """Suma todos los números pasados como argumento."""    
    return sum(args)

@decoradora
def resta(*args: float) -> float:
    """
    Resta todos los valores proporcionados mediante *args.
    El primer argumento se toma como base y a él se le restan los demás.
    """
    if len(args) == 0:
        print("Error: No se proporcionaron valores.")
        return 0.0
    
    resultado = args[0]
    for valor in args[1:]:
        resultado -= valor
    return resultado

@decoradora
def multiplicacion(*args: float) -> float:
    """
    Multiplica todos los números pasados como argumento.
    """
    if len(args) == 0:
        print("Error: No se proporcionaron valores.")
        return 0.0
    
    resultado = 1.0
    for valor in args:
        resultado *= valor
    return resultado

@decoradora
def division(*args: float) -> float:
    """
    Divide los números pasados como argumento.
    El primer argumento se toma como base y a él se le dividen los demás.
    """
    if len(args) == 0:
        print("Error: No se proporcionaron valores.")
        return 0.0
    
    resultado = args[0]
    for valor in args[1:]:
        if valor == 0:
            print("Error: División por cero.")
            return 0.0
        resultado /= valor
    return resultado
    """
    Divide los números pasados como argumento.
    El primer argumento se toma como base y a él se le dividen los demás.
    """
    if len(args) == 0:
        print("Error: No se proporcionaron valores.")
        return 0
    
    resultado = args[0]
    for valor in args[1:]:
        if valor == 0:
            print("Error: División por cero.")
            return 0
        resultado /= valor
    return resultado

# Ejemplos de uso:
suma(10, 5, 3)         # La Suma de 10 + 5 + 3 = 18
resta(10, 5, 2)        # La Resta de 10 - 5 - 2 = 3
multiplicacion(3, 5, 2) # La Multiplicacion de 3 x 5 x 2 = 30
division(100, 5, 2)    # La Division de 100 / 5 / 2 = 10.0
division(100, 0)       # Error: División por cero.
