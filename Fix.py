from Process import Process
from utils.Colors import bc


class MemoryOverflowException(Exception):
    def __init__(self):
        super().__init__(
            f"{bc.FAIL}!!Espaco insuficiente de memoria{bc.ENDC}\n")


class ProcessNotFoundException(Exception):
    def __init__(self, pid):
        super().__init__(f"{bc.FAIL}!!PID {pid} nao encontrado{bc.ENDC}\n")


class List:
    def __init__(self, memSize, part: int) -> None:
        self.part = part
        self.mem = [None] * (memSize // part)
        self.infrag = []

    def __str__(self) -> str:
        ret = "|{0}|\n".format('|'.join(["*" * self.part if p is None
                                         else f"{bc.GREEN}{p.pid*p.size}{bc.ENDC}{'*'*(self.part-p.size)}"
                                         for p in self.mem]))
        ret += f"Internal fragmentation: {self.infrag}\n" if self.infrag else ""
        return ret

    def add(self, p: Process):
        if(p.size > self.part or None not in self.mem):
            raise MemoryOverflowException
        for i, e in enumerate(self.mem):
            if(e == None):
                self.mem[i] = p
                if p.size != self.part:
                    self.infrag.append((p.pid, self.part-p.size))
                return self

    def remove(self, pid):
        for t, p in enumerate(self.mem):
            if(p == pid):
                self.mem[t] = None
                self.infrag = list(filter(lambda t: t[0] != pid, self.infrag))
                return self
        raise ProcessNotFoundException(pid)


class Fix:
    def __init__(self, memSize, part):
        self.mem = List(memSize, part)

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
                    except ProcessNotFoundException as e:
                        print(e)
