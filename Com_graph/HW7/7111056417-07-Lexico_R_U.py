from itertools import permutations 
import numpy as np

def factorial(n):
    fact = 1
    for i in range(1, n):
        fact *= i+1
    return fact

def Ranking(P):
    n = len(P)
    Digits = [i for i in range(n)]
    Ps = list(permutations(Digits))
    for rank in range(len(Ps)):
        if P == list(Ps[rank]):
            return rank

def Unranking(rank, n):
    Digits = [i for i in range(n)]
    P = list(permutations(Digits))
    return list(P[rank])

def main(n):
    fact = factorial(n)
    Func = input("Ranking(r) or Unranking(u):")
    if Func == "r":
        P = input("Input the list and split by space:").split(" ")
        P = list(np.array(P).astype(np.int64))
        print("Rank:", Ranking(P))
    else:
        rank = int(input("Input rank(<{}):".format(fact)))
        P = Unranking(rank, n)
        print("Lexicographic Order Lis:", end = "")
        for i in P:
            print(i, end = " ")
        print("\n")
        
n = int(input("Input the number of elements(n>0):"))
while(n > 0):
    main(n)
    n = int(input("Input the number of elements(n>0):"))