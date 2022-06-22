from src.Process import Process
from utils.Exceptions import MemoryOverflowException, ProcessNotFoundException


class MemoryManagment:
    def __str__(self):
        return self.mem

    def __in(self, pid: int, size: int) -> None:
        p = Process(pid, size)
        print(f"IN: {p}")
        return self.mem.add(p)

    def __out(self, pid: int) -> None:
        print(f"OUT: {pid}")
        return self.mem.remove(pid)

    def simulate(self, path: str) -> None:
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
                if("OUT" in line):
                    pid = line.split("OUT(", 1)[1].split(")")[0]
                    try:
                        print(self.__out(pid))
                    except ProcessNotFoundException as e:
                        print(e)
