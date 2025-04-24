print("""//////////////////////////////////////////////////////////////
//                                                          //   
//    Bienvenido al mundo de las listas                     //   
//    Aqui podras:                                          //
//    1. Sumar valores a una lista                          //
//    2. Ingresar un valor a una posicion de una lista      //
//    3. Mostrar Lista 1 y Lista 2                          //   
//    4. Salir                                              //   
//    """"""                                                      //
//////////////////////////////////////////////////////////////""")
option = int(input("Ingresa una opcion: "))
lista1 = []
lista2 = []
#print(lista1)
while option != 4:
    if option == 1:
        #print(lista1)
        item = int(input("Ingresa una valor a la lista: "))
        lista1.append(item)
        print(lista1)
        option = int(input("Ingresa una opcion: "))
    elif option == 2:
        #print(lista2)
        position = int(input("Ingrese la posicion: "))
        item = int(input("Ingresa el valor: "))
        lista2.insert(position,item)
        print(lista2)
        option = int(input("Ingresa una opcion: "))
    elif option == 3:
        print(lista1)
        print(lista2)
        option = int(input("Ingresa una opcion: "))
    else:
        option = int(input("Opcion invalida\nVuelva a ingresar: "))
else:
    print("Programa Finalizado.\nHasta la proxima.")    