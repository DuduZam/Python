print("EJERCICIO 6\n")
# Comparar dos números y verificar cuál es mayor y si son iguales 

num1 = int(input("Ingrese el primer numero: "))
num2 = int(input("Ingrese el segundo numero: "))

if num1 == num2:
	print(f"{num1} y {num2} son iguales.")
elif num1 > num2:
	print(f"{num1} es mayor a {num2}.")
else:
	print(f"{num2} es mayor a {num1}.")