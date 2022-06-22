from src.Process import Process
from utils.Colors import bc
from utils.Exceptions import MemoryOverflowException, ProcessNotFoundException


class Node:
    def __init__(self, data: Process):
        self.data = data
        self.next = None
        self.prev = None

    def __str__(self) -> str:
        return str(self.data.size) if self.data.pid == None else f"{bc.GREEN}{self.data.pid*self.data.size}{bc.ENDC}"

    def __eq__(self, other: int) -> bool:
        return self.data.pid == other

    def isHole(self) -> bool:
        return self.data.pid is None

    def size(self) -> int:
        return self.data.size


class DoublyLinkedList:
    def __init__(self, memSize: int):
        self.head = Node(Process(None, memSize))
        self.tail = self.head

    def __str__(self) -> str:
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node))
            node = node.next
        return "<->".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def fit(self, p: Process, b: bool):
        new = Node(p)
        cprev = self.head
        fit = None

        for cur in self:
            if cur.isHole() and new.size() <= cur.size():
                if fit is None:
                    fit = cur
                    continue
                if b:
                    if not b ^ bool(fit.size() > cur.size()):
                        fit = cur
            cprev = cur

        if fit is None:
            raise MemoryOverflowException

        if fit is self.head:
            self.head = new
        else:
            fit.prev.next = new
        new.prev = fit.prev

        if new.data.size == fit.data.size:
            if fit is self.tail:
                self.tail = new
            else:
                fit.next.prev = new
            new.next = fit.next
            # ? del fit
            return self

        fit.data.size -= new.data.size
        new.next = fit
        fit.prev = new

        return self

    def firsfit(self, p: Process) -> None:
        new = Node(p)
        cprev = self.head

        for cur in self:
            if cur.isHole():
                if new.data.size < cur.data.size:
                    cur.data.size -= new.data.size
                    new.prev = cur.prev
                    new.next = cur
                    cur.prev = new
                    if cur is self.head:
                        self.head = new
                    else:
                        cprev.next = new
                    return self
                elif new.data.size == cur.data.size:
                    new.next = cur.next
                    new.prev = cur.prev
                    if cur is self.tail:
                        self.tail = new
                    else:
                        cur.next.prev = new
                    if cur is self.head:
                        self.head = new
                    else:
                        cprev.next = new
                    return self
            cprev = cur

        raise MemoryOverflowException

    def __merge_neighbours(self, node: Node):
        while True:
            nprev = node.prev
            nnext = node.next
            if node is not self.head and nprev.isHole():
                if(node is not self.tail):
                    nprev.next = nnext
                    nnext.prev = nprev
                else:
                    self.tail = nprev
                    nprev.next = None
                nprev.data.size += node.data.size
                node = nprev
                continue
            if node is not self.tail and nnext.isHole():
                if(node is not self.head):
                    nprev.next = nnext
                    nnext.prev = nprev
                else:
                    self.head = nnext
                    nnext.prev = None
                nnext.data.size += node.data.size
                node = nnext
                continue
            return self

    def remove(self, pid: int) -> None:
        for node in self:
            if node.data.pid == pid:
                node.data.pid = None
                return self.__merge_neighbours(node)
        raise ProcessNotFoundException(pid)


class Variable:
    def __init__(self, memSize, fit):
        self.memSize = memSize
        self.fit = fit
        self.mem = DoublyLinkedList(memSize)

    def __str__(self):
        return self.mem

    def __in(self, pid: int, size: int) -> None:
        b = True if self.fit == "bf" else False
        p = Process(pid, size)
        print(f"IN: {p}")
        return self.mem.fit(p, b)

    def __out(self, pid: int) -> None:
        print(f"OUT: {pid}")
        return self.mem.remove(pid)

    def run(self, path: str) -> None:
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if("IN(" in line):
                    pid, size = line.split("IN(", 1)[1].split(")")[
                        0].split(",")
                    try:
                        print(self.__in(pid, size))
                    except MemoryOverflowException as e:
                        print(e)
                elif("OUT(" in line):
                    pid = line.split("OUT(", 1)[1].split(")")[0]
                    try:
                        print(self.__out(pid))
                    except ProcessNotFoundException as e:
                        print(e)
                else:
                    continue
