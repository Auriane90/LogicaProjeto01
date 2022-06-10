import csv
from sympy import *

arquivo = open('arquivoCSV/column_bin_3a_4p.csv')

dados = csv.reader(arquivo)
dadosPacientes = []

for dado in dados:
    dadosPacientes.append(dado)


def atoms(arquivoPacientes):
    resultado = []
    for dado in arquivoPacientes:
        for d in dado:
            if d != '1' and d != '0':
                if d is not resultado:
                    aux = d
                    aux2 = aux.replace(' ', '')
                    resultado.append(aux2)
    return resultado


def pegaValores(arquivoPacientes):
    resultado = []
    variaveis = atoms(arquivoPacientes)
    cont = len(variaveis)
    aux = []
    cont2 = 0
    for dado in arquivoPacientes:
        for d in dado:
            if d == '1' or d == '0':
                cont2 = cont2 + 1
                aux.append(d)
                if(cont2 == cont):
                    resultado.append(aux)
                    aux = []
                    cont2 = 0
    return resultado


def truth_value(arquivoPacientes):
    variaveis = atoms(arquivoPacientes)
    valores = pegaValores(arquivoPacientes)
    tamanho = len(valores)
    cont = 0
    resultado = str()
    aux = str()

    for valor in valores:
        cont = cont + 1
        for var, val in zip(variaveis, valor):
            if val == '1' and var != 'P':
                aux = aux + var
                if var != variaveis[-2]:
                    aux = aux + ' & '
            if val == '0' and var != 'P':
                aux = aux + '~' + var
                if var != variaveis[-2]:
                    aux = aux + ' & '
        resultado = resultado + '(' + aux + ')'
        #if valor[-1] == '1':
            #resultado = resultado + ' >> p '
        #else:
            #resultado = resultado + ' >> ~p '
        if cont != tamanho:
            resultado = resultado + ' | '
        aux = ''
    return resultado


def verificaVazios(arquivoPacientes):
    variaveis = atoms(dadosPacientes)
    pg = pegaValores(arquivoPacientes)
    tg = []
    aux = []
    for p in pg:
        for v, x in zip(variaveis, p):
            if x == '1' and v != 'P':
                aux.append(x)
        tg.append(aux)
        aux = []
    conf = False
    for t in tg:
        if not t:
            conf = True
    return conf


variaveis = atoms(dadosPacientes)
tamanho = len(variaveis) - 1
formula = truth_value(dadosPacientes)
formula2 = formula

for i in range(tamanho):
    a = variaveis[i]
    globals()[f'x{i}'] = symbols(a)
    formula2 = formula2.replace(variaveis[i], f'x{i}')


formulaRescrita = S(formula2)
simp = simplify_logic(formulaRescrita)

simpS = str(simp)

simpS = simpS.replace('~', '')
simpS = simpS.replace('(', '( ')
simpS = simpS.replace(')', ' )')
s1 = simpS
sl = []
v = s1.split()
for i in v:
    if i not in sl and (i != '(' or i != ')' or i != '&' or i != '|'):
        sl.append(i)
simpS = ' '.join(sl)

simpS = simpS.replace('| ( & )', '')
for i in range(tamanho):
    simpS = simpS.replace(f'x{i}', variaveis[i])

simpS = simpS.replace('(', '[')
simpS = simpS.replace(')', ']')
simpS = simpS.replace(' &', ',')
simpS = simpS.replace('|', '-> P,')
simpS = '{' + simpS + '}'
simpS = simpS.replace(' }', '}')

simpS = simpS.replace(f'{variaveis[0]}', '')

simpS = simpS.replace(', [, ]', '')
vericarPrimeiroElem = len(simpS.split(f'{variaveis[0]}'))

if vericarPrimeiroElem == 1:
    zl = variaveis[0]
    zl2 = zl.replace('<=', '>')
    simpS = simpS.replace('[', f'[{zl2}, ')
else:
    zl = variaveis[0]
    simpS = simpS.replace('[', f'[{zl}, ')

if verificaVazios(dadosPacientes):
    sd = len(simpS.split(f'{variaveis[-2]}'))
    if sd > 0:
        nm = variaveis[-2].replace('<', '>')
        nm2 = variaveis[-2]
        simpS = simpS.replace(nm2, nm)
    else:
        nm = variaveis[-2].replace('<=', '>')
        simpS = simpS.replace('}', ', [' + nm + '] -> P}')

simpS = simpS.replace('}', ' -> P}')
simpS = simpS.replace(', [', '[')
simpS = simpS.replace('-> P, ', '-> P], [')
simpS = simpS.replace(', [ -> P', '')
simpS = simpS.replace(' -> P]', '] -> P')
simpS = simpS.replace(']]', ']')
simpS.strip()



m = 3
total = len(simpS.split(']')) - 1

if m >= total:
    print(simpS)
else:
    print('Total de regras insulficiente')
