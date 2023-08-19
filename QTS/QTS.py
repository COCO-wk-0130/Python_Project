import numpy as np
from numpy.random import default_rng

#二進位轉十進位
def bin2dec(bin):
    result = 0
    for i in range(len(bin)):
        result += pow(2, i) * bin[i]
    return result

#fitness的計算根據問題會不一樣，這裡使用ABS當範例
def fitness(QTS):
    for i in range(QTS.population_size):
        QTS.fitness[i] = 0
        for j in range(0, QTS.Qbit_num, 5):
            QTS.fitness[i] += bin2dec(QTS.Population[i][j:j+5])
            
class QTS:
    #初始化
    def __init__(self, population_size = 10, max_cycle = 100, Qbit_num = 10, theta = 0.01):
        self.population_size = population_size
        self.max_cycle = max_cycle
        self.Qbit_num = Qbit_num
        self.theta = theta
        self.Population = np.zeros((population_size, Qbit_num))
        self.Q_matrix = [0.5 for i in range(Qbit_num)]
        self.fitness = [None for i in range(population_size)]
        self.best_index = -1
        self.worst_index = -1
        self.best = [None for i in range(Qbit_num)]
        self.dice = default_rng(722)
    
    #設定旋轉角度
    def set_theta(self, new_theta):
        self.theta = new_theta
    
    #生成新的Population
    def generate_new_population(self):
        for i in range(self.population_size):
            self.Population[i] = self.dice.random(self.Qbit_num)
            self.Population[i] = np.where(self.Population[i] > self.Q_matrix, 1, 0)
    
    #找出最佳及最差的粒子(min為最佳)
    def selection_find_min(self):
        self.best_index = self.fitness.index(min(self.fitness))
        self.worst_index = self.fitness.index(max(self.fitness))
        if self.best[-1] == None:
            self.best = self.Population[self.best_index]
            self.best = np.append(self.best, min(self.fitness))
        elif min(self.fitness) < self.best[-1]:
            self.best = self.Population[self.best_index]
            self.best = np.append(self.best, min(self.fitness))
    
    #找出最佳及最差的粒子(max為最佳)
    def selection_find_max(self):
        self.best_index = self.fitness.index(max(self.fitness))
        self.worst_index =self.fitness.index(min(self.fitness))
        if self.best[-1] == None:
            self.best = self.Population[self.best_index]
            self.best = np.append(self.best, max(self.fitness))
        elif max(self.fitness) > self.best[-1]:
            self.best = self.Population[self.best_index]
            self.best = np.append(self.best, max(self.fitness))
    
    #更新Qmatrix
    def update(self):
        for i in range(self.Qbit_num):
            if self.Population[self.best_index][i] != self.Population[self.worst_index][i]:
                if self.Population[self.best_index][i] == 1:
                    self.Q_matrix[i] -= self.theta
                else:
                    self.Q_matrix[i] += self.theta
                    
    #更新Qmatrix, Gbest
    def update_G(self):
        for i in range(self.Qbit_num):
            if self.best[i] != self.Population[self.worst_index][i]:
                if self.best[i] == 1:
                    self.Q_matrix[i] -= self.theta
                else:
                    self.Q_matrix[i] += self.theta
    
    #簡易測試
    def run(self):
        for i in range(self.max_cycle):
            self.generate_new_population()
            fitness(self)
            self.selection_find_min()
            self.update()
            print(self.best[-1])
            