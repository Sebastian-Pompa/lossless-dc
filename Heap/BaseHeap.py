from typing import TypeVar, Callable, Generic
from interfaces.Comparable import Comparable

T = TypeVar('T', bound = Comparable)
class BaseHeap(Generic[T]):
    """
    Clase base para un heap binario para gestionar una cola de prioridad.

    Los elementos se almacenan y mantienen en orden prioritario, desde la raiz, en base al criterio de comparacion `compare`.
    Soporta inserción y extracción eficiente de elementos manteniendo la propiedad del heap.

    Propiedades:
    - `items` : Elementos del heap.
    - `compare` : Funcion que establece el criterio de comparacion entre dos elementos `T` para definir la prioridad del heap.

    Métodos principales:
    - `push(item: T)` : Inserta un elemento en el heap.
    - `pop()` : Extrae y retorna el elemento con mayor prioridad.

    Nota:
    - `T` : `Comparable`
    """
    def __init__(self, compare: Callable[[T, T], bool], items: list[T] | None = None):
        self._items = items or []
        self._compare = compare

    def __len__(self) -> int:
        return len(self._items)

    def push(self, item: T):
        """
        Inserta un elemento.

        Args:
            item: Elemento a insertar.

        Returns:
            None
        """
        self._items.append(item)
        i = len(self._items) - 1

        while True:
            try:
                i_parent = self.__parent(i)
                i_brother = self.__brother(i)
                i_compared = self.__compareByIndex(i, i_brother) if i_brother else i

                if self._compare(self._items[i_compared], self._items[i_parent]):
                    self.__swap(i_parent, i_compared)
                    i = i_parent
                else:
                    break
            except:
                break

    def pop(self) -> T:
        """
        Extrae y devuelve el elemento con la mayor prioridad del heap.

        Returns:
            El elemento con mayor prioridad.

        Raises:
            IndexError: Si el heap está vacío.
        """
        try:
            left, right = self.__childs(0)

            if left and right:
                # Se adiciona nuevamente quien no cumpla el criterio de comparacion.
                #   Si `left` no cumple con `right` se obtiene `left`, caso contrario `right`.
                e = self._items[left] if not self._compare(self._items[left], self._items[right]) else self._items[right]
                self._items.remove(e)
                self.push(e)

            return self._items.pop(0)
        except:
            raise IndexError("pop from an empty heap")

    def __compareByIndex(self, index_i: int, index_j: int) -> int:
        """
        Compara, mediante sus indices, dos nodos y retorna el indice del nodo que cumpla el criterio de comparacion `compare`.
        """
        return index_i if self._compare(self._items[index_i], self._items[index_j]) else index_j

    def __swap(self, index_i: int, index_j: int):
        """
        Intercambia dos nodos mediante sus indices.
        """
        temp = self._items[index_i]
        self._items[index_i] = self._items[index_j]
        self._items[index_j] = temp

    def __brother(self, index: int) -> int | None:
        """
        Calcula y retorna el indice del nodo 'hermano' de un nodo mediante su indice o `None` si no tiene.
        """
        i_brother = index + (1 if index % 2 else -1)
        return i_brother if self.__validIndex(i_brother) else None

    def __validIndex(self, index: int) -> bool:
        """
        Retorna `true` si un indice se encuentra dentro de los limites del heap, caso contrario `false`.
        """
        return 0 <= index < len(self._items)

    def __childs(self, index: int) -> tuple[int, int]:
        """
        Calcula y retorna los nodos 'hijos' de un nodo mediante su indice.

        El calculo hace uso de las siguientes formulas para los nodos `left` y `right`
            2i + 1 ; 2i + 2
        , respectivamente.
        Donde:
            `i` : indice del nodo 'padre'
        """
        i_left = 2 * index + 1
        i_right = 2 * index + 2

        i_left = i_left if self.__validIndex(i_left) else None
        i_right = i_right if self.__validIndex(i_right) else None

        return (i_left, i_right)

    def __parent(self, index):
       """
       Calculo del indice del nodo padre en base a la posicion del nodo hijo, left or right.
        Para este `Heap` la formula del indice para un nodo hijo izquierdo y derecho es:
            2i + 1 ; 2i + 2
        , respectivamente.
        Donde:
            `i` : indice del nodo padre
        
        Teniendo en cuenta lo siguiente:
            - `2i` es siempre un numero par, siendo `i` cualquier numero entero.
            Con P: numero entero par; I: numero entero impar
                - P + P = P
                - P + I = I
        Concluimos que el indice de un nodo hijo izquierdo y derecho es impar, y par, respectivamente:
            left(impar) | right(par)
            2i + 1      | 2i + 2

        Ahora, para poder calcular el indice del nodo padre he visto dos formas: mediante condicionales o mediante una ecuacion matematica.
        Se opto por la ultima opcion.
        Para hallar la ecuacion simplemente se simplifica las formulas de los indices de los nodos hijos de tal forma para poder ayudarnos del `mod 2`:
            restando 2: 
            left(impar)   | right(par)
            2i - 1        | 2i

            Dado que `a mod 2` siempre retorna `0` cuando `a` es par y `1` cuando es impar. Entonces, el indice del nodo padre es:
            `i = (index - 2 + index % 2) * 1/2`

            Donde:
                `index` : indice del nodo hijo.
       """ 
       i_parent = int((index - 2 + (index % 2)) * .5)
       return i_parent if self.__validIndex(i_parent) and self.__validIndex(index) else None