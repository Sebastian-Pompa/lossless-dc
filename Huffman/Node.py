from __future__ import annotations
from interfaces.Comparable import Comparable

class Node(Comparable):
    def __init__(self, freq: int, char: str | None = None, left: Node | None = None, right: Node | None = None):
        self.__freq: int = freq
        self.char: str | None = char
        self.left = left
        self.right = right

    @property
    def freq(self) -> int:
        return self.__freq
    
    def __lt__(self, other: Node) -> bool:
        return self.__freq < other.freq

    def __gt__(self, other: Node) -> bool:
        return self.__freq > other.freq

    def __eq__(self, other: Node) -> bool:
        return self.freq == other.freq and self.char == other.char and self.left == other.left and self.right == other.right
    
    def __repr__(self) -> str:
        return (
            f'({self.char} : {self.__freq})\n'
            f'  Left: {repr(self.left)}\n'
            f'  Right: {repr(self.right)}'
        )
