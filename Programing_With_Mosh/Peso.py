while True:  # Bucle infinito
    # Menú de opciones
    print("\nTERCER EJERCICIO PYTHON")
    peso = float(input("INGRESA TU PESO: "))

    uni_masa = input("(K)g o (L)bs ").strip().lower()

    # KILO
    if uni_masa == "k":
        # Pedir el primer valor
        resultado = peso * 2.20462
        
        print(f"\nEl peso es: {resultado} libras.")

    # LIBRAS
    elif uni_masa == "l":
        # Pedir el primer valor
        resultado = peso * 0.453592
        
        print(f"\nEl peso es: {resultado} kilos.")

    else:
        print("Opción no válida. Vuelve a intentarlo.")

    # Preguntar si desea ingresar otra fecha
    otra_vez = input("\n¿Deseas saber tu peso en otra unidad de masa? (s/n): ").strip().lower()
    if otra_vez != "s":
        print("¡Gracias por usar el programa! ¡Hasta luego!")
        break  # Sale del bucle while