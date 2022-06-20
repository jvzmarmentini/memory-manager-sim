from Process import Process
from utils.Colors import bc


class MemoryOverflowException(Exception):
    def __init__(self):
        super().__init__(f"{bc.FAIL}!!Espaco insuficiente de memoria{bc.ENDC}")


class Node:
    def __init__(self, size) -> None:
        self.size = size
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return str(self.size)

    def split(self):
        half = self.size // 2
        self.left = Node(half)
        self.right = Node(half)

    def isLeaf(self):
        return True if self.left is None else False


class Tree:
    def __init__(self, memSize) -> None:
        self.root = Node(memSize)

    def __str__(self) -> str:
        return self._straux(0, self.root)

    def _straux(self, level, f):
        ret = "\t"*level+repr(f.size)+"\n"
        if isinstance(f.left, Node):
            ret += self._straux(level+1, f.left)
        else:
            ret += "\t"*(1+level)+str(f.left)+"\n"
        if isinstance(f.right, Node):
            ret += self._straux(level+1, f.right)
        else:
            ret += "\t"*(1+level)+str(f.right)+"\n"
        return ret

    def _add(self, p: Process, f: Node):
        half = f.size // 2
        if f.isLeaf():
            if p.size > half and p.size <= f.size:
                self.root = p
                return self


        if f.isLeaf():
            if p.size > half and p.size <= f.size:
                f = p
                return self
            if p.size <= half:
                f.split()
                return self._add(p, f.left)
        else:
            if isinstance(f.left, Node):
                res = self._add(p, f.left)
                if res is not None:
                    return res
            if isinstance(f.right, Node):
                return self._add(p, f.right)
        return None

    def add(self, p: Process):
        return self._add(p, self.root)

    def remove():
        pass


class Buddy:
    def __init__(self, memSize):
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
                        # import pdb
                        # pdb.set_trace()
                        print(self.__in(pid, size))
                    except MemoryOverflowException as e:
                        print(e)
                else:
                    pid = line.split("OUT(", 1)[1].split(")")[0]
                    try:
                        print(self.__out(pid))
                    except ValueError as e:
                        print(e)
