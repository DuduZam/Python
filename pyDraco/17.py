print("EJERCICIO 17\n")
# Clasificación de edades. Si es menor a 12, eres un niño. Si eres menor a 18, eres un adolescente. 
# Si eres menor a 60, eres adulto. Caso contrario eres adulto mayor. 

edad = int(input("Ingrese la edad: "))

if(edad in range(0,13)):
	print(f"Tienes {edad} años, eres un niño. \U0001F476\U0001F3FC \U0001F466\U0001F3FC")
elif(edad in range(13,19)):
	print(f"Tienes {edad} años, eres adolescente. \U0001F466\U0001F3FC \U0001F467\U0001F3FC")
elif(edad in range(19,61)):
	print(f"Tienes {edad} años, eres adulto. \U0001F468\U0001F3FC \U0001F469\U0001F3FC")
else:
	print(f"Tienes {edad} años, eres adulto mayor. \U0001F474\U0001F3FC \U0001F475\U0001F3FC")