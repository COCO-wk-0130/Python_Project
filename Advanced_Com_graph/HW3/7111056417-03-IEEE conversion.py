import struct
import os
 
getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]
 
def floatToBinary64(value):
    val = struct.unpack('Q', struct.pack('d', value))[0]
    return getBin(val)
 
def binaryToFloat(value):
    hx = hex(int(value, 2))   
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]

#main
while True:
    feature_list = os.listdir("./feature")
    print("Input the choice.")
    print("1:Decimal to IEEE-754")
    print("2:IEEE-755 to Decimal")
    print("3:Finish")
    Fnc = input()
    if Fnc == "1":
        for i in feature_list:
            if i[-7:-4] != "dec":
                continue
            with open("./feature/"+i) as file:
                values = []
                for lines in file:
                    values.append(float(lines))
            bins = []
            for j in values:
                bins.append(floatToBinary64(j))
            filename = "./feature/" + i[:-7] + "bin.csv"
            file = open(filename, "w")
            for j in bins:
                file.write(str(j)+"\n")
            file.close()
    elif Fnc == "2":
        for i in feature_list:
            if i[-7:-4] != "bin":
                continue
            with open("./feature/"+i) as file:
                values = []
                for lines in file:
                    values.append(str(lines[:-1]))
            decs = []
            for j in values:
                decs.append(binaryToFloat(j))
            filename = "./feature/" + i[:-7] + "dec.csv"
            file = open(filename, "w")
            for j in decs:
                file.write(str(round(j, 2))+"\n")
            file.close()
    else:
        break