from src.Process import Process
from src.MemoryManagment import MemoryManagment
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
    def __init__(self, memSize: int, strat):
        self.head = Node(Process(None, memSize))
        self.tail = self.head
        self.strat = True if strat == "bf" else False

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

    def add(self, p: Process):
        new = Node(p)
        cprev = self.head
        fit = None

        for cur in self:
            if cur.isHole() and new.size() <= cur.size():
                if fit is None:
                    fit = cur
                    continue
                if not self.strat ^ bool(fit.size() > cur.size()):
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


class Variable(MemoryManagment):
    def __init__(self, memSize, strat):
        self.mem = DoublyLinkedList(memSize, strat)
