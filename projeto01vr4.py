import csv
from sympy import *

arquivo = open('arquivoCSV/column_bin_3a_p.csv')

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


def verificaPrimeiroElemento(arquivoPacientes):
    valores = pegaValores(arquivoPacientes)
    conf = False
    for val in valores:
        if val[-1] == '1' and val[0] == '1':
            conf = True
    return conf


def satisfiability_brute_force(arquivoPacientes):
    variaveis = atoms(arquivoPacientes)
    tamanho = len(variaveis) - 1
    formula = truth_value(arquivoPacientes)
    formula2 = formula

    for i in range(tamanho):
        a = variaveis[i]
        globals()[f'x{i}'] = symbols(a)
        formula2 = formula2.replace(variaveis[i], f'x{i}')

    formulaRescrita = S(formula2)
    resultado = simplify_logic(formulaRescrita)
    return resultado


def organizaRegras(arquivoPacientes):
    variaveis = atoms(arquivoPacientes)
    tamanho = len(variaveis) - 1
    formula = str(satisfiability_brute_force(arquivoPacientes))
    formula = formula.replace('~', '')
    formula = formula.replace('(', '( ')
    formula = formula.replace(')', ' )')
    form = formula.split()
    result = []

    for i in form:
        if i not in result and (i != '(' or i != ')' or i != '&' or i != '|'):
            result.append(i)
    resultado = ' '.join(result)

    for i in range(tamanho):
        resultado = resultado.replace(f'x{i}', variaveis[i])

    if verificaVazios(arquivoPacientes):
        nv = variaveis[-2].replace('<=', '>=')
        nv2 = variaveis[-2].replace('<=', '>')
        resultado = resultado.replace(f'& {variaveis[-2]}', f'& {nv}')
        resultado = resultado.replace(f'| {variaveis[-2]}', f'& {nv2}')

    if len(resultado.split(variaveis[0])) > 0:
        if verificaPrimeiroElemento(arquivoPacientes):
            nv = variaveis[0]
            resultado = resultado.replace(nv, '')
            resultado = resultado.replace('( ', f'( {nv}, ')
        else:
            nv = variaveis[0]
            nv2 = variaveis[0].replace('<=', '>')
            resultado = resultado.replace(nv, '')
            resultado = resultado.replace('( ', f'( {nv2} & ')
    resultado = resultado.replace('( ', '(')
    resultado = resultado.replace(' )', ')')
    resultado = resultado.replace(' & ', '&')
    resultado = resultado.replace('|', '')
    resultado = resultado.replace('& (', '(')
    resultado = resultado.replace(') &', ')')
    resultado = resultado.replace(')&', '(')
    resultado = resultado.replace('&)', ')')
    resultFinal = resultado.split()
    res = []
    for re in resultFinal:
        re = re.replace('(', '')
        re = re.replace(')', '')
        res.append(re)
    return res


def imprimeRegras(arquivoPacientes):
    regras = organizaRegras(arquivoPacientes)
    print('{', end='')
    for valor in regras:
        aux = valor
        if len(valor.split('(')) == 1 and len(valor.split(')')) == 1:
            valor = '(' + valor + ')'
            valor = valor.replace('(&', '(')
            valor = valor.replace(')&', ')')
        valor = valor.replace('(', '[')
        valor = valor.replace(')', ']')
        valor = valor.replace('&', ', ')
        translation = {39: None}
        lista = str(valor).translate(translation)
        print(lista, '-> P', end='')
        if aux != regras[-1]:
            print(', ', end='')
    print('}')

m = 1
if len(organizaRegras(dadosPacientes)) >= m:
    imprimeRegras(dadosPacientes)
else:
    print('Total de regras insuficientes')



