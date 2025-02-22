def es_par(num):
    return num%2==0

def calcular_area_rectangulo(base,altura):
    return base * altura    

def imprimir_lista(lista):
    for elemento in lista:
        print(elemento)

while True:  # Bucle infinito
    # Menú de opciones
    opcion = input(
        "\nSEGUNDO EJERCICIO PYTHON DEEPSEEK\n"
        "QUE OPERACION DESEAS HACER:\n"
        "1. VERIFICAR PAR.\n"
        "2. CALCULAR EL AREA DE UN RECTANGULO.\n"        
        "3. IMPRIMIR LISTA\n"        
        "4. SALIR\n"
        "Escribe: 1, 2, 3 o 4. "
    )

    # Salir del programa si el usuario elige la opción 3
    if opcion == "4":
        print("¡Gracias por usar el programa! ¡Hasta luego!")
        break  # Sale del bucle while

    # FUNCION ES_PAR
    if opcion == "1":
        numero = int(input("Ingrese un numero entero: "))
        print(es_par(numero))

    # AREA DEL RECTANGULO
    elif opcion == "2":
        b = float(input("Ingrese la base del rectangulo: "))
        a = float(input("Ingrese la altura del rectangulo: "))
        area = calcular_area_rectangulo(b,a)
        print(f"\nEl area del rectangulo es: {area}")

    # RECIBIR LISTA
    elif opcion == "3":
        el_lista = input("Ingresa una lista de elementos separados por comas: ")

        # Convertir la entrada en una lista
        lista_usuario = el_lista.split(",")

        # Llamar a la función para imprimir la lista
        imprimir_lista(lista_usuario)

    else:
        print("Opción no válida. Vuelve a intentarlo.")

    # Preguntar si desea ingresar otra fecha
    otra_vez = input("\n¿Deseas hacer otra operacion? (s/n): ").strip().lower()
    if otra_vez != "s":
        print("¡Gracias por usar el programa! ¡Hasta luego!")
        break  # Sale del bucle while