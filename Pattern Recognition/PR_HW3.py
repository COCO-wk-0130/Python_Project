import numpy as np
import pandas as pd
from math import*
from sklearn.preprocessing import MinMaxScaler #標準化
from scipy import stats

class SOFM:
    def __init__(self, data, label, neural_num = 10, iter_num = 100, learning_rate = 0.05):
        self.data = data
        self.label = label
        self.class_num = len(np.unique(label))
        self.neural_num = neural_num
        self.iter_num = iter_num
        self.learning_rate = learning_rate
        self.feature_num = data.shape[1]
        self.nodes = np.random.rand(self.neural_num, self.neural_num, self.feature_num)
        self.counts = np.zeros([self.neural_num, self.neural_num])
        self.label_counts = np.zeros([self.class_num, self.neural_num, self.neural_num])
        self.winner = [0, 0]

    def select_winner(self, d):
        M = float('inf')
        self.winner = [-1, -1]
        for i in range(self.neural_num):
            for j in range(self.neural_num):
                dis =ㄋ(self.nodes[i][j](self.nodes[i][j] - d, 2)))
                if dis < M:
                    M = dis
                    self.winner = [i, j]
    
    def update(self, d):
        head = np.zeros(2)
        tail = np.zeros(2)
        #邊界處理
        for i in range(2):
            if self.winner[i] > 0:
                head[i] = self.winner[i] - 1
            else:
                head[i] = self.winner[i]
            
            if self.winner[i] + 2 <= self.neural_num:
                tail[i] = self.winner[i] + 2
            else:
                tail[i] = self.winner[i] + 1

        for i in range(int(head[0]), int(tail[0])):
            for j in range(int(head[1]), int(tail[1])):
                temp = self.learning_rate * (d - self.nodes[i][j])
                self.nodes[i][j] += temp

    def fit(self):
        for iter in range(self.iter_num):
            for d in self.data:
                self.select_winner(d)
                self.update(d)

    def count(self):
        self.counts = np.zeros([self.neural_num, self.neural_num])
        for d in data:
            self.select_winner(d)
            self.counts[self.winner[0]][self.winner[1]] += 1

    def label_count(self):
        self.label_counts = np.zeros([self.class_num, self.neural_num, self.neural_num])
        for i, d in enumerate(data):
            self.select_winner(d)
            self.label_counts[labels[i]-1][self.winner[0]][self.winner[1]] += 1

#main
if __name__ == "__main__":
    #資料預處理
    feature_names = ['label','Alcohol', 'Malic acid','Ash','Alcalinity of ash' ,'Magnesium',
                    'Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins',
                    'Color intensity','Hue','OD280/OD315 of diluted wines','Proline' ]

    data = pd.read_csv("wine.txt", names=feature_names)
    data = data.sample(frac=1) 

    labels = data.iloc[:,0].values

    data = data.drop('label', axis=1)

    scaler = MinMaxScaler()
    data = scaler.fit_transform(data.iloc[:, :])
    #超參數設定
    neural_num = 10
    iter_num = 100
    learning_rate = 0.05
    test = SOFM(data, labels, neural_num, iter_num, learning_rate)
    #訓練
    test.fit()
    #標點
    test.count()
    print(test.counts)
    test.label_count()
    for i in range(test.class_num):
        print(test.label_counts[i])