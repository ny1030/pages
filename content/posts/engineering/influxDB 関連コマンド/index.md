---
date: 2022-08-24
title: influxDB 関連コマンド
---

- データベース作成
```bash
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE mydb"
```

- Smapleデータ書き込み
```bash
curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'
```

### 参考
[Write data with the InfluxDB API](https://docs.influxdata.com/influxdb/v1.8/guides/write_data/)
