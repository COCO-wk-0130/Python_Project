使用的函示庫：math, os, numpy, cv2
加密與解密使用的是相同的class(NEAT_3D)，NEAT_3D包含的功能如下：
__init__(img, b_xyz=[1, 1, 1], r_xyz=[1, 1, 1], L=5)：參數初始化，創建時會自動執行。
encrypt()：將輸入的圖片進行加密並回傳(BRG)。
decrypt()：將輸入的無片進行解密並回傳(BRG)。
img_type()：回傳輸入的圖片為"Gray"會"BRG"。
write_parameter(file_name)：將輸入的參數寫成txt檔，檔名為{file_name}_parameter.txt
注：img_type()是回傳三維的圖片是否為黑白，而不是判斷圖片是否為灰階的。

範例使用os.listdir列出目標資料夾內的所有圖片，並依序執行加解密。