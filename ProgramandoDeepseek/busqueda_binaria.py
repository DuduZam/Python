array = [2, 5, 7, 8, 11, 12]
#hallar el indice del numero que le pidas
#objetivo: 5                    #objetivo: 11
#output: 1                      #output: 4
print(array)

def busquerda_binaria(lista):
    objetivo = int(input("Ingresa el Objetivo: "))
    izquierda = 0
    derecha = len(lista) - 1 # Corregido
    medio = (izquierda + derecha) // 2
    while izquierda <= derecha and lista[medio] != objetivo: # Corregido
        medio = (izquierda + derecha) // 2
        if lista[medio] > objetivo:
            derecha = medio - 1
        elif lista[medio] < objetivo:
            izquierda = medio + 1
    if izquierda > derecha: # Corregido
      print("el numero no se encuentra en la lista")
    else:
        print(medio)

busquerda_binaria(array)