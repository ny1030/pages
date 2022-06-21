---
date: "2022-06-15"
title: nodejsでCSVファイルを作成する
---

## CSVファイルを読み込む
```JavaScript
let datas = fs.readFileSync('data/chart/1m_' + code + '.csv').toString().split("\r\n");
```


