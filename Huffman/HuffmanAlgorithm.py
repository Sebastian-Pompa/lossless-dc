from Huffman.Node import Node
from Heap.MinHeap import MinHeap
from collections import Counter

class HuffmanAlgorithm:
    """
    Implementación del algoritmo de codificación y decodificación de Huffman.

    Esta clase implementa el algoritmo de Huffman para la compresión de datos sin pérdida, 
    permitiendo tanto la codificación como la decodificación de un mensaje utilizando un árbol de Huffman.

    Atributos:
        __freqs (dict): Diccionario de frecuencias de los caracteres del contenido.
        __root (Node): Nodo raíz del árbol de Huffman construido a partir de las frecuencias.
        __codes (dict): Diccionario con los códigos binarios de cada carácter.
        __codedContent (str): Contenido original codificado como una secuencia de bits.

    Métodos:
        __init__: Inicializa la instancia, calculando frecuencias, construyendo el árbol de Huffman, generando los códigos binarios y codificando el contenido.
        decode: Decodifica un mensaje utilizando los códigos binarios.
    
    Parámetros de __init__:
        content (str): El contenido que se desea codificar.
    """

    def __init__(self, content: str):
        """
        Inicializa una nueva instancia de la clase HuffmanAlgorithm para codificar el contenido dado.

        El constructor realiza los siguientes pasos:
            1. Calcula las frecuencias de los caracteres en el contenido.
            2. Construye el árbol de Huffman, utilizando las frecuencias, y se obtiene el nodo raiz.
            3. Genera los códigos binarios para cada carácter en el árbol.
            4. Codifica el contenido original utilizando los códigos generados.

        Parámetros:
            content (str): El contenido que se desea codificar.
        """
        # 1
        self.__freqs: dict[str, int] = dict(Counter(content))

        # 2
        self.__root: Node = self.__buildTree(self.__freqs)

        # 3
        self.__codes: dict[str, str] = dict()
        self.__calculateCodes(self.__root, "")

        # 4
        self.__codedContent: str = "".join(self.__codes[ch] for ch in content)

    @property
    def freqs(self) -> dict[str, int]:
        return self.__freqs
    
    @property
    def root(self) -> Node:
        return self.__root

    @property
    def codes(self) -> dict[str, str]:
        return self.__codes

    @property
    def codedContent(self) -> str:
        return self.__codedContent

    def __buildTree(self, frequencyData: dict[str, int]) -> Node:
        """
        Construye el árbol de Huffman a partir de un diccionario de frecuencias.

        El árbol de Huffman se construye utilizando una cola de prioridad (min-heap) para combinar los 
        nodos con menor frecuencia hasta que quede solo un nodo raíz que representa el árbol completo.

        Parámetros:
            frequencyData (dict[str, int]): Un diccionario con los caracteres y sus respectivas frecuencias.

        Retorna:
            Node: Nodo raíz del árbol de Huffman.
        """
        minHeap = MinHeap[Node]([ Node(f, c) for c, f in frequencyData.items() ])

        while len(minHeap) > 1:
            l: Node = minHeap.pop()
            r: Node = minHeap.pop()
            n = Node(l.freq + r.freq, left=l, right=r)
            minHeap.push(n)

        return minHeap.pop()
   
    def __calculateCodes(self, node: Node | None, code: str):
        """
        Calcula los códigos binarios de Huffman recursivamente.

        Este método recorre el árbol de Huffman y genera un código binario único para cada símbolo.
        Los códigos se almacenan en el diccionario `__codes`.

        Parámetros:
            node (Node | None): El nodo actual en el árbol de Huffman.
            code (str): El código binario actual que se construye recursivamente.
        """
        if node is None:
            return
        
        if node.char is not None:
            self.__codes[node.char] = code

        self.__calculateCodes(node.left, code + "0")
        self.__calculateCodes(node.right, code + "1")

    @staticmethod
    def decode(content: str, codes: dict[str, str]) -> str:
        """
        Decodifica un mensaje codificado utilizando los códigos binarios dados.

        El proceso recorre el mensaje codificado bit por bit y reconstruye los caracteres
        originales utilizando el diccionario de códigos binarios.

        Parámetros:
            content (str): El contenido codificado como una secuencia de bits.
            codes (dict[str, str]): Un diccionario que mapea los caracteres a sus códigos binarios.

        Retorna:
            str: El mensaje decodificado.
        """
        currentCode = ""
        decodedContent = []
        reversedCodes = { code: ch for ch, code in codes.items() }
        
        for bit in content:
            currentCode += bit
            if currentCode in reversedCodes:
                decodedContent.append(reversedCodes[currentCode])
                currentCode = ""
        
        return "".join(decodedContent)