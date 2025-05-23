class Heap:
    def __init__(self, items = []):
        self.items = items

    def push(self, item):
        self.items.append(item)
        i = len(self.items) - 1

        while True:
            try:
                i_parent = self.parent(i)
                i_brother = self.brother(i)
                i_min = self.min(i, i_brother) if i_brother else i

                if self.items[i_min] < self.items[i_parent]:
                    self.swap(i_parent, i_min)
                    i = i_parent
                else:
                    break
            except:
                break

    def swap(self, index_i, index_j):
        temp = self.items[index_i]
        self.items[index_i] = self.items[index_j]
        self.items[index_j] = temp

    def min(self, index_i, index_j):
        return index_i if self.items[index_i] < self.items[index_j] else index_j

    def brother(self, index):
        i_brother = index + (1 if index % 2 else -1)
        return i_brother if self.isValid(i_brother) else None

    def isValid(self, index):
        return 0 <= index < len(self.items)

    def childs(self, index):
        i_left = 2 * index + 1
        i_right = 2 * index + 2

        i_left = i_left if self.items[i_left] else None
        i_right = i_right if self.items[i_right] else None

        return (i_left, i_right)

    def pop(self):
        try:
            left, right = self.childs(0)
            greater = max(self.items[left], self.items[right])
            self.items.remove(greater)
            self.push(greater)
            return self.items.pop(0)
        except:
            return None

    def parent(self, index):
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
       return i_parent if self.isValid(i_parent) and self.isValid(index) else None
        #    try:
        #        ip = int((index - 2 + index % 2) * .5)
        #        return (ip, self.items[ip])
        #    except:
        #        return None
       

heap = Heap()

heap.push(6)
heap.push(14)
heap.push(4)
heap.push(10)
heap.push(12)
heap.push(1)
heap.push(3)

heap.pop()

print(heap.items)