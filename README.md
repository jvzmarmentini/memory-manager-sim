# memory-manager-sim

simulador do gerenciador de memoria do sisop. foram implementadas tres estrategias de alocação, sendo elas partição fixa, partição variável e buddy.

## python version

Python 3.10.5

obs: **a principio** funciona em qualquer versão > 3.0, mas não foi testado

## usage

o arquivo de instrução deve necessariamente estar no diretório test.

para adicionar um processo na memoria, insira conforme o padrão (case sensitive):
"IN(PID, Size)"

para remover um processo da memoria, insira conforme o padrão (case sensitive):
"OUT(PID)"

run `python app.py`
