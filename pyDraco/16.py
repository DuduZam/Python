print("EJERCICIO 16\n")
# Determinar si un número es primo 

num1 = int(input("Ingrese el numero: "))
multiplos = 0
i = 1

while i <= num1:
    if(num1 % i == 0):
    	multiplos += 1    
    i += 1

if(num1 < 2):
	print(f"{num1} No es primo.")
else:
	if(multiplos > 2):
		print(f"{num1} No es primo.")
	else:
		print(f"{num1} Es primo.")