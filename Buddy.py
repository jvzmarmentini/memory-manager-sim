from typing import Self
from Process import Process
from utils.Colors import bc


class MemoryOverflowException(Exception):
    def __init__(self):
        super().__init__(f"{bc.FAIL}!!Espaco insuficiente de memoria{bc.ENDC}")


class Node:
    def __init__(self, size) -> None:
        self.flag = -1
        self.size = size
        self.left = None
        self.right = None


class Tree:
    def __init__(self, memSize) -> None:
        self.root = Node(memSize)

    def add(self, p: Process, f: Node = None) -> Self:
        if f is None:
            f = self.root

        if f.flag > 0:
            return None

        if f.flag == 0:
            if self.add(p, f.left) is not None:
                return
            if self.add(p, f.right) is not None:
                return

        half = f.size // 2
        if half // 2 > p.size:
            f.left = Node(half)
            f.left = Node(half)
            f.flag = 0
            self.add(p, f.left)
        else:
            f = p
        # ! TODO change flags
        return self

    def remove() -> Self:
        pass


class Buddy:
    def __init__(self, memSize, fit):
        self.memSize = memSize
        self.mem = Tree(memSize)

    def __str__(self):
        return self.mem

    def __in(self, pid: int, size: int) -> None:
        p = Process(pid, size)
        print(f"IN: {p}")
        return self.mem.add(p)

    def __out(self, pid: int) -> None:
        print(f"OUT: {pid}")
        return self.mem.remove(pid)

    def run(self, path: str) -> None:
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if("IN" in line):
                    pid, size = line.split("IN(", 1)[1].split(")")[
                        0].split(",")
                    try:
                        print(self.__in(pid, size))
                    except MemoryOverflowException as e:
                        print(e)
                else:
                    pid = line.split("OUT(", 1)[1].split(")")[0]
                    try:
                        print(self.__out(pid))
                    except ValueError as e:
                        print(e)
