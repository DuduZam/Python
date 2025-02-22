from datetime import datetime
from dateutil.relativedelta import relativedelta

while True:  # Bucle infinito
    # Menú de opciones
    opcion = input(
        "\nPRIMER EJERCICIO PYTHON\n"
        "Digita una opción:\n"
        "1. Cuánto tiempo has vivido (versión Eduardo).\n"
        "2. Cuánto tiempo has vivido (versión Librería Exacta).\n"
        "3. Salir.\n"
        "Escribe: 1, 2 o 3. "
    )

    # Salir del programa si el usuario elige la opción 3
    if opcion == "3":
        print("¡Gracias por usar el programa! ¡Hasta luego!")
        break  # Sale del bucle while

    # Obtener la fecha actual
    fecha_actual = datetime.now().date()

    if opcion == "1":
        # Pedir la fecha de nacimiento
        fecha_nacimiento_str = input("Ingresa tu fecha de nacimiento en este formato: AAAA-MM-DD: ")
        
        # Convertir la cadena a un objeto datetime
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except ValueError:
            print("Formato de fecha incorrecto. Usa AAAA-MM-DD.")
            continue  # Vuelve al inicio del bucle

        # Calcular la diferencia
        diferencia = fecha_actual - fecha_nacimiento
        años = diferencia.days // 365
        meses = (diferencia.days % 365) // 30
        dias = (diferencia.days % 365) % 30

        # Mostrar el resultado
        print(f"\nNaciste el {fecha_nacimiento}. Por lo tanto:")
        print(f"Has vivido {años} años, {meses} meses y {dias} días.")

    elif opcion == "2":
        # Versión Librería Exacta (usando dateutil.relativedelta para mayor precisión)
        # Pedir la fecha de nacimiento
        fecha_nacimiento_str = input("Ingresa tu fecha de nacimiento en este formato: AAAA-MM-DD: ")
        
        # Convertir la cadena a un objeto datetime
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except ValueError:
            print("Formato de fecha incorrecto. Usa AAAA-MM-DD.")
            continue  # Vuelve al inicio del bucle

        # Calcular la diferencia exacta
        diferencia = relativedelta(fecha_actual, fecha_nacimiento)
        print(f"\nNaciste el {fecha_nacimiento}. Por lo tanto:")
        print(f"Has vivido {diferencia.years} años, {diferencia.months} meses y {diferencia.days} días.")

    else:
        print("Opción no válida. Vuelve a intentarlo.")

    # Preguntar si desea ingresar otra fecha
    otra_vez = input("\n¿Deseas ingresar otra fecha? (s/n): ").strip().lower()
    if otra_vez != "s":
        print("¡Gracias por usar el programa! ¡Hasta luego!")
        break  # Sale del bucle while