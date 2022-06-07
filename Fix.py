from Process import Process
from utils.Colors import bc


class Fix:
    def __init__(self, memSize=32, part=4):
        self.memSize = memSize
        self.part = part
        self.mem = [None] * (memSize // part)

    def __str__(self):
        return "|{0}|".format('|'.join(["*" * self.part if p is None
                                        else f"{bc.GREEN}{p.pid*p.size}{'*'*(self.part-p.size)}{bc.ENDC}"
                                        for p in self.mem]))

    def __in(self, p: Process) -> None:
        print(f"IN: {p}")
        if(p.size > self.part or None not in self.mem):
            return print(f"{bc.FAIL}!!Espaco insuficiente de memoria{bc.ENDC}")
        for i, e in enumerate(self.mem):
            if(e == None):
                self.mem[i] = p
                return print(self)

    def __out(self, pid: int) -> None:
        print(f"OUT: {pid}")
        for t, p in enumerate(self.mem):
            if(p == pid):
                self.mem[t] = None
                return print(self)

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
