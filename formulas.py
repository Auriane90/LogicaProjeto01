# import sympy
from sympy import *

# Variaveis
a = symbols('a')
b = symbols('b')
c = symbols('c')
d = symbols('d')
e = symbols('e')
f = symbols('f')
g = symbols('g')
h = symbols('h')
i = symbols('i')
j = symbols('j')
k = symbols('k')
l = symbols('l')
m = symbols('m')
n = symbols('n')
o = symbols('o')
p = symbols('p')
q = symbols('q')
r = symbols('r')
s = symbols('s')
t = symbols('t')
u = symbols('u')
v = symbols('v')
w = symbols('w')
x = symbols('x')
y = symbols('y')
z = symbols('z')


def atoms_names(A):
    resultado = A.atoms(Symbol)
    print("As atomicas da formula são: ", resultado)


def truth_value(formula, interpretacao):
    if(interpretacao == True):
        print("A formula ", formula, " é True")
    else:
        print("A formula ", formula, " é False")


def satisfiability_brute_force(formula, interpretacao):
    if(interpretacao == True):
        print("A formula ", formula, " é Satisfatoria")
    else:
        print("A formula ", formula, " é não Satisfatoria")


formula = Or(Not(And(p, s)), p)
atoms_names(formula)


#para usar a formula defina os valores das variaveis
formula2 = Or(Not(And(p, s)), p)
p = True
s = False
interpretacao = Or(Not(And(p, s)), p)

truth_value(formula2, interpretacao)
satisfiability_brute_force(formula2, interpretacao)

