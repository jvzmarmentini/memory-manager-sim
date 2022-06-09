from Process import Process
from utils.Colors import bc


class MemoryOverflowException(Exception):
    def __init__(self):
        super().__init__(f"{bc.FAIL}!!Espaco insuficiente de memoria{bc.ENDC}")


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

    def bestfit(self, p: Process) -> None:
        new = Node(p)
        cprev = self.head
        bestfit = None

        for cur in self:
            if cur.isHole():
                if new.data.size == cur.data.size:
                    # * prev neighour node
                    new.prev = cur.prev
                    if cur is self.head:
                        self.head = new
                    else:
                        cur.prev.next = new

                    # * next neighour node
                    new.next = cur.next
                    if cur is self.tail:
                        self.tail = new
                    else:
                        cur.next.prev = new

                    return self
                if new.data.size < cur.data.size:
                    # * init best fit
                    if bestfit is None:
                        bestfit = cur
                        continue

                    # * check if is the best fit
                    if bestfit.data.size - new.data.size > cur.data.size - new.data.size:
                        bestfit = cur
            cprev = cur

        if bestfit is None:
            raise MemoryOverflowException

        bestfit.data.size -= new.data.size
        new.prev = bestfit.prev
        new.next = bestfit
        if bestfit is self.head:
            self.head = new
        else:
            bestfit.prev.next = new
        bestfit.prev = new

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

    def remove(self, n: int) -> None:
        for node in self:
            if node.data.pid == n:
                node.data.pid = None
                return self.__merge_neighbours(node)
        raise ValueError(f"{bc.FAIL}!!PID nao encontrado{bc.ENDC}")


class Variable:
    def __init__(self, memSize):
        self.memSize = memSize
        self.mem = DoublyLinkedList(memSize)

    def __str__(self):
        return self.mem

    def __in(self, pid: int, size: int) -> None:
        p = Process(pid, size)
        print(f"IN: {p}")
        return self.mem.bestfit(p)

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
