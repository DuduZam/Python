while True:  # Bucle infinito
    # Menú de opciones
    opcion = input(
        "\nSEGUNDO EJERCICIO PYTHON\n"
        "QUE OPERACION DESEAS HACER:\n"
        "1. SUMAR.\n"
        "2. RESTAR.\n"        
        "3. MULTIPLICAR\n"
        "4. DIVIDIR\n"
        "5. SALIR\n"
        "Escribe: 1, 2, 3, 4 o 5. "
    )

    # Salir del programa si el usuario elige la opción 3
    if opcion == "5":
        print("¡Gracias por usar el programa! ¡Hasta luego!")
        break  # Sale del bucle while

    # SUMA
    if opcion == "1":
        # Pedir el primer valor
        num1 = input("Ingresa el primer valor: ")
        num2 = input("Ingresa el segundo valor: ")
        
        # Convertir la cadena a un objeto datetime
        try:
            num1 = float(num1)
            num2 = float(num2)            
        except ValueError:
            print("Por favor ingrese valores correctos.")
            continue  # Vuelve al inicio del bucle

        # Calcular la operacion
        resultado = num1+num2
        print(f"\nLa suma de {num1} y {num2} da como resultado: {resultado}")

    # RESTA
    elif opcion == "2":
        # Pedir el primer valor
        num1 = input("Ingresa el primer valor: ")
        num2 = input("Ingresa el segundo valor: ")
        
        # Convertir la cadena a un objeto datetime
        try:
            num1 = float(num1)
            num2 = float(num2)            
        except ValueError:
            print("Por favor ingrese valores correctos.")
            continue  # Vuelve al inicio del bucle

        # Calcular la operacion
        resultado = num1-num2
        print(f"\nLa resta de {num1} y {num2} da como resultado: {resultado}")

    # MULTIPLICACION
    elif opcion == "3":
        # Pedir el primer valor
        num1 = input("Ingresa el primer valor: ")
        num2 = input("Ingresa el segundo valor: ")
        
        # Convertir la cadena a un objeto datetime
        try:
            num1 = float(num1)
            num2 = float(num2)            
        except ValueError:
            print("Por favor ingrese valores correctos.")
            continue  # Vuelve al inicio del bucle

        # Calcular la operacion
        resultado = num1*num2
        print(f"\nLa multiplicacion de {num1} y {num2} da como resultado: {resultado}")

    # DIVISION
    elif opcion == "4":
        # Pedir el primer valor
        num1 = input("Ingresa el primer valor: ")
        num2 = input("Ingresa el segundo valor: ")
        
        # Convertir la cadena a un objeto datetime
        try:
            num1 = float(num1)
            num2 = float(num2)            
        except ValueError:
            print("Por favor ingrese valores correctos.")
            continue  # Vuelve al inicio del bucle

        # Calcular la operacion
        resultado = num1//num2
        print(f"\nLa division de {num1} y {num2} da como resultado: {resultado}")

    else:
        print("Opción no válida. Vuelve a intentarlo.")

    # Preguntar si desea ingresar otra fecha
    otra_vez = input("\n¿Deseas usar la calculadora? (s/n): ").strip().lower()
    if otra_vez != "s":
        print("¡Gracias por usar el programa! ¡Hasta luego!")
        break  # Sale del bucle while