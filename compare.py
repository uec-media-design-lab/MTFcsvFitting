import numpy as np
import csv
import sys
import enum
IMG_WIDTH_REAL = 3012
IMG_WIDTH_CG   = 1506 
SENSOR_WIDTH   = 35.9
LENS_FOCUS_DISTANCE = 35
CAM_TO_IMG_DISTANCE = 300
class ImgType(enum.IntEnum):
    REAL = 0
    CG = 1

# cycles/px -> lp/mm
def cpm2lppmm(x, type):
    return 1.0*x * (IMG_WIDTH_REAL if type==ImgType.REAL else IMG_WIDTH_CG) / (1.0* SENSOR_WIDTH * CAM_TO_IMG_DISTANCE / LENS_FOCUS_DISTANCE)
    

def main():
    # コマンドライン入力確認
    comparePath1 = sys.argv[1]
    comparePath2 = sys.argv[2]
    freq = float(sys.argv[3])
    
    # 特定frequencyまでのデータを取得
    data1 = getData(comparePath1, freq)
    data2 = getData(comparePath1, freq)
    
    # data1(real)から比較する部分だけトリミングする(疎にレンダリングしていた場合)
    data1 = trimData(data1)
    
    # 類似度計算
    similarity = compare(data1, data2)
    print(similarity)

if __name__ == "__main__":
    main()