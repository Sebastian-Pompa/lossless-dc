from Heap.BaseHeap import BaseHeap, T

class MinHeap(BaseHeap[T]):
    def __init__(self):
        super().__init__(compare = lambda a, b: a < b)