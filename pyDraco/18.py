print("EJERCICIO 18\n")
# Verificar si un número es divisible entre 3 y 5.

num1 = int(input("Ingrese el numero: "))

if(num1 % 3 == 0):
	if(num1 % 5 == 0):
		print(f"{num1} es divisible entre 3 y 5.")
	else:
		print(f"{num1} es divisible entre 3.")
elif(num1 % 5 == 0):
	print(f"{num1} es divisible entre 5.")
else:
	print(f"{num1} NO es divisible entre 3 y 5.")