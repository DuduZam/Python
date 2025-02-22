print("\nEJERCICIO 1 PYTHON\n")

suma = 0

while True:
    num = int(input("Ingrese número a sumar: "))
    if num == 0:
        break
    suma += num

print(f"La respuesta es {suma}")