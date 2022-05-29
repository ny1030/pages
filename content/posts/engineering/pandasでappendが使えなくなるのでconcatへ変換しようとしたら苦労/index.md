---
date: "2022-05-29"
title: pandasでappendが使えなくなるのでconcatへ変換しようとしたら苦労
draft: true
---

pythonのバージョンをアップデートしたらpythonのスクリプトで以下のWARNが出るようになった。

```
FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
```

### やったこと
concatの使い方を調べて、appendを使っている該当箇所で以下のような書き換えをおこなった。
```
df1.append(df2)
```
↓
```
pd.concat([df1, df2])
```
しかし、このスクリプトから出力されるCSVファイルを開くと
```
number,name,date,uid,0
,,,,1
,,,,NameA
,,,,2022/05/29(日) 20:21:56.66
,,,,ID:AAAAA
```
のようになっており、列の名前や行の内容が崩れてしまうようになってしまった。
連結しているdf1,df2のshapeを調べてみる。
```
code:
print(df1.shape,df2.shape)

output:
(0,4) (4,)
```
補足：(0,4)は0行, 4列を表す。
次にappendとconcatで結合した後のshapeを比較してみた。
```
code:
print(df_append.shape,df_concat.shape)

output:
(1,4) (5,5)
```
たしかに後者のshapeはカラム数が増えたりしているので、CSVのフォーマットも崩れている。