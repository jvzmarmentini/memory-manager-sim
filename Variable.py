from Process import Process
from utils.Colors import bc


class Node:
    def __init__(self, data: Process):
        self.size = data.size
        self.data = data
        self.next = None

    def __str__(self):
        return '*'*self.data.size if self.data.pid == None else f"{bc.GREEN}{self.data.pid*self.data.size}{'*'*(self.size-self.data.size)}{bc.ENDC}"

    def __eq__(self, other):
        return self.data.pid == other


class LinkedList:
    def __init__(self, nodes=None, memSize=9):
        self.head = Node(Process(None, memSize))
        self.tail = self.head

    def __str__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node))
            node = node.next
        return "->".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __add(self, node):
        self.head.data.size -= node.data.size
        node.next = self.head
        self.head = node

    def add(self, n):
        if self.head == self.tail:
            return self.__add(n)

        prev_node = self.head
        for node in self:
            if node == None and node.data.size >= n.data.size:
                prev_node.next = n
                n.next = node
                node.data.size -= n.size
                return
            prev_node = node

    def remove(self, n):
        for node in self:
            if node.data == n:
                node.data.pid = None
                return

    # def remove(self, n):
    #     if self.head == n:
    #         self.head = self.head.next
    #         return

    #     previous_node = self.head
    #     for node in self:
    #         if node.data == n:
    #             previous_node.next = node.next
    #             return
    #         previous_node = node

    #     raise Exception("Node with pid '%s' not found" % n)


llist = LinkedList()
print(llist)
llist.add(Node(Process("A", 3)))
print(llist)
llist.add(Node(Process("B", 3)))
print(llist)
llist.add(Node(Process("C", 1)))
print(llist)
llist.add(Node(Process("D", 2)))
print(llist)
llist.remove("A")
print(llist)
llist.add(Node(Process("E", 2)))
print(llist)


class Variable:
    def __init__(self, memSize):
        self.memSize = memSize
        # TODO: init empty linkedlist

    def __str__(self):
        return ""

    def __in(self, p: Process) -> None:
        print(f"IN: {p}")

    def __out(self, pid: int) -> None:
        print(f"OUT: {pid}")

    def run(self, path: str) -> None:
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if("IN" in line):
                    line = "".join(line.split()).split(
                        "IN(", 1)[1].split(")")[0]
                    pid, size = line.split(",")
                    self.__in(Process(pid, size))
                else:
                    pid = line.split("OUT(", 1)[1].split(")")[0]
                    self.__out(pid)
