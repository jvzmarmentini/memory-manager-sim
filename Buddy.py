from Process import Process
from utils.Colors import bc


class MemoryOverflowException(Exception):
    def __init__(self):
        super().__init__(f"{bc.FAIL}!!Espaco insuficiente de memoria{bc.ENDC}")


class Tree:
    def __init__(self, memSize) -> None:
        self._tree = [None] * (memSize-1)
        self._tree[0] = memSize

    def __str__(self, k=0, level=0):
        if self._tree[k] is not None:
            if 2*k+1 < len(self._tree):
                self.__str__(2*k+1, level + 4)
            print(level * ' ' + '-> ' + repr(self._tree[k]))
            if 2*k+2 < len(self._tree):
                self.__str__(2*k+2, level + 4)
        return ""

    # ! test edge cases
    def _add(self, p: Process, k: int):
        if isinstance(self._tree[k], Process):
            return None

        if self._tree[k] == 2 or p.size > self._tree[k] // 2:
            if 2*k+1 >= len(self._tree) or self._tree[2*k+1] is None:
                self._tree[k] = p
                return self
            return None

        if self._tree[2*k+1] is None:
            self._tree[2*k+1] = self._tree[2*k+2] = self._tree[k] // 2

        if self._add(p, 2*k+1) is not None:
            return self
        return self._add(p, 2*k+2)

    def add(self, p: Process):
        if p.size > self._tree[0]:
            raise MemoryOverflowException
        if self._add(p, 0) is None:
            raise MemoryOverflowException
        return self

    def remove(self, pid):
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
