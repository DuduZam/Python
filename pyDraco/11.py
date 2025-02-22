print("EJERCICIO 11\n")
# Determinar el mayor de 3 números enteros 

num1 = int(input("Ingrese el primer numero: "))
num2 = int(input("Ingrese el segundo numero: "))
num3 = int(input("Ingrese el tercer numero: "))

if num1 > num2:
	if num1 > num3:
		print(f"{num1} es el numero mayor.")
	else:
		print(f"{num3} es el numero mayor.")
else:
	if num2 > num3:
		print(f"{num2} es el numero mayor.")
	else:
		print(f"{num3} es el numero mayor.")