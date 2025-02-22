print("EJERCICIO 2\n")
# Resto o módulo de una división (pedir datos al usuario)

opcion = input("Escoger:\n1. Resta\n2. Modulo de una division\n")

if opcion == "1":

	num1 = int(input("Ingrese el primer numero: "))
	num2 = int(input("Ingrese el segundo numero: "))
	print(num1-num2)

elif opcion == "2":

	num1 = int(input("Ingrese el primer numero: "))
	num2 = int(input("Ingrese el segundo numero: "))

	print(num1%num2)

else:

	print("Opcion no valida.")