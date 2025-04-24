lista1 = [5, 3, 8, 6, 7, 2]
#        [2, 3, 5, 6, 7, 8]
lista2= [8, 10, 6, 2, 4]
#       [2, 4, 6, 8, 10]

def ordenamiento_burbuja(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j] :
                k = lista[i]
                lista[i] = lista[j]
                lista[j] = k
            else:
                continue
    return lista

print("Lista 1 desordenada: " , lista1)
print("Lista 1 ordenada:    " , ordenamiento_burbuja(lista1) , "\n")
print("Lista 2 desordenada: " , lista2)
print("Lista 2 ordenada:    " , ordenamiento_burbuja(lista2) , "\n")