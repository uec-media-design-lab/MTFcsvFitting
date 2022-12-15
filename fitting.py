import os
import re
import numpy as np
import csv
import sys
import math
import enum

IMG_WIDTH_REAL = 3012
IMG_WIDTH_CG   = 1200
SENSOR_WIDTH   = 35.9
LENS_FOCUS_DISTANCE = 35
CAM_TO_IMG_DISTANCE = 300
USINGREALDATA = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
class ImgType(enum.IntEnum):
    REAL = 0
    CG = 1
SUFF = "/exr/Result_csv/all.csv"
FREQ = 1

# cycles/px -> lp/mm
def cpm2lppmm(x, type):
    return 1.0*x * (IMG_WIDTH_REAL if type==ImgType.REAL else IMG_WIDTH_CG) / (1.0* SENSOR_WIDTH * CAM_TO_IMG_DISTANCE / LENS_FOCUS_DISTANCE)

def n(data):
    return np.array(data).size

def ME(data1, data2):
    return np.sum(data2-data1)/n(data1)

def MAE(data1, data2):
    return np.absolute(data2-data1).sum() / n(data1)

def RMSE(data1, data2):
    return math.sqrt( np.sum(data2-data1)**2 /  n(data1))

def MPE(data1, data2):
    return np.sum((data2-data1)/data1) / n(data1)
    
def MAPE(data1, data2):
    return np.absolute((data2-data1)/data1).sum() / n(data1)

def RMSPE(data1, data2):
    return math.sqrt(np.sum((data2-data1)/data1)**2 / n(data1))

def getData(path, freq, ImgType):
    idx = -1
    f = np.linspace(0, 1, 1024)
    f_lpmm = cpm2lppmm(f, ImgType)
    for i in range(len(f_lpmm)):
        if f_lpmm[i]>freq:
                idx = i
                break
    
    y = [[]]
    count = 0
    
    with open(path, 'r') as f:
        csvreader = csv.reader(f)
        firstRow = False
        for row in csvreader:
            if firstRow:
                continue
            ytmp = row
            ytmp = list(map(float, ytmp))
            y.append(ytmp)
            count += 1
            if idx>-1 and count == idx:
                # indexの個数分データとったので抜けだす
                break
    return y[1:]

def extractData(data, ext):
    return np.array(data)[np.ix_(list(range(np.array(data).shape[0])), ext)]

def getDataList(folder_path):
    folder_list = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    
    a_surface = []
    a_back = []
    data_list= []
    for f in folder_list:
        pattern = ".*-as(.*)-ai(.*)-.*"
        a_surface.append(re.search(pattern, f).group(1))
        a_back.append(re.search(pattern, f).group(2))
        data_list = getData(folder_path+f+SUFF, FREQ, ImgType.CG)
        
    return data_list, a_surface, a_back

def fitMTF(realData, dataList, a_surface, a_back):
    res_mpe = []
    res_mape = []
    res_rmspe = []
    for i in range(len(a_surface)):
        res_mpe.append(MPE(realData, dataList[i]))
        res_mape.append(MAPE(realData, dataList[i]))
        res_rmspe.append(RMSPE(realData, dataList[i]))
    
    # それぞれの最小値とインデックス
    min_mpe_idx, min_mpe = min(enumerate(res_mpe), key=lambda x: x[1])
    min_mape_idx, min_mape = min(enumerate(res_mape), key=lambda x: x[1])
    min_rmspe_idx, min_rmspe = min(enumerate(res_rmspe), key=lambda x: x[1])
    
    # 出力
    print("="*20+" RESULT "+"="*20)
    # print("[MPE]\taS:{}".format(a_surface[min_mpe_idx]))
    print("[MPE]\taS:{}\taI:{}\terr:{:.4f}".format(a_surface[min_mpe_idx], a_back[min_mpe_idx], min_mpe))
    print("[MAPE]\taS:{}\taI:{}\terr:{:.4f}".format(a_surface[min_mape_idx], a_back[min_mape_idx], min_mape))
    print("[RMSPE]\taS:{}\taI:{}\terr:{:.4f}".format(a_surface[min_rmspe_idx], a_back[min_rmspe_idx], min_rmspe))
    
def main():
    realDataPath = sys.argv[1]
    fitFolderPath = sys.argv[2]
    
    data_real = getData(realDataPath, FREQ, ImgType.REAL)
    data_real = extractData(data_real, USINGREALDATA)
    data, surf, back = getDataList(fitFolderPath)
    fitMTF(data_real, data, surf, back)


if __name__ == "__main__":
    main()