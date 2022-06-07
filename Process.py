class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = int(size)

    def __str__(self):
        return f"{self.pid=}, {self.size=}"

    def __eq__(self, other):
        if self.pid == None:
            return False
        return self.pid == other
