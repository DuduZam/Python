import math

def area_circulo(radio):
    return math.pi * radio ** 2

def area_rectangulo(largo, ancho):
    return largo * ancho

if __name__ == "__main__":
    print("Área del círculo (radio=5):", area_circulo(5))
    print("Área del rectángulo (largo=4, ancho=6):", area_rectangulo(4, 6))