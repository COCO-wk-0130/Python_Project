from math import*
import random

population_size = 10

def resort(genes, n):
    temp = genes[n]
    genes = sorted(genes[:n])
    genes.append(temp)
    return genes

def init(n, F):
    chromosone = [[0 for _ in range(n+1)] for _ in range(population_size)]
    b = ceil(pow(F, 1/n))
    for i in range(population_size):
        j = 0
        M = 1
        while j < n:
            chromosone[i][j] =random.randrange(b-2, b+3)
            M = M*chromosone[i][j]
            j = j+1
            if j == n:
                if M >= F:
                    break
                else:
                    M = 1
                    j = 0
        chromosone[i] = resort(chromosone[i], n)
    chromosone = fitness(chromosone, n, F)
    return chromosone

def EMSE(B):
    if B%2 == 0:
        return (pow(B, 2)+2)/12
    else:
        return(pow(B, 2)-1)/12

def fitness(chromosone, n, F):
    for i in range(population_size):
        fit = 0
        M = 1
        for j in range(n):
            M*=chromosone[i][j]
            fit += EMSE(chromosone[i][j])
        if M < F:
            chromosone[i][n] = 100
        else:
            chromosone[i][n] = round(fit/n, 4)
    chromosone = sorted(chromosone, key = lambda x: x[n])
    OBV = list(chromosone[0])
    return chromosone

def crossover(chromosone, n, F):
    #selection
    parent = []
    parent.append(list(chromosone[0]))
    parent.append(list(chromosone[1]))
    for i in range(n):
        if i%2 == 0:
            parent[0][i], parent[1][i] = parent[1][i], parent[0][i]
    chromosone[population_size-2] = resort(parent[0], n)
    chromosone[population_size-1] = resort(parent[1], n)
    chromosone = fitness(chromosone, n, F)
    return chromosone

def mutation(chromosone, n, F):
    b = ceil(pow(F, 1/n))
    for i in range(population_size):
        p = random.random()
        if p < 0.01:
            position = random.randrange(0, n)
            chromosone[i][position] = random.randrange(b-2, b+3)
        else:
            continue
    chromosone = fitness(chromosone, n, F)
    return chromosone

def gene_generation(chromosone, n, F):
    b = ceil(pow(F, 1/n))
    for i in range(2, population_size, 1):
        j = 0
        M = 1
        while j < n:
            chromosone[i][j] =random.randrange(b-2, b+3)
            M = M*chromosone[i][j]
            j = j+1
            if j == n:
                if M >= F:
                    break
                else:
                    M = 1
                    j = 0
        chromosone[i] = resort(chromosone[i], n)
    chromosone = fitness(chromosone, n, F)
    return chromosone

def history_best(CBV, OBV, n):
    if CBV[n] < OBV[n]:
        return list(CBV)
    else:
        return list(OBV)

def output(OBV, n, F):
    M = 1
    print("1. Optimal Base Vector OBV：", end='')
    for i in range(n):
        M = M*OBV[i]
        if i == n-1:
            print(OBV[i])
        else:
            print(OBV[i], end = ", ")
    print("2. Derived Notation M：", M)
    print("3. Difference D：", M-F)
    print("4. EMSE OBV：", OBV[n])
    print("5. PSNR：", round(10*log((255*255)/OBV[n], 10), 2))
    
    

def main():
    cycle = 50
    while True:
        n_F = input().split(" ")
        n = int(n_F[0])
        F = int(n_F[1])
        if n == 0 or F == 0:
            break
        CBV = init(n, F)
        OBV = CBV[0]
        for G in range(cycle):
            CBV = crossover(CBV, n, F)
            CBV = mutation(CBV, n, F)
            CBV = gene_generation(CBV, n, F)
            OBV = history_best(CBV[0], OBV, n)
        output(OBV, n, F)
        
main()