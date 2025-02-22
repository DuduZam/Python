print("EJERCICIO 20\n")
# Calculadora básica, debe pedir al usuario la operación que desea realizar (+, -, *, /).

numeros = []
print("Ingrese los números que desea calcular (ingrese 'fin' para terminar):")

while True:
    entrada = input("> ")
    if entrada.lower() == "fin":
        break
    try:
        numero = float(entrada)
        numeros.append(numero)
    except ValueError:
        print("Entrada inválida. Ingrese un número o 'fin'.")

if not numeros:
    print("No se ingresaron números.")
else:
    print("\nElija la operación:")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")

    opcion = input("Ingrese el número de la operación: ")

    resultado = numeros[0]

    if opcion == "1":
        for numero in numeros[1:]:
            resultado += numero
    elif opcion == "2":
        for numero in numeros[1:]:
            resultado -= numero
    elif opcion == "3":
        for numero in numeros[1:]:
            resultado *= numero
    elif opcion == "4":
        for numero in numeros[1:]:
            if numero == 0:
                print("Error: No se puede dividir por cero.")
                exit()
            resultado /= numero
    else:
        print("Opción inválida.")
    print("Resultado:", resultado)