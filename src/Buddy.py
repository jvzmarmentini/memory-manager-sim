from src.Process import Process
from src.MemoryManagment import MemoryManagment
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
                print(",", f"{r}") if r else print()
            else:
                print()
            if 2*k+2 < len(self._tree):
                self.__str__(2*k+2, level+1)
        return ""

    def _hasChild(self, k):
        return self._tree[2*k+1] is not None

    def _isFit(self, k):
        return 2*k+1 >= len(self._tree) or not self._hasChild(k)

    def _add(self, p: Process, k: int):
        cur = self._tree[k]
        leftIdx = 2*k+1
        rightIdx = leftIdx+1

        if isinstance(cur, Process):
            return None

        if cur == 2 or p.size > cur // 2:
            if self._isFit(k):
                self._tree[k] = p
                return self
            return None

        if not self._hasChild(k):
            self._tree[leftIdx] = self._tree[rightIdx] = cur // 2

        if self._add(p, leftIdx) is not None:
            return self
        return self._add(p, rightIdx)

    def add(self, p: Process):
        if p.size > self._tree[0]:
            raise MemoryOverflowException
        if self._add(p, 0) is None:
            raise MemoryOverflowException
        return self

    def _remove(self, pid, k):
        cur = self._tree[k]
        leftIdx = 2*k+1
        rightIdx = leftIdx+1

        if isinstance(cur, Process):
            if cur.pid == pid:
                return True
            return None

        if not self._isFit(k):
            res = self._remove(pid, leftIdx)
            if res is not None:
                if res:
                    if not isinstance(self._tree[rightIdx], Process) and self._isFit(rightIdx):
                        self._tree[leftIdx] = self._tree[rightIdx] = None
                        return True
                    self._tree[leftIdx] = cur // 2
                return False
        else:
            return None

        if not self._isFit(k):
            res = self._remove(pid, rightIdx)
            if res is not None:
                if res:
                    if not isinstance(self._tree[leftIdx], Process) and self._isFit(2*k+1):
                        self._tree[rightIdx] = self._tree[leftIdx] = None
                        return True
                    self._tree[rightIdx] = cur // 2
                return False
        return None

    def remove(self, pid):
        if self._remove(pid, 0) is None:
            raise ProcessNotFoundException(pid)
        return self


class Buddy(MemoryManagment):
    def __init__(self, memSize):
        self.mem = Tree(memSize)
