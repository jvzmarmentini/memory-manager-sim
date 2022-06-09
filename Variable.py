from Process import Process
from utils.Colors import bc


class Node:
    def __init__(self, data: Process):
        self.data = data
        self.next = None
        self.prev = None

    def __str__(self) -> str:
        return str(self.data.size) if self.data.pid == None else f"{bc.GREEN}{self.data.pid*self.data.size}{bc.ENDC}"

    def __eq__(self, other: int) -> bool:
        return self.data.pid == other

    def isNone(self) -> bool:
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
        return "<=>".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def add(self, p: Process) -> None:
        new = Node(p)
        prev = self.head

        for cur in self:
            if cur.data.pid is None:
                if new.data.size < cur.data.size:
                    cur.data.size -= new.data.size
                    new.prev = cur.prev
                    new.next = cur
                    cur.prev = new
                    if cur is self.head:
                        self.head = new
                    else:
                        prev.next = new
                    return print(self)
                elif new.data.size == cur.data.size:
                    new.next = cur.next
                    new.prev = cur.prev
                    cur.next.prev = new
                    if cur is self.head:
                        self.head = new
                    else:
                        prev.next = new
                    return print(self)
            prev = cur

        return print(f"{bc.FAIL}!!Espaco insuficiente de memoria{bc.ENDC}")

    def remove(self, n: int) -> None:
        for node in self:
            if node.data.pid == n:
                node.data.pid = None
                while True:
                    if node is not self.head and node.prev.isNone():
                        if(node is not self.tail):
                            node.prev.next = node.next
                            node.next.prev = node.prev
                        else:
                            self.tail = node.prev
                            node.prev.next = None
                        node.prev.data.size += node.data.size
                        node = node.prev
                        continue
                    if node is not self.tail and node.next.isNone():
                        if(node is not self.head):
                            node.prev.next = node.next
                            node.next.prev = node.prev
                        else:
                            self.head = node.next
                            node.next.prev = None
                        node.next.data.size += node.data.size
                        node = node.next
                        continue
                    break
                return print(self)


class Variable:
    def __init__(self, memSize):
        self.memSize = memSize
        self.mem = DoublyLinkedList(memSize)

    def __str__(self):
        return self.mem

    def __in(self, p: Process) -> None:
        print(f"IN: {p}")
        self.mem.add(p)

    def __out(self, pid: int) -> None:
        print(f"OUT: {pid}")
        self.mem.remove(pid)

    def run(self, path: str) -> None:
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if("IN" in line):
                    pid, size = line.split("IN(", 1)[1].split(")")[
                        0].split(",")
                    self.__in(Process(pid, size))
                else:
                    self.__out(line.split("OUT(", 1)[1].split(")")[0])
