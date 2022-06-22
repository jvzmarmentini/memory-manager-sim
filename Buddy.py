from Process import Process
from utils.Colors import bc
from utils.Exceptions import MemoryOverflowException, ProcessNotFoundException


class Tree:
    def __init__(self, memSize) -> None:
        self._tree = [None] * (memSize-1)
        self._tree[0] = memSize

    def __str__(self, k=0, level=0):
        if self._tree[k] is not None:
            if 2*k+1 < len(self._tree):
                self.__str__(2*k+1, level+1)
            print(level * 4 * ' ' + '-> ' + repr(self._tree[k]), end='')
            if isinstance(self._tree[k], Process):
                r = self._tree[0]//2 ** level-self._tree[k].size
                print(",", f"{bc.WARNING}{r}{bc.ENDC}") if r else print()
            else:
                print()
            if 2*k+2 < len(self._tree):
                self.__str__(2*k+2, level+1)
        return ""

    def _isLeaf(self, k):
        return 2*k+1 >= len(self._tree)

    def _hasChild(self, k):
        return self._tree[2*k+1] is not None

    def _g(self, k):
        return not self._isLeaf(k) and self._hasChild(k)

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

    def _remove(self, pid, k):
        if isinstance(self._tree[k], Process):
            if self._tree[k].pid == pid:
                return True
            return None

        if self._g(k):
            res = self._remove(pid, 2*k+1)
            if res is not None:
                if res:
                    if not isinstance(self._tree[2*k+2], Process) and not self._g(2*k+2):
                        self._tree[2*k+1] = self._tree[2*k+2] = None
                        return True
                    else:
                        self._tree[2*k+1] = self._tree[k] // 2
                        return False
                else:
                    return False
        else:
            return None

        if self._g(k):
            res = self._remove(pid, 2*k+2)
            if res is not None:
                if res:
                    if not isinstance(self._tree[2*k+1], Process) and not self._g(2*k+1):
                        self._tree[2*k+2] = self._tree[2*k+1] = None
                        return True
                    else:
                        self._tree[2*k+2] = self._tree[k] // 2
                        return False
                else:
                    return False
        return None

    def remove(self, pid):
        if self._remove(pid, 0) is None:
            raise ProcessNotFoundException(pid)
        return self


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

                        print(self.__in(pid, size))
                    except MemoryOverflowException as e:
                        print(e)
                else:
                    pid = line.split("OUT(", 1)[1].split(")")[0]
                    try:
                        # import pdb
                        # pdb.set_trace()
                        print(self.__out(pid))
                    except ProcessNotFoundException as e:
                        print(e)
