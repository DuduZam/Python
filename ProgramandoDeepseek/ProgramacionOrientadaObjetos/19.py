import time
from typing import Callable, Any

class numero:
    def __init__(self, lista: list[int]):
        """
        Inicializa una instancia de la clase con una lista de números enteros.

        Args:
            lista (list[int]): Lista de números enteros que se asignará al atributo `lista_num`.
        """
        self.lista_num = lista

    def mostrar_lista(self):
        """
        Muestra el contenido del atributo `lista_num`.

        Este método imprime la lista almacenada en el atributo `lista_num`
        en la consola.

        Retorna:
            None
        """
        print(self.lista_num)
    
    @staticmethod
    def decorador(funcion: Callable[..., Any]) -> Callable[..., Any]:  # Corrige el tipo del parámetro        
        """
        Un decorador que mide el tiempo de ejecución de una función y lo imprime en la consola.

        Args:
            funcion (Callable[..., Any]): La función que será decorada.

        Returns:
            Callable[..., Any]: La función decorada que incluye la medición del tiempo de ejecución.

        La función decorada imprimirá el nombre de la función original y el tiempo que tomó ejecutarse
        en segundos.
        """
        def funcion_decorada(self: Any, *args: Any, **kwargs: Any):
            """Función decoradora que mide el tiempo de ejecución de una función.
            Args:
                self (Any): Referencia al objeto actual.
                *args (Any): Argumentos posicionales que se pasan a la función decorada.
                **kwargs (Any): Argumentos con nombre que se pasan a la función decorada.
            Returns:
                Callable: La función decorada con la funcionalidad adicional de medir el tiempo de ejecución."""            
            inicio = time.time()
            funcion(self, *args, **kwargs)
            fin = time.time()
            print(f"Funcion: {funcion.__name__.capitalize()}. Tiempo de ejecucion: {fin - inicio} segundos")
        return funcion_decorada
    
    @decorador
    def remover(self, numero: int):
        """
        Elimina un número especificado de la lista si existe.

        Argumentos:
            numero (int): El número que se desea eliminar de la lista.

        Excepciones:
            Imprime un mensaje si el número no se encuentra en la lista.
        """
        if numero in self.lista_num:
            self.lista_num.remove(numero)
        else:
            print(f"El numero {numero} no se encuentra en la lista")
    
    @decorador
    def poper(self, indice: int):
        """
        Elimina un elemento de la lista en el índice especificado.
            indice (int): El índice del elemento a eliminar.
        Excepciones:
            ValueError: Si el índice proporcionado está fuera de rango, se imprime un mensaje indicando el índice no válido.
        Notas:
            Si el índice es válido, se elimina el elemento en el índice especificado de la lista `self.lista_num`.
            Si el índice es inválido (mayor o igual a la longitud de la lista), se imprime un mensaje en su lugar.        
        """
        if indice < len(self.lista_num):
            self.lista_num.pop(indice)
        else:
            print(f"El indice {indice} no es valido")


listita = numero([1, 2, 3, 2, 3])
listita.mostrar_lista()

listita.remover(3) # Elimina la primera ocurrencia del valor 3
listita.mostrar_lista()
listita.poper(3) # Elimina el elemento en la posicion 3 (cuarta posicion)

listita.mostrar_lista() # [1, 2, 2]