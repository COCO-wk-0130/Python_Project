#Binary search Force Method
import cv2
import numpy as np
import os

#"算"出mean, std
def mean_std(img):
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
        
def cal_hist_dis(img1, img2):
    hist_dis = []
    for i in range(3):
        hist1 = cv2.calcHist([img1], [i], None, [256], [0, 256])
        hist1 = cv2.normalize(hist1, hist1)
        hist2 = cv2.calcHist([img2], [i], None, [256], [0, 256])
        hist2 = cv2.normalize(hist2, hist2)
        hist_dis.append(cv2.compareHist(hist1, hist2, cv2.HISTCMP_HELLINGER))
    return hist_dis

#執行顏色轉換
def weighted_color_tranfer(target_img, source_img, BGR_weight = [1, 1, 1], target_mean=0, target_std=0, source_mean=0, source_std=0):
    if target_mean == 0:
        target_mean, target_std = mean_std(target_img)
        source_mean, source_std = mean_std(source_img)
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
    result_img = result_img.astype("uint8")
    return result_img

def Cal_opt_weights_Bin(target_img, source_img):
    target_mean, target_std = mean_std(target_img)
    source_mean, source_std = mean_std(source_img)
    
    head = [0, 0, 0]
    tail = [1, 1, 1]
    
    head_img = weighted_color_tranfer(target_img, source_img, head, target_mean, target_std, source_mean, source_std)
    tail_img = weighted_color_tranfer(target_img, source_img, tail, target_mean, target_std, source_mean, source_std)
    
    head_source_dis = cal_hist_dis(head_img, source_img)
    head_target_dis = cal_hist_dis(head_img, target_img)
    head_hist_dis = [abs(head_source_dis[k]-head_target_dis[k]) for k in range(3)]
    tail_source_dis = cal_hist_dis(tail_img, source_img)
    tail_target_dis = cal_hist_dis(tail_img, target_img)
    tail_hist_dis = [abs(tail_source_dis[k]-tail_target_dis[k]) for k in range(3)]
    
    for N in range(15):
        mid = [(head[i] + tail[i])/2 for i in range(3)]
        mid_img = weighted_color_tranfer(target_img, source_img, mid, target_mean, target_std, source_mean, source_std)
        mid_source_dis = cal_hist_dis(mid_img, source_img)
        mid_target_dis = cal_hist_dis(mid_img, target_img)
        mid_hist_dis = [abs(mid_source_dis[k]-mid_target_dis[k]) for k in range(3)] 
        #update tail and head
        for i in range(3):
            if tail_hist_dis[i] > head_hist_dis[i]:
                tail_hist_dis[i] = mid_hist_dis[i]
                tail[i] = mid[i]
            else:
                head_hist_dis[i] = mid_hist_dis[i]
                head[i] = mid[i]
    best_weights = []
    for i in range(3):
        best_weights.append(min(tail[i], mid[i], head[i]))
    return mid

#main:
while True:
    target = input("Imput the target image.")
    source = input("Input the source image.")
    target_path = "./target/"+target+".png"
    source_path = "./source/"+source+".png"
    target_img = cv2.imread(target_path)
    source_img = cv2.imread(source_path)
    weights = Cal_opt_weights_Bin(target_img, source_img)
    img = weighted_color_tranfer(target_img, source_img, weights)
    cv2.imwrite(f"./result/WCT0{i+1}-Bin-{round(weights[0], 4)}-{round(weights[1], 4)}-{round(weights[2], 4)}.png", img)#x
