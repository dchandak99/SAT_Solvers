#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time
import numpy as np

problem1 = [
 [ 9, 0, 0,   0, 1, 0,   5, 0, 0],
 [ 7, 0, 0,   8, 0, 3,   0, 0, 2],
 [ 0, 0, 0,   0, 0, 0,   3, 0, 8],

 [ 0, 7, 8,   0, 2, 5,   6, 0, 0],
 [ 0, 0, 0,   0, 0, 0,   0, 0, 0],
 [ 0, 0, 2,   3, 4, 0,   1, 8, 0],

 [ 8, 0, 9,   0, 0, 0,   0, 0, 0],
 [ 5, 0, 0,   4, 0, 1,   0, 0, 9],
 [ 0, 0, 1,   0, 5, 0,   0, 0, 4]
]

problem2 = [
[ 0, 8, 0,   0, 0, 3,   0, 0, 0],
[ 5, 0, 3,   0, 4, 0,   2, 0, 0],
[ 7, 0, 4,   0, 8, 0,   0, 0, 3],
    [ 0, 7, 0,   0, 0, 0,   5, 0, 0],
[ 0, 3, 0,   8, 0, 5,   0, 6, 0],
[ 0, 0, 1,   0, 0, 0,   0, 9, 0],
[ 9, 0, 0,   0, 3, 0,   7, 0, 6],
[ 0, 0, 7,   0, 2, 0,   3, 0, 1],
[ 0, 0, 0,   6, 0, 0,   0, 2, 0]
]

problem3 = [
[ 7, 0, 0,   8, 0, 5,   0, 0, 6],
[ 0, 0, 4,   0, 6, 0,   2, 0, 0],
[ 0, 5, 0,   2, 0, 4,   0, 9, 0],
    [ 8, 0, 5,   0, 0, 0,   3, 0, 9],
[ 0, 1, 0,   0, 0, 0,   0, 6, 0],
[ 3, 0, 6,   0, 0, 0,   1, 0, 7],
[ 0, 6, 0,   5, 0, 7,   0, 1, 0],
[ 0, 0, 7,   0, 9, 0,   6, 0, 0],
[ 5, 0, 0,   3, 0, 6,   0, 0, 2]
]

problem = problem3
# problem = problem2

# define the problem variables
# Hint: three dimentional array

v=[[[Bool ("v_{}_{}_{}".format(i,j,k)) for k in range(9)]for j in range(9)]for i in range(9)]
v


def sum_to_one( ls ):
    a=Or(ls)
    c=[]
    for i in range(len(ls)):
        for j in range(i+1,len(ls)):
            c.append(Or(Not(ls[i]),Not(ls[j])))
    c=And(c)
    return And(c,a)


# Accumulate constraints in the following list 
Fs = []


# Encode already filled positions

for i in range(9):
    for j in range(9):
        if problem[i][j]>0:
            k=problem[i][j]-1
            Fs.append(v[i][j][k])

# Encode for i,j  \sum_k x_i_j_k = 1

for i in range(9):
    for j in range(9):
        ls=[]
        for k in range(9):
            ls.append(v[i][j][k])
        Fs.append(sum_to_one(ls))

# Encode for j,k  \sum_i x_i_j_k = 1

for j in range(9):
    for k in range(9):
        ls=[]
        for i in range(9):
            ls.append(v[i][j][k])
        Fs.append(sum_to_one(ls))

# Encode for i,k  \sum_j x_i_j_k = 1

for i in range(9):
    for k in range(9):
        ls=[]
        for j in range(9):
            ls.append(v[i][j][k])
        Fs.append(sum_to_one(ls))

# Encode for i,j,k  \sum_r_s x_3i+r_3j+s_k = 1

for i in range(3):
    for j in range(3):
        for k in range(9):
            ls=[]
            for r in range(3):
                for s in range(3):
                    ls.append(v[3*i+r][3*j+s][k])
            Fs.append(sum_to_one(ls))

s = Solver()
s.add( And( Fs ) )

if s.check() == sat:
    m = s.model()
    for i in range(9):
        if i % 3 == 0 :
            print("|-------|-------|-------|")
        for j in range(9):
            if j % 3 == 0 :
                print ("|", end =" ")
            for k in range(9):
                # FILL THE GAP
                # val model for the variables
                val = m[v[i][j][k]]
                if is_true( val ):
                    print("{}".format(k+1), end =" ")
        print("|")
    print("|-------|-------|-------|")
else:
    print("sudoku is unsat")

# print vars

vs = [ [ [ Bool ("e_{}_{}_{}".format(i,j,k)) for k in range(9)] for j in range(9)] for i in range(9)]
vs


