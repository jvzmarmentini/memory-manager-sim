#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import argparse


class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size


def partFix(memSize=32, part=4):
    mem = [None] * (memSize // part)
    with open('input.txt') as f:
        lines = f.readlines()
        for line in lines:
            if("IN" in line):
                line = "".join(line.split()).split("IN(", 1)[1].split(")")[0]
                pid, size = line.split(",")
                proc = Process(pid, int(size))
                print(f"IN: {pid=}, {size=}")
                if (int(size) <= part):
                    for t, p in enumerate(mem):
                        if(p == None):
                            mem[t] = proc
                            break
            else:
                pid = line.split("OUT(", 1)[1].split(")")[0]
                print(f"OUT: {pid=}")
                for t, p in enumerate(mem):
                    if(p != None):
                        if(p.pid == pid):
                            mem[t] = None
                            break

            print("|", end="")
            for p in mem:
                if(p == None):
                    print("*"*part, end="|")
                    continue
                print(f"{p.pid*p.size}{'*'*(part-p.size)}", end="|")
            print()
    return 0


def main():
    IN_DEBBUG = True
    """ Main program """
    opt = input("estrategia de alocacao [f, v, b]: ")

    while(mem):
        mem = int(input("tamanho da memoria: "))
        if (math.ceil(math.log2(mem)) == math.floor(math.log2(mem))):
            break
        print("numero deve ser potencia de 2!!")

    if(opt == "f"):
        while(True):
            part = int(input("tamanho da particao: "))
            if (mem % part == 0):
                break
            print("numero deve ser divisivel pelo tamanho da memoria!!")
        partFix(mem, part)
    elif(opt == "v"):
        policy = input("best fit ou worst fit [bf, wf]: ")
        # TODO: particao variavel main
    elif(opt == "b"):
        return 1
        # TODO: buddy main
    return 0


if __name__ == "__main__":
    main()
