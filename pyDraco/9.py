print("EJERCICIO 9\n")
# Verificar si un año es bisiesto (Un año es bisiesto si es divisible por 4 y no por 100, a menos que 
# también sea divisible por 400

año = int(input("Ingrese el año: "))

if año % 4 == 0 and (año % 100 != 0 or año % 400 == 0):
	print(f"{año} es año bisiesto.")
else:
	print(f"{año} no es año bisiesto.")