---
date: "2022-05-21"
title: JSONで定義したURLの置換ルールをPythonで変換する
---

## 概要

ApacheやNginx、ELBのアクセスログの集計などをする時に以下のような変換を行う必要がある。

Input: 
```
timestamp,backend_processing_time_msec,alb_status_code,backend_status_code,target_status_code_list,method,URL
2021-12-01T03:50:00.115676Z,182,201,201,201,POST,https://api.test.io:443/service1/v2/jp/cart/7219b08ec8464865a6020bb6025cd641/details
2021-12-01T03:50:20.597508Z,67,200,200,200,GET,https://api.test.io:443/service2/v2/jp/history/0130050002112010350-8052922
2021-12-01T03:50:20.613452Z,145,200,200,200,GET,https://api.test.io:443/service2/v2/jp/history?display_results=5&search_page=1
2021-12-01T03:50:20.894114Z,22,200,200,200,GET,https://api.test.io:443/service2/v2/jp/history/0130050002112010350-8052921
2021-12-01T03:51:45.903017Z,8,404,404,404,DELETE,https://api.test.io:443/service3/v1/jp/reserve/7041b995fa1b4c8b99543acc50c60865
2021-12-01T03:54:41.598315Z,20,200,200,200,GET,https://api.test.io:443/service3/v1/jp/stocks?code_list=11111111%22222222%33333333
2021-12-01T03:54:56.672346Z,165,200,200,200,GET,https://api.test.io:443/service4/v1/jp/pay/accesstoken?device_id=AAAAA-BBBB-CCC
```

⬇️ URLの正規化（≒変換, 名寄せ）

Output: 
```
timestamp,backend_processing_time_msec,alb_status_code,backend_status_code,method,URL
2021-12-01T03:50:00.115676Z,182.0,201,201,POST,https://api.test.io:443/service1/v2/jp/cart/{cart_no}/details
2021-12-01T03:50:20.597508Z,67.0,200,200,GET,https://api.test.io:443/service2/v2/jp/history/{order_no}
2021-12-01T03:50:20.613452Z,145.0,200,200,GET,https://api.test.io:443/service2/v2/jp/history
2021-12-01T03:50:20.894114Z,22.0,200,200,GET,https://api.test.io:443/service2/v2/jp/history/{order_no}
2021-12-01T03:51:45.903017Z,8.0,404,404,DELETE,https://api.test.io:443/service3/v1/jp/reserve/{cart_no}
2021-12-01T03:54:41.598315Z,20.0,200,200,GET,https://api.test.io:443/service3/v1/jp/stocks
2021-12-01T03:54:56.672346Z,165.0,200,200,GET,https://api.test.io:443/service4/v1/jp/pay/accesstoken
```

上記のような変換を行うことで、APIのEndpointごとにコール回数やレスポンス時間など統計処理をPandasなどを行うことができる。

## コード
概要で説明したような事を実現するために、以下のコードを作成。

### 1. URLの変換パターンを定義した設定ファイル（JSON）
- 置換のパターンはAPIの定義書などを参考に記述するのが良い（ない場合はアクセスログからリバースするしかない...）
```json:replace-pattern.json
{
	"^(.*)/history/[0-9]{12,19}-[0-9]{5,7}": "\\1/history/{order_no}",
	"^(.*)(cart|reserve)/[0-9a-z]{32}": "\\1\\2/{cart_no}"
}
```

### 2. inputしたCSVからURLの変換処理を行うスクリプト（Python）
- タイトル詐欺になるが、クエリパラメータに関する置換はルールが単純なのでJSONでは定義せず、こちらのスクリプトで定義・処理している（# REMOVE QUERY PARAMETERのセクション）。
```python:test.py
import pandas as pd
import json

input_filename = './input.csv'
output_filename = './output.csv'

input_csv = pd.read_csv(
    input_filename,
    sep=',',
    usecols=lambda x: x in ['timestamp','alb_status_code', 'backend_status_code', 'method', 'URL', 'backend_processing_time_msec'],
    index_col='timestamp',
    dtype={'timestamp': str, 'alb_status_code': str, 'backend_status_code': str, 'method': str, 'URL': str, 'backend_processing_time_msec': 'float16'}
)

# REMOVE QUERY PARAMETER
input_csv = pd.concat([input_csv, input_csv["URL"].str.extract(r'([^\?]+).*', expand=True)], axis=1, ignore_index=False)
input_csv = input_csv.drop(columns=["URL"])
input_csv.rename(columns={0: 'URL'}, inplace=True)

# REPLACE ID IN URL TEXT FOR AGGREGATION
with open('./replace-pattern.json') as f:
    dct = json.load(f)
input_csv["URL"] = input_csv["URL"].replace(dct, regex=True)

# Output to CSV
input_csv.to_csv(output_filename, header=True, index=True)
exit
```

`python test.py` 実行することで概要通りの csvに変換されることを確認。