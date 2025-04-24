print("""//////////////////////////////////////////////////////////////
//                                                          //   
//    Bienvenido al mundo de las Matrices                   //   
//    Aqui podras:                                          //
//    1. Crear una Matriz                                   //
//    2. Mostrar Matriz                                     //   
//    3. Salir                                              //   
//                                                          //
//////////////////////////////////////////////////////////////""")
option = int(input("Ingresa una opcion: "))
matriz = []
while option != 3:    
    if option == 1:
        filas = int(input("Ingresa num de filas: "))
        columnas = int(input("Ingresa num de columnas: "))
        matriz = []        
        for i in range(filas):
            filas = []
            for j in range(columnas):
                elemento = int(input(F"Ingresa el valor en la posicion [{i}][{j}]: "))
                filas.append(elemento)                
            matriz.append(filas)  
        option = int(input("Ingresa una opcion: "))
    elif option == 2:        
        print("Matriz Final:")
        for fila in matriz:
            print(fila)
        option = int(input("Ingresa una opcion: "))
    else:
        print("No es una opcion valida.")
        option = int(input("Ingresa una opcion: "))
else:
    print("Programa Finalizado.\nHasta la proxima.")