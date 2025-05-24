from Heap.BaseHeap import BaseHeap, T

class MinHeap(BaseHeap[T]):
    def __init__(self, items: list[T] | None = None):
        super().__init__(lambda a, b: a < b, items)