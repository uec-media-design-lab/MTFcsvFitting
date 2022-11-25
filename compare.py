import numpy as np
import csv
import sys
import enum
IMG_WIDTH_REAL = 3012
IMG_WIDTH_CG   = 3012
SENSOR_WIDTH   = 35.9
LENS_FOCUS_DISTANCE = 35
CAM_TO_IMG_DISTANCE = 300
class ImgType(enum.IntEnum):
    REAL = 0
    CG = 1

# cycles/px -> lp/mm
def cpm2lppmm(x, type):
    return 1.0*x * (IMG_WIDTH_REAL if type==ImgType.REAL else IMG_WIDTH_CG) / (1.0* SENSOR_WIDTH * CAM_TO_IMG_DISTANCE / LENS_FOCUS_DISTANCE)

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
                # 最初1行は取り除く
                # firstRow=False
                continue
            ytmp = row
            ytmp = list(map(float, ytmp))
            y.append(ytmp)
            count += 1
            if idx>-1 and count == idx:
                # indexの個数分データとったので抜けだす
                break
    return y[1:]

def trimData(data, delArray):
    return np.delete(data, delArray, 1)
    
def compare(data1, data2):
    # 行列として与えられるデータをベクトル化
    vec1 = np.ravel(data1)
    vec2 = np.ravel(data2)
    n1 = vec1 / np.sqrt(np.sum(vec1**2))
    n2 = vec2 / np.sqrt(np.sum(vec2**2))
    return np.dot(n1, n2)

def compare_mean(data1, data2): # compareと結果同じ
    # それぞれの列に対して平均とって、結果をcompare
    means1 = np.mean(data1, axis=0)
    means2 = np.mean(data2, axis=0)
    return compare(means1, means2)

def main():
    # コマンドライン入力確認
    comparePath1 = sys.argv[1]
    comparePath2 = sys.argv[2]
    freq = float(sys.argv[3])
    
    # 特定frequencyまでのデータを取得
    data1 = getData(comparePath1, freq, ImgType.REAL)
    data2 = getData(comparePath2, freq, ImgType.CG)
    
    # print(data1)
    # print(data2)
    # print(np.array(data1).shape)
    # data1(real)から比較する部分だけトリミングする(疎にレンダリングしていた場合)
    # data1 = trimData(data1, [1, 3, 5, 7, 9, 10, 11, 12, 13])
    data1 = trimData(data1, [10,11,12,13,14])
    
    # print(np.array(data1).shape)
    # print(np.array(data2).shape)
    
    # 類似度計算
    similarity = compare(data1, data2)
    # similarity_mean = compare(data1, data2)
    print(similarity)
    # print(similarity_mean)    # 値同じ
    

if __name__ == "__main__":
    main()