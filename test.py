#from tkinter import *
#from tkinter import messagebox
import copy
from decimal import Decimal
import re
import math
import sys

variables_assignment = True
variables_names = []
variables = {}
variables_type = {}
scale = 30
oper = ['+', '-', '*', '/', '^', '%', '>']
condition = ['>', '<', '==', '=', '!=', '!', 'and', 'or']

class Call_Tree:
    def __init__(self):
        self.variables = {}
        self.variables_type = {}
        self.tree = []
        self.variable_names = []

    def set_varbles(self, varbl, varbl_names, varbl_types):
        self.variables = varbl
        self.variables_type = varbl_types
        self.variable_names = varbl_names

    def get_var(self, name):
        return self.variables[name]

    def get_setvar(self):
        return self.variables

    def variabels_changing(self, v_name, v_value):
        self.variables[v_name] = v_value

    def push_elem(self, a):
        self.tree.append(copy.deepcopy(a))

    def start_executing(self):
        for i in self.tree:
            i.execution(self.variables)
        for i in self.variable_names:
            if (self.variables_type[i] == 'integer'):
                self.variables[i] = int(self.variables[i])
            elif (self.variables_type[i] == 'float'):
                self.variables[i] = float(self.variables[i])

    def show_vars(self):
        print(self.variables)

class expression:
    def __init__(self, var, val):
        self.var_name = copy.copy(var)
        self.var_val = copy.copy(val)

    def show_vals(self):
        print(self.var_name, self.var_val)

    def execution(self, set_of_variables):
        set_of_variables[self.var_name] = expr_parse(self.var_val, set_of_variables)


class if_condition:
    def __init__(self, val, set_of_var):
        self.s_o_v = set_of_var
        self.condition = copy.copy(val)
        self.actions = []

    def get_var(self, name):
        return self.s_o_v[name]

    def get_setvar(self):
        return self.s_o_v

    def push_action(self, val):
        self.actions.append(copy.deepcopy(val))

    def execution(self, set_of_variables):
        if (expr_parse(self.condition, set_of_variables) == 1):
            for i in self.actions:
                i.execution(set_of_variables)

class for_loop:
    def __init__(self, var, lower, high, set_of_var):
        self.iter_var = var
        self.s_o_v = set_of_var
        self.begin = copy.copy(lower)
        self.end = copy.copy(high)
        self.low = 0
        self.hig = 0
        self.actions = []

    def get_setvar(self):
        return self.s_o_v

    def get_var(self, name):
        return self.s_o_v[name]

    def push_action(self, val):
        self.actions.append(copy.deepcopy(val))

    def execution(self, set_of_variables):
        self.low = expr_parse(self.begin, set_of_variables)
        self.hig = expr_parse(self.end, set_of_variables)
        for i in range(int(self.low), int(self.hig) + 1):
            set_of_variables[self.iter_var] = i
            for j in self.actions:
                j.execution(set_of_variables)

class read:
    def __init__(self):
        self.enter_variables = {}

    def add_var(self, var):
        self.enter_variables[var] = 0

    def execution(self, set_of_variables):
        for i in self.enter_variables:
            set_of_variables[i] = input()

def operat(a, k):
    n = 0
    while (a[k] == '-'):
        a.pop(k)
        n += 1
    if (n % 2 == 0):
        a.insert(k , '+')
    else:
        a.insert(k, '-')
    return a, k

def clr(a, res):
    for i in range(4):
        a.pop(0)
    a.insert(0, res)
    return a
    
def clr1(a, res):
    for i in range(3):
        a.pop(0)
    a.insert(0, res)
    return a

def count(an):
    a = an
    k = 0
    res = 0
    ni = 0
    while (ni < (len(a) - 1)):
        if (a[ni] in condition):
            if (a[ni] == '>'):
                if (Decimal(a[ni - 1]) > Decimal(a[ni + 1])):
                    res = 1
                    return res
                else:
                    res = 0
                    return res
            elif (a[ni] == '<'):
                if (Decimal(a[ni - 1]) < Decimal(a[ni + 1])):
                    res = 1
                    return res
                else:
                    res = 0
                    return res
            elif (a[ni] == '=='):
                if (Decimal(a[ni - 1]) == Decimal(a[ni + 1])):
                    res = 1
                    return res
                else:
                    res = 0
                    return res
            elif (a[ni] == '!='):
                if (Decimal(a[ni - 1]) != Decimal(a[ni + 1])):
                    res = 1
                    return res
                else:
                    res = 0
                    return res
            elif (a[ni] == '!'):
                if (Decimal(a[ni + 1]) != 0):
                    res = 0
                    return res
                elif (Decimal(a[ni + 1]) == 0):
                    res = 1
                    return res
            elif (a[ni] == 'and'):
                res = Decimal(a[ni - 1]) and Decimal(a[ni + 1])
                a.pop(ni - 1)
                a.pop(ni - 1)
                a.pop(ni - 1)
                a.insert(ni - 1, str(res))
            elif (a[ni] == 'or'):
                res = Decimal(a[ni - 1]) or Decimal(a[ni + 1])
                a.pop(ni - 1)
                a.pop(ni - 1)
                a.pop(ni - 1)
                a.insert(ni - 2, str(res))
        else:
            ni += 1
    if (len(a) == 1):
        res = Decimal(a[0])
    while (k < (len(a) - 1)):
        if (a[k].isdigit()):
            k += 1
        if (a[k] == '-'):
            a, k = operat(a, k)
        k = 0
        if (a[k] == '-'):
            a.pop(k)
            res -= slag(a, k)
        elif (a[k] == '+'):
            if (a[k + 1] == '-'):
                k += 1
                a, k = operat(a, k)
                if (a[k] == '+'):
                    a.pop(k)
                    a.pop(k - 1)
                    a.insert(k - 1, '+')
                    k -= 1
                else:
                    a.pop(k)
                    a.pop(k - 1)
                    a.insert(k - 1, '-')
                    k -= 1
            if (a[k] == '+'):
                a.pop(k)
                res += slag(a, k)
            else:
                a.pop(k)
                res -= slag(a, k)
        else:
            res += slag(a, k)
        k = 0
    return res

def slag(a , k):
    if (k < len(a) - 1):
        k += 1
    else:
        return Decimal(a[0])
    res = 0
    if (a[k] == '+' or a[k] == '-'):
        a1 = Decimal(a[0])
        a.pop(0)
        return a1
    else:
        while (a[k] != '+' and a[k] != '-'):
            if (a[k].isdigit()):
                k += 1
            if (a[k + 1] == '-'):
                l = k
                k += 1
                a, k = operat(a, k)
                k = l
            if (a[k] == '*'):
                if (a[k + 1] == '-'):
                    res = -(Decimal(a[k - 1]) * Decimal(a[k + 2]))
                    a = clr(a, res)
                elif (a[k + 1] == '+'):
                    res = Decimal(a[k - 1]) * Decimal(a[k + 2])
                    a = clr(a, res)
                else:
                    res = Decimal(a[k - 1]) * Decimal(a[k + 1])
                    a = clr1(a, res)
            elif (a[k] == '/'):
                if (a[k + 1] == '-'):
                    res = -(Decimal(a[k - 1]) / Decimal(a[k + 2]))
                    a = clr(a, res)
                elif (a[k + 1] == '+'):
                    res = Decimal(a[k - 1]) / Decimal(a[k + 2])
                    a = clr(a, res)
                else:
                    res = Decimal(a[k - 1]) / Decimal(a[k + 1])
                    a = clr1(a, res)
            elif (a[k] == '%'):
                if (a[k + 1] == '-'):
                    res = -(Decimal(a[k - 1]) % Decimal(a[k + 2]))
                    a = clr(a, res)
                elif (a[k + 1] == '+'):
                    res = Decimal(a[k - 1]) % Decimal(a[k + 2])
                    a = clr(a, res)
                else:
                    res = Decimal(a[k - 1]) % Decimal(a[k + 1])
                    a = clr1(a, res)
            if (k < len(a) - 1):
                k = 1
            else:
                return Decimal(a[0])
        a1 = Decimal(a[0])
        a.pop(0)
        return a1 

def power(a):
    if (len(a) == 1):
        return a
    i = 0
    res = 0
    while (i < len(a)):
        if (a[i].isdigit()):
            i += 1
        if (a[i + 1] == '-'):
            l = i
            i += 1
            a, i = operat(a, i)
            i = l
        if (a[i] == '^'):
            if (a[i + 1] == '-'):
                res = (Decimal(a[i - 1]) ** (-Decimal(a[i + 2])))
                i -= 1
                a.pop(i)
                a.pop(i)
                a.pop(i)
                a.pop(i)
                a.insert(i, str(res))
            elif (a[i + 1] == '+'):
                res = Decimal(a[i - 1]) ** Decimal(a[i + 2])
                i -= 1
                a.pop(i)
                a.pop(i)
                a.pop(i)
                a.pop(i)
                a.insert(i, str(res))
            else:
                res = Decimal(a[i - 1]) ** Decimal(a[i + 1])
                i -= 1
                a.pop(i)
                a.pop(i)
                a.pop(i)
                a.insert(i, str(res))
        i += 1
        if (i >= len(a) - 1):
            return a
    return a

def perem(a, x):
    i = 0
    s = ''
    while (i < len(a)):
        if (is_variable(a[i]) == True):
            s = a[i]
            a.pop(i)
            a.insert(i, str(x[s]))
        i += 1
    return a

def isNot_a_digit(st):
    k = 0
    for i in st:
        if (i == '(' or i == ')'):
            k += 1
    if (k > 0):
        return 0
    else:
        return 1
    
def is_variable(s_):
    k = 0
    for i in s_:
        if i.isalpha():
            k += 1
    if k > 0:
        return True
    else:
        return False

def normalized(a, x_set):
    i = 0
    ma = []
    while (i < (len(a))):
        if (isNot_a_digit(a[i]) == 1 or len(a[i]) <= 1):
            i += 1
        elif (isNot_a_digit(a[i]) == 0 and not(a[i].isalpha())):
            ma = spread(a[i][1:(len(a[i]) - 1):1], 0)
            b = count(normalized(ma, x_set))
            a.pop(i)
            a.insert(i, str(b))
            i += 1
    ma = perem(a, x_set)
    ma = power(ma)
    return ma

def Digit(stri, n):
    a = ''
    while (stri[n].isdigit() or stri[n] == '.'):
        a = a + stri[n]
        n += 1
        if (n > len(stri) - 1):
            return a, n
    return a, n

def get_operat(strin, n):
    a = ''
    while(strin[n] in condition):
        a = a + strin[n]
        n += 1
        if (n > len(strin) - 1):
            return a, n
    return a, n

def skob(stry, n):
    l = 0
    t = 0
    a = ''
    if (stry[n] == '('):
            a = a + stry[n]
            t += 1
            n += 1
    while (stry[n] != ')' or l < t):
        if (stry[n] == '('):
            t += 1
        a = a + stry[n]
        n += 1
        if (stry[n] == ')'):
            l += 1
        if (n > len(stry) - 1):
            return a, n
    a = a + stry[n]
    n += 1
    return a, n

def spread(strn, y):
    n = y
    str1 = ''
    a = []
    if (strn[n] == '-' or strn[n] == '+'):
        a.append(strn[n])
        n += 1
    while (n < len(strn)):
        if (strn[n] in oper):
            a.append(strn[n])
            n += 1
        if (strn[n] in condition):
            str1, n = get_operat(strn, n)
            a.append(str1)
        if (strn[n].isdigit()):
            str1, n = Digit(strn, n)
            a.append(str1)
        elif (strn[n].isalpha()):
                str1, n = get_func(strn, n)
                a.append(str1)
        elif (strn[n] == '('):
            str1, n = skob(strn, n)
            a.append(str1)
        if (n >= len(strn)):
            return a
    return a

def get_func(func, n):
    a = ''
    while (func[n].isalpha()):
        a = a + func[n]
        n += 1
        if (n > len(func) - 1):
            return a, n
    return a, n

def expr_parse(st, s_x):
    s_str = ''
    for i in st:
        if (i != ' '):
            s_str = s_str + i
    res = count(normalized(spread(s_str, 0), s_x))
    return res

def del_spaces(st):
    s_str = ''
    for i in st:
        if (i != ' '):
            s_str = s_str + i
    return s_str

def string_parser(where):
    global variables_assignment
    flag = True
    while (flag == True):
        string = input()       
        s1 = '(var)*\s*\w+\s*:\s*(integer|float);+'
        s2 = '\s*\w+\s*:=[\s*\w\(\)\/\+-\.]+;+' 
        s3 = '(\s*if[><=\(\)\s\w]+\s*then\s*)'  
        s4 = '\s*begin\s*'  
        s5 = '\s*end[\.;]*\s*'
        s6 = '\s*for\s+\w+\s*:=\s*[\s*\w\(\)\/\+-]+\s+to\s+[\w\s*\(\)*\/\+-]+\s+do\s*'
        s7 = 'Function\s+\w+\s*\([\w, ]+:\s*(integer|float)\s*\)\s*:\s*(integer|float)\s*;'
        s8 = '(R|r)ead\([\w, ]+\)\s*;'
        s9 = 'var'
        s10 = '[ ]+'

        if (re.search(s1, string)):
            pRes = re.findall(r'\w+', string)
            for i in pRes:
                if not(i == 'var' or i == 'integer' or i == 'float'):
                    variables[i] = 0
                    variables_type[i] = pRes[len(pRes) - 1]
                    variables_names.append(i)
                    
        elif (re.search(s6, string)):
            pRes = re.findall(r'[^fortd:=]+', string)
            if (len(pRes) == 4):
                pRes.pop(0)
            for_l = for_loop(del_spaces(pRes[0]), pRes[1], pRes[2], where.get_setvar())
            string_parser(for_l)
            if (type(where) == Call_Tree):
                where.push_elem(for_l)
            elif (type(where) == if_condition):
                where.push_action(for_l)
            elif (type(where) == for_loop):
                where.push_action(for_l)

        elif (re.search(s2, string)):
            pRes = re.findall(r'[^:=;]+', string)
            Expr = expression(del_spaces(pRes[0]), pRes[1])#count(normalized(spread(pRes[1], 0), where.get_var(pRes[0]))))
            Expr.show_vals()
            if (type(where) == Call_Tree):
                where.push_elem(Expr)
            elif (type(where) == if_condition):
                where.push_action(Expr)
            elif (type(where) == for_loop):
                where.push_action(Expr)
    
        elif (re.search(s3, string)): 
            s = ''
            n = 0
            while (n < len(string) - 1): 
                if (string[n] + string[n + 1] == 'if'):
                    n += 2
                    continue
                elif (string[n] + string[n + 1] + string[n + 2] + string[n + 3]== 'then'):
                    n += 4
                    continue
                elif (string[n] == ' '):
                    n += 1
                    continue
                else:
                    s = s + string[n]
                    n += 1

            if_cond = if_condition(s, where.get_setvar())            
            string_parser(if_cond)
            if (type(where) == Call_Tree):
                where.push_elem(if_cond)
            elif (type(where) == if_condition):
                where.push_action(if_cond)
            elif (type(where) == for_loop):
                where.push_action(if_cond)

        elif (re.search(s4, string)):
            if variables_assignment == True:
                AST.set_varbles(variables, variables_names, variables_type)
                variables_assignment == False
        elif (re.search(s8, string)):
            pRes = re.findall(r'\w+', string)
            Read_obj = read()
            for i in pRes:
                if not(i == 'Read' or i == 'read'):
                    Read_obj.add_var(i)
            if (type(where) == Call_Tree):
                where.push_elem(Read_obj)
            elif (type(where) == if_condition):
                where.push_action(Read_obj)
            elif (type(where) == for_loop):
                where.push_action(Read_obj)

        elif (re.search(s5, string)):
            flag = False

        elif (re.search(s9, string)):
            continue

        elif (re.search(s10, string)):
            continue

        else:
            print('Syntax error')
            sys.exit()

def executing():
    AST.start_executing() 

AST = Call_Tree()
string_parser(AST)
executing()
AST.show_vars()

