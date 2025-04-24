tablero = [
    ["T", "C", "A", "R", "K", "A", "C", "T"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["t", "c", "a", "r", "k", "a", "c", "t"]
]
def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))
        
imprimir_tablero(tablero)