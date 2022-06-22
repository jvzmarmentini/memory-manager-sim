from utils.Colors import bc


class ProcessNotFoundException(Exception):
    def __init__(self, pid):
        super().__init__(f"{bc.FAIL}!!PID {pid} nao encontrado{bc.ENDC}\n")


class MemoryOverflowException(Exception):
    def __init__(self):
        super().__init__(
            f"{bc.FAIL}!!Espaco insuficiente de memoria{bc.ENDC}\n")
