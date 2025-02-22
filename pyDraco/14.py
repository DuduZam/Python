print("EJERCICIO 14\n")
# Determinar si un número es múltiplo de otro.

num1 = int(input("Ingrese el numero: "))
num2 = int(input("Ingrese su divisor: "))

if num1 % num2 ==0:	
	print(f"{num1} es multiplo de: {num2}.")
else:
	print(f"{num1} no es multiplo de: {num2}.")