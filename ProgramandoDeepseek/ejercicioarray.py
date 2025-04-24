print("ejercicio 1")

#lista = [3, 3, 3, 5, 1]
#[3, 6, 9, 10]
#[3, 3, 3, 5, 1]
#[1, 3, 3, 3, 5]
def asignar_rangos(lista):
    # Ordenar la lista en orden descendente y eliminar duplicados
    orden_desc = sorted(set(lista), reverse=True)
    
    # Crear un diccionario con los valores y sus rangos
    rangos = {valor: rango + 1 for rango, valor in enumerate(orden_desc)}
    
    # Asignar rangos a la lista original
    return [rangos[num] for num in lista]

# Ejemplo de uso
mi_lista = [3, 3, 3, 1, 5, 6]
resultados = asignar_rangos(mi_lista)
print(resultados)