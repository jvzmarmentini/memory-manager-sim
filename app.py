#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from Buddy import Buddy
from Fix import Fix
from Variable import Variable


def main():

    while(True):
        opt = input("Estrategia de alocacao [f, v, b]: ")
        if (opt in "FfVvBb"):
            break
        print("!!Estategia invalida")
    while(True):
        mem = int(input("Tamanho da memoria: "))
        if (math.ceil(math.log2(mem)) == math.floor(math.log2(mem))):
            break
        print("!!Numero deve ser potencia de 2")

    if(opt.lower() == "f"):
        while(True):
            part = int(input("Tamanho da particao: "))
            if (mem % part == 0):
                break
            print("!!Numero deve ser divisivel pelo tamanho da memoria")
        f = Fix(mem, part)
        f.run("input.txt")
    elif(opt.lower() == "v"):
        policy = input("best fit ou worst fit [bf, wf]: ")
        v = Variable(mem, policy)
        v.run("input3.txt")
    elif(opt.lower() == "b"):
        b = Buddy(mem)
        b.run("input3.txt")
    return 0


if __name__ == "__main__":
    main()
