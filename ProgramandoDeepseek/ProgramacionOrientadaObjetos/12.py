def sumar_dos_numeros(a:float, b:float)-> float:
    """Suma dos numeros y devuelve entera.
    Valores permitidos a = flotante , b = flotante"""
    resultado = int(a + b)
    return resultado

def sumar_varios_numeros(*numeros: float) -> int:
    """Suma varios números y devuelve el resultado como entero.
    Valores permitidos: flotantes."""
    resultado = int(sum(numeros))
    return resultado
    
# Ejemplo de uso
"""numero1 = 5.8
numero2 = 3.3
resultado = sumar_dos_numeros(numero1, numero2)
print(f"La suma de {numero1} y {numero2} es {resultado}")"""
numeros = input("Ingrese los numeros separados por , Ejemplo: 1,2,3:")
numeros_listados = tuple(map(float, numeros.split(",")))
resultado = sumar_varios_numeros(*numeros_listados) 
numeros_formateados = " + ".join(map(str, numeros_listados))
print(f"La suma de {numeros_formateados} es {resultado}")
#print(f"La suma de {list()} es {resultado}")