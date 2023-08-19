import cv2
import numpy as np
from math import*
from skimage.metrics import structural_similarity
import matplotlib.pyplot as plt
import os

#已使用HW-02在coltra生成以下圖片
#01_kodim05_kodim06.png
#02_kodim07_kodim08.png
#03_kodim09_kodim10.png

#寫入Mean/STD資料
def write_mean_std(img_name, file):
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
    for i in range(2, -1, -1):
        file.write(str(round(img_mean[i], 2))+'\n')
    for i in range(2, -1, -1):
        file.write(str(round(img_std[i], 2))+'\n')
        
def info2list_BGR(info):
    #order：BGR
    info = [float(i) for i in info[0:12]]
    return info[2::-1], info[5:2:-1], info[8:5:-1], info[11:8:-1]
        
        
#還原原始圖片
def img_reverse(img_path, rev_info):
    img = cv2.imread(img_path)
    img_shape = np.shape(img)
    rev_img = np.zeros(img_shape[0]*img_shape[1]*3)
    rev_img = rev_img.reshape(img_shape[0], img_shape[1], 3)
    #分類rev_info
    source_mean, source_std, target_mean, target_std = info2list_BGR(rev_info)
    #img reverse
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            for k in range(3):
                rev_img[i][j][k] = round((source_std[k]/target_std[k])*(img[i][j][k]-target_mean[k])+source_mean[k])
                #將範圍維持在(0, 255)
                if rev_img[i][j][k] < 0:
                    rev_img[i][j][k] = 0
                elif rev_img[i][j][k] > 255:
                    rev_img[i][j][k] = 255
    return rev_img

#將BGR拆開來
def img2BGR(img):
    img_shape = np.shape(img)
    img_R = np.zeros(img_shape[0]*img_shape[1])
    img_R = img_R.reshape(img_shape[0], img_shape[1])
    img_G = np.zeros(img_shape[0]*img_shape[1])
    img_G = img_G.reshape(img_shape[0], img_shape[1])
    img_B = np.zeros(img_shape[0]*img_shape[1])
    img_B = img_B.reshape(img_shape[0], img_shape[1])
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            for k in range(3):
                if k == 0:
                    img_B[i][j] = img[i][j][k]
                elif k == 1:
                    img_G[i][j] = img[i][j][k]
                else:
                    img_R[i][j] = img[i][j][k]
    return img_B, img_G, img_R

#計算MSE, PSNR, SSIM
def Cal_MSE_PSNR_SSIM(source_path, revfct_path):
    source_img = cv2.imread(source_path)
    revfct_img = cv2.imread(revfct_path)
    img_shape = np.shape(source_img)
    MSE = [0, 0, 0]
    PSNR = [0, 0, 0]
    SSIM = [0, 0, 0]
    #Calcuate MSE, BGR
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            for k in range(3):
                #防止overflow, opencv的矩陣超過[0, 255]就會overflow
                if source_img[i][j][k] > revfct_img[i][j][k]:
                    MSE[k] += source_img[i][j][k]-revfct_img[i][j][k]
                else:
                    MSE[k] += revfct_img[i][j][k]-source_img[i][j][k]
    pixel_num = img_shape[0]*img_shape[1]
    MSE = [round(i/pixel_num, 2) for i in MSE]
    #Calcuate PSNR, BGR
    for i in range(3):
        PSNR[i] = round(10*log((255*255)/MSE[i], 10), 2)
    #Calcuate SSIM, BGR
    source_B, source_G, source_R = img2BGR(source_img)
    revfct_B, revfct_G, revfct_R = img2BGR(revfct_img)
    SSIM[0] = round(structural_similarity(source_B, revfct_B), 6)
    SSIM[1] = round(structural_similarity(source_G, revfct_G), 6)
    SSIM[2] = round(structural_similarity(source_R, revfct_R), 6)
    return MSE, PSNR, SSIM

#將資料寫入文件
def write_MSE_PSNR_SSIM(MSE, PSNR, SSIM, path):
    file = open(path, 'w')
    #BGR to RGB
    for i in range(2, -1, -1):
        file.write(str(MSE[i])+" "+str(PSNR[i])+" "+str(SSIM[i])+"\n")
    file.close()
    
#謝入reverse所需的資料
#寫入01_kodim05_kodim06.txt
file = open("./sideinfodeci/01_kodim05_kodim06.txt", 'w')
#source
source_path = "./source/"+"kodim05.png"
write_mean_std(source_path, file)
#target
target_path = "./target/"+"kodim06.png"
write_mean_std(target_path, file)
file.close()

#寫入02_kodim07_kodim08.txt
file = open("./sideinfodeci/02_kodim07_kodim08.txt", 'w')
#source
source_path = "./source/"+"kodim07.png"
write_mean_std(source_path, file)
#target
target_path = "./target/"+"kodim08.png"
write_mean_std(target_path, file)
file.close()

#寫入03_kodim09_kodim10.txt
file = open("./sideinfodeci/03_kodim09_kodim10.txt", 'w')
#source
source_path = "./source/"+"kodim09.png"
write_mean_std(source_path, file)
#target
target_path = "./target/"+"kodim10.png"
write_mean_std(target_path, file)
file.close()

#img_reverse
#Reverse 01_kodim05_kodim06.png
#read info.
rev_info_path = "./sideinfodeci/01_kodim05_kodim06.txt"
file = open(rev_info_path, "r")
rev_info = file.read().split("\n")
#reverse
img_path = "./coltra/01_kodim05_kodim06.png"
rev_img = img_reverse(img_path, rev_info)
#save rev_img
result_path = "./revfct/01_kodim05_revfct.png"
cv2.imwrite(result_path, rev_img)

source_path = "./source/kodim05.png"
MSE, PSNR, SSIM = Cal_MSE_PSNR_SSIM(source_path, result_path)
file_path = "./revfct/01_kodim05_revfct.txt"
write_MSE_PSNR_SSIM(MSE, PSNR, SSIM, file_path)

#Reverse 01_kodim07_kodim08.png
#read info.
rev_info_path = "./sideinfodeci/02_kodim07_kodim08.txt"
file = open(rev_info_path, "r")
rev_info = file.read().split("\n")
#reverse
img_path = "./coltra/02_kodim07_kodim08.png"
rev_img = img_reverse(img_path, rev_info)
#save rev_img
result_path = "./revfct/02_kodim07_revfct.png"
cv2.imwrite(result_path, rev_img)

source_path = "./source/kodim07.png"
MSE, PSNR, SSIM = Cal_MSE_PSNR_SSIM(source_path, result_path)
file_path = "./revfct/02_kodim07_revfct.txt"
write_MSE_PSNR_SSIM(MSE, PSNR, SSIM, file_path)

#Reverse 01_kodim09_kodim10.png
#read info.
rev_info_path = "./sideinfodeci/03_kodim09_kodim10.txt"
file = open(rev_info_path, "r")
rev_info = file.read().split("\n")
#reverse
img_path = "./coltra/03_kodim09_kodim10.png"
rev_img = img_reverse(img_path, rev_info)
#save rev_img
result_path = "./revfct/03_kodim09_revfct.png"
cv2.imwrite(result_path, rev_img)

source_path = "./source/kodim09.png"
MSE, PSNR, SSIM = Cal_MSE_PSNR_SSIM(source_path, result_path)
file_path = "./revfct/03_kodim09_revfct.txt"
write_MSE_PSNR_SSIM(MSE, PSNR, SSIM, file_path)
