print("EJERCICIO 15\n")
# Calcular el IMC (índice de Masa Corporal).

peso = float(input("Ingrese el peso: "))
altura = float(input("Ingrese la altura: "))
imc = peso / (altura**2)

print(f"El IMC [Indice de Masa Corporal] es: {round(imc,2)}.\n\nVALORES:\nBajo peso: Menos de 18.5\nPeso normal: 18.5 - 24.9\nSobrepeso: 25.0 - 29.9\nObesidad: 30.0 o más")	