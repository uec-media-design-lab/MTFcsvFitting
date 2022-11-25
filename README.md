# MTFcsvFitting

2ファイル(csv)同士を比較するコードです。

## 使い方
`XXX.py a.csv b.csv`


解析仮定では以下の仮定を置いてます

- csvファイルはMTFデータが格納されている
- アスペクト比が同じ
- レンズ焦点距離(fov)が同じ
- カメラから撮像面までの距離が同じ


## propertyies
`compare.py`の冒頭、main関数のtrimDataの引数が設定可能です

### 冒頭
カメラや画像サイズの設定を行います。

- `IMG_WIDTH_REAL`：実測データの画像解像度(横)`[pv]`
- `IMG_WIDTH_CG`：レンダリング結果の画像解像度(横)`[px]`
- `SENSOR_WIDTH`：撮像素子サイズ(横)`[mm]`
- `LENS_FOCUS_DISTANCE`：使用したレンズの焦点距離(CG、実測)`[mm]`、もしくはfovを焦点距離に換算したもの(CG)
- `CAM_TO_IMG_DISTANCE`：カメラから撮影対象までの距離`[mm]`


### trimData
第二引数に、**削除したい列**を配列として入力します。

ex) `data`から第二、第四列を消したい場合
`data = trimData(data, [1, 3])`

細かく取った実測データに対して粗くレンダリングして簡単に傾向を調べる場合、外れ値を除く場合、データ範囲を狭める場合などに使います。