import numpy as np
import pandas as pd
from math import*
from sklearn.preprocessing import StandardScaler #標準化
from scipy import stats

class Bayes:
    def __init__(self, training_data, labels):
        self.training_data = training_data
        self.labels = labels
        self.classes = np.unique(labels)
        self.class_num = len(self.classes)
        self.feature_num = training_data.shape[1]
        self.means = np.zeros([self.class_num, self.feature_num])
        self.variances = np.zeros([self.class_num, self.feature_num])
        self.covariances = np.zeros([self.class_num, self.feature_num, self.feature_num])
        self.priors = [0 for _ in range(self.class_num)]

    def fit(self):
        #calculate priors, means, variances
        for i, c in enumerate(self.classes):
            data_class = self.training_data[self.labels == c]
            self.priors[i] = len(data_class) / len(self.training_data)
            self.means[i] = np.mean(data_class, axis=0)
            self.variances[i] = np.var(data_class, axis=0) + 1e-10
            self.covariances[i] = np.cov(data_class, rowvar=False) + 1e-10 * np.eye(self.feature_num)
    
    def predict(self, testing_data):
        likelihood = np.zeros([len(testing_data), self.class_num])

        for i, c in enumerate(self.classes):
            class_likelihood = stats.norm.pdf(testing_data, loc=self.means[i], scale=np.sqrt(self.variances[i]))
            class_likelihood = np.prod(class_likelihood, axis=1)
            likelihood[:, i] = class_likelihood * self.priors[i]
        return self.classes[np.argmax(likelihood, axis=1)]

    def score(self, testing_data, testing_labels):
        pre_labels = self.predict(testing_data)
        return np.sum([pre_labels[i] == testing_labels[i] for i in range(len(testing_data))]) / len(testing_data)
    
    def bayes_error(self):
        Opt_s = np.zeros([self.class_num, self.class_num])
        Bayes_errors = [[float('-inf') for _ in range(self.class_num)] for _ in range(self.class_num)]
        for i in range(self.class_num):
            for j in range(i+1, self.class_num):
                delta = self.means[j] - self.means[i]
                for s in np.linspace(0, 1, 50):

                    sigma = s * self.covariances[i] + (1-s) * self.covariances[j]
                    sigma_inv = np.linalg.pinv(sigma)

                    error = (((s * (1-s)) / 2) * np.matmul(np.matmul(delta.T, sigma_inv), delta) + 0.5 * np.log(np.linalg.det(sigma) / 
                            pow(np.linalg.det(self.covariances[i]), s) * pow(np.linalg.det(self.covariances[j]), (1-s))))
                    if error > Bayes_errors[i][j]:
                        Bayes_errors[i][j] = error
                        Opt_s[i][j] = round(s, 4)
                #計算錯誤率
                Bayes_errors[i][j] = round(exp(-Bayes_errors[i][j]), 2)

        return Opt_s, Bayes_errors
        
#main
scores = []
for _ in range(10):
    #read data and data preprocessing
    feature_names = ['label','Alcohol', 'Malic acid','Ash','Alcalinity of ash' ,'Magnesium',
                    'Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins',
                    'Color intensity','Hue','OD280/OD315 of diluted wines','Proline' ]

    data = pd.read_csv("wine.txt", names=feature_names)
    data = data.sample(frac=1) 

    half = int(len(data) * 0.5)
    train_data=data.iloc[:half]
    test_data=data.iloc[half:]

    train_labels = train_data.iloc[:,0].values
    test_labels = test_data.iloc[:,0].values

    train_data = train_data.drop('label', axis=1)
    test_data = test_data.drop('label', axis=1)

    scaler = StandardScaler()
    train_data = scaler.fit_transform(train_data.iloc[:, :])
    test_data  = scaler.transform(test_data.iloc[:, :])
    #fit
    test = Bayes(train_data, train_labels)
    test.fit()
    pred = test.predict(test_data)
    score = test.score(test_data, test_labels)
    scores.append(round(score*100, 2))
    for i in range(test.class_num):
        for j in range(i+1, test.class_num):
            print(f"{i} 與 {j} 的 Chernoff bound 為 {S[i][j]}", end=" ")
            print(f"Bayes Error 為 {Bayes_errors[i][j]}%")
    print("")