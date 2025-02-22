print("EJERCICIO 24\n")
# Comprobar si una palabra es palíndroma. 
# Se usa: palabra[::-1] para invertir la palabra y compararla con la original.

palabra = input("Ingrese la palabra: ")

if palabra.lower() == palabra[::-1].lower():
	print(f"{palabra} es una palabra palíndroma.")
else:
	print(f"{palabra} NO es una palabra palíndroma.")