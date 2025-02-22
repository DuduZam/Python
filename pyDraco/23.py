print("EJERCICIO 23\n")
# Calcular salario con bonificación. Si el salario de un empleado es menor a 2000, tendrá un bono de 
# 20%. Si el salario es mayor a 2000, el bono es del 10%. Mostrar el salario total, incluyendo su 
# bonificación. 

salario = int(input("Ingrese el salario: "))

if salario < 2000:
	print(f"Tu salario es: {salario}$, tienes un bono del 20%.\nSalario Neto: {salario+(salario*0.2)}$.")
else:
	print(f"Tu salario es: {salario}$, tienes un bono del 10%.\nSalario Neto: {salario+(salario*0.1)}$.")