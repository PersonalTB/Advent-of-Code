"""
*** *** ADVENT OF CODE - DAY 18 - OPERATION ORDER *** ***

Src: https://adventofcode.com/2020/day/18
Setting: help with maths homework, but with a twist: the operators have a different evaluation precedence order
Challenge: evaluate the expressions based on the new evaluation precedence order

Input: input.txt, a .txt file containing the homework

e.g.

1 + 2 * 3 + 4 * 5 + 6 
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5) 
5 + (8 * 3 + 9 + 3 * 4 * 3) 
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) 
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2

In part 1, the evaluation preceence order is as follows:
1. Brackets
2. Addition, Multiplication
(so addition and multiplication are on the same operator precedence level, with left-to-right associativity)

In the example above, these evaluate to [71,51,26,437,12240,13632], with a sum of 26457

In part 2, the evaluation precedence order is as follows:
1. Brackets
2. Addition
3. Multiplication
(so addition and multiplication are switched from the normal operator precedence)

In the example above, these evaluate to [231,51,46,1445,669060,23340], with a sum of 694173

The challenge consists of two parts:
Part 1: Evaluate each line of the homework with * and + on the same left-to-right precedence level; what is the sum of the resulting values?
Part 2: Evaluate each line of the homework with * and + having swapped precedence level; what is the sum of the resulting values?

"""

data_file = open('input.txt','r')
#data_file = open('test_input.txt','r')
data = data_file.read().strip().split('\n')

# *** PART 1: Evaluate each line of the homework with * and + on the same left-to-right precedence level; what is the sum of the resulting values? ***

print("Part 1: Evaluate each line of the homework with * and + on the same left-to-right precedence level; what is the sum of the resulting values?")

import ast
import operator as op

def alt_eval(node, operators):
    if isinstance(node, ast.Num): 
        return node.n
    elif isinstance(node, ast.BinOp):
        return operators[type(node.op)](alt_eval(node.left, operators), alt_eval(node.right, operators))

def parse_and_alt_eval_expr(expr, operators):
    return alt_eval(ast.parse(expr, mode='eval').body, operators)

data_1 = [d.replace('*', '-') for d in data] # switch operator of mult with that of sub so it gets parsed on the same level as plus (i.e. same precedence, left-to-right),
operators_1 = {ast.Sub: op.mul, ast.Add: op.add} # but then still make it evaluate using their own operators

print(sum([parse_and_alt_eval_expr(d, operators_1) for d in data_1]))

# solution for test_input.txt: 26457
# solution for input.txt: 202553439706

# *** PART 2: Evaluate each line of the homework with * and + having swapped precedence level; what is the sum of the resulting values? ***

print("Part 2: Evaluate each line of the homework with * and + having swapped precedence level; what is the sum of the resulting values? ")

data_2 = [d.translate(str.maketrans('*+', '+*')) for d in data] # switch operators of plus and mult operators so it gets parsed with switched precedence,
operators_2 = {ast.Mult: op.add, ast.Add: op.mul} # but then still make it evaluate using their own operators

print(sum([parse_and_alt_eval_expr(d, operators_2) for d in data_2]))

# solution for test_input.txt: 694173
# solution for input.txt: 88534268715686

"""

Reflection:

- Started creating my own parsing algorithm, and then I found out python had its own tree eval library (abstract syntax trees - ast)
- then it took a little bit of research to find out how to switch the operator precedences
- not too happy with the implementation, though, it's super hacky, I would've liked it better if I had/could have created my own operators 

"""
