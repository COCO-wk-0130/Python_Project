import numpy as np
import csv
from math import*

def dec2Mary(dec, M, n):
    result = np.zeros(n)
    i = 0
    for i in range(n):
        result[i] = dec % M
        dec //= M
    return np.array(result[::-1]).astype(np.int64)

def table_generate(n, M, W):
    q = round(pow(M, 1/n)-1, 6)
    v = ceil(sqrt(pow(q, 2)*n))
    R_SE = []
    for k in range(int(pow(2*v+1, n))):
        SE = 0
        temp = []
        index = dec2Mary(k, 2*v+1, n) - v
        for i in index:
            SE += pow(i, 2)
        temp.append(index)
        temp.append(np.dot(index, W) % M)
        temp.append(int(SE))
        R_SE.append(temp)
    R_SE.sort(key = lambda ele: ele[2])
    R_SE.sort(key = lambda ele: ele[1])

    HA = []
    PA = []
    for i in range(len(R_SE)):
        if R_SE[i][1] == len(PA):
            PA.append(R_SE[i])
        else:
            HA.append(R_SE[i])
    return HA, PA

def PSNR(MSE):
    return 10*log(pow(255, 2)/MSE, 10)

def CSV_write(HA, PA, n, M, W):
    v = int(pow(len(HA) + len(PA), 1/n))
    
    #HA
    filename = "HA_" + str(n) + "_" + str(M) + "_("
    for i in range(len(W)):
        filename += str(W[i])
        if i != len(W)-1:
            filename += "_"
        else:
            filename += ")"
            
    with open(filename + ".csv", "w", newline="", encoding = "UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        RowOne = ["HA", n, M]
        for i in range(len(W)):
            RowOne.append("w" + str(i+1))
        writer.writerow(RowOne)
        RowTwo = ["Index", "d", "SE"]
        for i in W:
            RowTwo.append(i)
        writer.writerow(RowTwo)
        
        for i in range(len(HA)):
            Row = [i, HA[i][1], HA[i][2]]
            for j in HA[i][0]:
                Row.append(j)
            writer.writerow(Row)
            
    #PA
    filename = "PA_" + str(n) + "_" + str(M) + "_("
    for i in range(len(W)):
        filename += str(W[i])
        if i != len(W)-1:
            filename += "_"
        else:
            filename += ")"
            
    with open(filename + ".csv", "w", newline="", encoding = "UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        RowOne[0] = "PA"
        writer.writerow(RowOne)
        writer.writerow(RowTwo)
        TSE = 0
        for i in range(len(PA)):
            TSE += PA[i][2]
            Row = [i, PA[i][1], PA[i][2]]
            for j in PA[i][0]:
                Row.append(j)
            writer.writerow(Row)
            
        writer.writerow(["\t", "TSE", TSE])
        writer.writerow(["\t", "MSE", TSE / (M*n)])
        writer.writerow(["\t", "PSNR", PSNR(TSE/(M*n))])
                
#main
def main():
    print("Input the number of pixel cluster(2≤n≤6):")
    n = int(input())
    print("Input the M-ary(2≤M≤1024):")
    M = int(input())
    print("Input n weights and split by space:")
    W = input()
    W = W.split(" ")
    W = np.array(W).astype(np.int64)
    HA, PA = table_generate(n, M, W)
    CSV_write(HA, PA, n, M, W)

while(True):
    main()