from math import gcd
import numpy as np
import cv2
import os

class NEAT_3D:
    def __init__(self, img, b_xyz = [1, 1, 1], r_xyz = [1, 1, 1], L=5):
        self.b_xyz = b_xyz
        self.r_xyz = r_xyz
        self.M = img.shape[0]
        self.N = img.shape[1]
        self.img = img
        self.L = L

        if img.shape[2] == 1:
            self.K = 8
        else:
            self.K = 24
        
        self.GCD_NM = gcd(self.N,self.M)
        self.GCD_MK = gcd(self.M,self.K)
        self.GCD_KN = gcd(self.K,self.N)
            
        self.c_xyz = [int(r_xyz[0]*(self.K/self.GCD_MK)), 
                      int(r_xyz[1]*(self.N/self.GCD_KN)), 
                      int(r_xyz[2]*(self.M/self.GCD_NM))]

        self.S_x = [[1, 0, 0], 
                    [0, 1, self.b_xyz[0]], 
                    [0, self.c_xyz[0], 1+self.b_xyz[0]*self.c_xyz[0]]]

        self.S_y = [[1+self.b_xyz[1]*self.c_xyz[1], 0, self.c_xyz[1]], 
                    [0, 1, 0], 
                    [self.b_xyz[1], 0, 1]]

        self.S_z = [[1, self.b_xyz[2], 0], 
                    [self.c_xyz[2], 1+self.b_xyz[2]*self.c_xyz[2], 0], 
                    [0, 0, 1]]

    def encrypt(self):
        enc_img = np.zeros([self.M, self.N, self.K], "uint8")

        img_bits = np.unpackbits(self.img, axis=2)
        for _ in range(self.L):
            for n in range(self.N):
                for m in range(self.M):
                    for k in range(self.K):
                        #z
                        temp = np.matmul(self.S_z, [n, m, k])
                        temp[0] %= self.N
                        temp[1] %= self.M
                        temp[2] %= self.K

                        #x
                        temp = np.matmul(self.S_x, temp)
                        temp[0] %= self.N
                        temp[1] %= self.M
                        temp[2] %= self.K

                        #y
                        temp = np.matmul(self.S_y, temp)
                        temp[0] %= self.N
                        temp[1] %= self.M
                        temp[2] %= self.K

                        enc_img[temp[1]][temp[0]][temp[2]] = img_bits[m][n][k]
        enc_img = np.packbits(enc_img, axis=2)
        return enc_img

    def decrypt(self):
        dec_img = np.zeros([self.M, self.N, self.K], "uint8")

        img_bits = np.unpackbits(self.img, axis=2)
        temp = [0, 0, 0]
        for _ in range(self.L):
            for n in range(self.N):
                for m in range(self.M):
                    for k in range(self.K):
                        #y^-1
                        temp[0] = (n - self.c_xyz[1] * k) % self.N
                        temp[1] = m
                        temp[2] = (k - self.b_xyz[1] * temp[0]) % self.K

                        #x^-1
                        temp[2] = (temp[2] - self.c_xyz[0] * temp[1]) % self.K
                        temp[1] = (temp[1] - self.b_xyz[0] * temp[2]) % self.M

                        #z^-1
                        temp[1] = (temp[1] - self.c_xyz[2] * temp[0]) % self.M
                        temp[0] = (temp[0] - self.b_xyz[2] * temp[1]) % self.N
                        
                        dec_img[temp[1]][temp[0]][temp[2]] = img_bits[m][n][k]
                        
        dec_img = np.packbits(dec_img, axis=2)

        return dec_img

    def img_type(self):
        threshold = 3 #根據input image做調整
        img = self.img.astype(np.float32)
        b, g, r = cv2.split(img)
        x = np.sum(img, axis=2)/3
        area_s = img.shape[0] * img.shape[1]
        r_gray = abs(r-x)
        g_gray = abs(g-x)
        b_gray = abs(b-x)
        r_avg = np.sum(r_gray) / area_s
        g_avg = np.sum(g_gray) / area_s
        b_avg = np.sum(b_gray) / area_s
        gray_degree = np.average([r_avg, g_avg, b_avg])
        if gray_degree < threshold:
            return "Gray"
        else:
            return "BGR"
    
    def write_parameter(self, file_name):
        file_path = "./parame/{}_parameter.txt".format(file_name)
        f = open(file_path, 'w')
        f.write("N = {}\n".format(self.N))
        f.write("M = {}\n".format(self.M))
        f.write("K = {}\n".format(self.K))

        f.write("gcd(N, M) = {}\n".format(self.GCD_NM))
        f.write("gcd(M, K) = {}\n".format(self.GCD_MK))
        f.write("gcd(K, N) = {}\n".format(self.GCD_KN))

        f.write("b_x = {}\n".format(self.b_xyz[0]))
        f.write("b_y = {}\n".format(self.b_xyz[1]))
        f.write("b_z = {}\n".format(self.b_xyz[2]))

        f.write("r_x = {}\n".format(self.r_xyz[0]))
        f.write("r_y = {}\n".format(self.r_xyz[1]))
        f.write("r_z = {}\n".format(self.r_xyz[2]))

        f.write("c_x = {}\n".format(self.c_xyz[0]))
        f.write("c_y = {}\n".format(self.c_xyz[1]))
        f.write("c_z = {}\n".format(self.c_xyz[2]))

        f.write("S_x = {}\t{}\t{}\n".format(self.S_x[0][0], self.S_x[0][1], self.S_x[0][2]))
        f.write("\t  {}\t{}\t{}\n".format(self.S_x[1][0], self.S_x[1][1], self.S_x[1][2]))
        f.write("\t  {}\t{}\t{}\n".format(self.S_x[2][0], self.S_x[2][1], self.S_x[2][2]))

        f.write("S_y = {}\n".format(self.S_y[0]))
        f.write("\t  {}\n".format(self.S_y[1]))
        f.write("\t  {}\n".format(self.S_y[2]))

        f.write("S_z = {}\n".format(self.S_z[0]))
        f.write("\t  {}\n".format(self.S_z[1]))
        f.write("\t  {}\n".format(self.S_z[2]))

        f.close()

#main
if __name__ == "__main__":
    for img_name in os.listdir("./encrypt"):
        enc_img = cv2.imread("./encrypt/"+img_name)
        dec_N3 = NEAT_3D(enc_img)
        dec_img = dec_N3.decrypt()
        cv2.imwrite("./decrypt/{}_dec.png".format(img_name[:-8]), dec_img)
