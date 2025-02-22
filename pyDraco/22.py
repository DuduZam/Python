print("EJERCICIO 22\n")
# Clasificación de notas. Si la nota es mayor a 90, es excelente. También mostrar si aprobó o 
# reprobó.

nota = int(input("Ingrese la nota: "))

if nota > 50:
	if(nota > 90):
		print(f"Tu nota es: {nota}\nFELICIDADES ES UNA NOTA EXCELENTE!.\nAPROBASTE.")
	else:
		print(f"Tu nota es: {nota}.\nAPROBASTE.")
else:
	print(f"Tu nota es: {nota}.\nREPROBASTE.")