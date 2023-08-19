import cv2
import numpy as np
from math import*
import matplotlib.pyplot as plt
import os

#印出mean, std
def write_mean_std(img_name):
    img = cv2.imread(img_name)
    img_shape = np.shape(img)
    #[B,G,R]
    img_mean = [0, 0, 0]
    img_std = [0, 0, 0]
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            for k in range(3):
                img_mean[k] += img[i][j][k]
    #every element in list divide 512*512
    img_mean[:] = [x/(img_shape[0]*img_shape[1]) for x in img_mean]
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            for k in range(3):
                img_std[k] += pow(img[i][j][k]-img_mean[k], 2)
    img_std[:] = [sqrt(x/(img_shape[0]*img_shape[1])) for x in img_std]
    file = open("./result/"+img_name[9:-4]+'-mean-std.csv', 'w')
    file.write(str(img_mean[2])+","+str(img_mean[1])+","+str(img_mean[0])+'\n')
    file.write(str(img_std[2])+","+str(img_std[1])+","+str(img_std[0])+'\n')
    file.close()

#"算"出mean, std
def mean_std(img_name):
    img = cv2.imread(img_name)
    img_shape = np.shape(img)
    #[B,G,R]
    img_mean = [0, 0, 0]
    img_std = [0, 0, 0]
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            for k in range(3):
                img_mean[k] += img[i][j][k]
    #every element in list divide 512*512
    img_mean[:] = [x/(img_shape[0]*img_shape[1]) for x in img_mean]
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            for k in range(3):
                img_std[k] += pow(img[i][j][k]-img_mean[k], 2)
    return img_mean, img_std

#印出his
def his(img_name):
    BGR = []
    BGR.append([0 for i in range(256)])
    BGR.append([0 for i in range(256)])
    BGR.append([0 for i in range(256)])
    img = cv2.imread(img_name)
    img_shape = np.shape(img)
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            for k in range(3):
                BGR[k][img[i][j][k]]+=1
    file = open("./result/"+img_name[9:-4]+'-his.csv', 'w')
    for i in range(256):
        file.write(str(BGR[2][i])+","+str(BGR[1][i])+","+str(BGR[0][i])+"\n")
    file.close()
    x = [i for i in range(256)]
    plt.bar(x, BGR[2], color = "r")
    plt.title(img_name+"_Red_HIS")
    plt.show()
    plt.bar(x, BGR[1], color = "g")
    plt.title(img_name+"_Green_HIS")
    plt.show()
    plt.bar(x, BGR[0], color = "b")
    plt.title(img_name+"_Blue_HIS")
    plt.show()

#執行顏色轉換
def weighted_color_tranfer(target_path, source_path, BGR_weight = [1, 1, 1]):
    target_mean, target_std = mean_std(target_path)
    source_mean, source_std = mean_std(source_path)
    source_img = cv2.imread(source_path)
    source_shape = np.shape(source_img)
    result_img = np.zeros(source_shape[0]*source_shape[1]*3)
    result_img = result_img.reshape(source_shape[0], source_shape[1], 3)
    for i in range(source_shape[0]):
        for j in range(source_shape[1]):
            for k in range(3):
                result_img[i][j][k] = round(((target_std[k]*BGR_weight[k] + source_std[k]*(1-BGR_weight[k]))/source_std[k])*(source_img[i][j][k]-source_mean[k]) + target_mean[k]*BGR_weight[k] + source_mean[k]*(1-BGR_weight[k]))
                #將範圍維持在(0, 255)
                if result_img[i][j][k] < 0:
                    result_img[i][j][k] = 0
                elif result_img[i][j][k] > 255:
                    result_img[i][j][k] = 255
    return result_img

#印出圖片
def print_img(img):
    cv2.imshow("img", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

#main

while(True):
    target = input("Imput the target image.")
    source = input("Input the source image.")
    B_weight = input("Input the Blue domain weight.[0, 1]")
    G_weight = input("Input the Green domain weight.[0, 1]")
    R_weight = input("Input the Red domain weight.[0, 1]")
    target_path = "./target/"+target+".png"
    source_path = "./source/"+source+".png"
    result_path = './result/01_' + source + '_' + target + '.png'
    weight = [float(B_weight), float(G_weight), float(R_weight)]
    result_img = weighted_color_tranfer(target_path, source_path, weight)
    cv2.imwrite(result_path, result_img)