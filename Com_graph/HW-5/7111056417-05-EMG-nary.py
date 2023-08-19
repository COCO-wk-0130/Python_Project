from math import*
import random
import numpy as np
import cv2
import os

#依照n, pixel_num隨機生成訊息
def message_generation(n, pixel_num, dimension):
    #計算要嵌入的訊息長度
    #像素數量除以n向下取整，保證所有訊息都可以被嵌入
    #再乘上欲嵌入圖像之維度
    length = pixel_num // n * dimension
    #隨機生成長度為length的2*n+1進制訊息
    message = [random.randint(0, 2*n) for i in range(length)]
    return message

#EMD, 嵌入順序為RGB, 輸入圖片為RGB
def EMD_RGB(n, img_rgb):
    Nary = n*2+1
    img_shape = np.shape(img_rgb)
    pixel_num = img_shape[0]*img_shape[1]
    dimension = img_shape[2]
    message = message_generation(n, pixel_num, dimension)
    img_flat = img_rgb.reshape(pixel_num, dimension)
    msg_num = len(message)
    msg_per_field = msg_num // dimension
    for i in range(msg_num):
        f = 0
        for j in range(n):
            f += img_flat[(i % msg_per_field)*n + j][i // msg_per_field]*(j+1)
        f %= Nary
        s = (message[i] - f) % Nary
        if s == 0:
            continue
        while (True):
            if (s <= n):
                if img_flat[(i % msg_per_field)*n + s - 1][i // msg_per_field] == 255:
                    img_flat[(i % msg_per_field)*n + s - 1][i // msg_per_field] -= 1
                else:
                    img_flat[(i % msg_per_field)*n + s-1][i // msg_per_field] += 1
                    break
            else:
                if img_flat[(i % msg_per_field)*n + Nary - s - 1][i // msg_per_field] == 0:
                    img_flat[(i % msg_per_field)*n + Nary - s - 1][i // msg_per_field] += 1
                else:
                    img_flat[(i % msg_per_field)*n + Nary-s-1][i // msg_per_field] -= 1
                    break
            f = 0
            for j in range(n):
                f += img_flat[(i % msg_per_field)*n + j][i // msg_per_field]*(j+1)
            f %= Nary
            s = (message[i] - f) % Nary
                
    result_img_rgb = img_flat.reshape(img_shape[0], img_shape[1], img_shape[2])
    #message是用來驗證的
    return result_img_rgb, message

#解出嵌入的訊息
def Un_EMD_RGB(n, img_rgb):
    Nary = 2*n + 1
    img_shape = np.shape(img_rgb)
    pixel_num = img_shape[0]*img_shape[1]
    dimension = img_shape[2]
    rebuild_message = []
    msg_per_field = pixel_num // n
    img_flat = img_rgb.reshape(pixel_num, dimension)
    for i in range(msg_per_field * dimension):
        f = 0
        for j in range(n):
            f += img_flat[(i % msg_per_field)*n + j][i // msg_per_field]*(j+1)
        f %= Nary
        rebuild_message.append(f)
    return rebuild_message

#比較是否相同
def Checker(Unembed_MSG, MSG):
    for i in range(len(MSG)):
        if(Unembed_MSG[i] != MSG[i]):
            return False
    return True

#main
random.seed(2022)
n = 5
img_name = "kodim07"
img_bgr = cv2.imread(".\\Source\\"+img_name + ".png")

#Convert BGR and RGB
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
result_img_rgb, message = EMD_RGB(n, img_rgb)
result_img_bgr = cv2.cvtColor(result_img_rgb, cv2.COLOR_RGB2BGR)
cv2.imwrite(".\\stego\\" + img_name + "_stego_EMD" + str(n) + ".png", result_img_bgr)

#Check the message is right
Unembed_MSG = Un_EMD_RGB(n, result_img_rgb)
if(Checker(Unembed_MSG, message)):
    print(True)
else:
    print(False)