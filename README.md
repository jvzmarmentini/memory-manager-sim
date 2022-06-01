# memory-manager-sim

https://moodle.pucrs.br/pluginfile.php/4232655/mod_resource/content/2/TP2.pdf?redirect=1

## processo
cada processo é representado por um id e possui um tamanho

## partições fixas de mesmo tamanho
in: tamanho da partição

struct: array de nodos com tamanho fixo

## partições variáveis 
in: política de alocação (best-fit ou worst-fit)

struct: linked list de nodos
https://panda.ime.usp.br/panda/static/pythonds_pt/02-EDBasicos/ImplementinganUnorderedListLinkedLists.html
https://realpython.com/linked-lists-python/

## partições definidas com o sistema buddy
in: -

struct: arvore binaria nao balanceada
https://stackoverflow.com/questions/2598437/how-to-implement-a-binary-tree
