from src.Process import Process
from src.MemoryManagment import MemoryManagment
from utils.Colors import bc
from utils.Exceptions import MemoryOverflowException, ProcessNotFoundException


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


class Fix(MemoryManagment):
    def __init__(self, memSize, part):
        self.mem = List(memSize, part)
