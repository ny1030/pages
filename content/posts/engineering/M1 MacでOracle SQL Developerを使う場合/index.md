---
date: 2023-02-15
title: M1 MacでOracle SQL Developerを使う場合
---

M1 MacBookProでOracle社のSQL Developerと呼ばれるSQLクライアント[^1]を使っていると、上手く出来なかったり、頻繁に異常終了することがある。

対処法として、 `arch` コマンドを使って起動することで、安定して利用できることを確認。

```
arch -x86_64 /Applications/SQLDeveloper.app/Contents/MacOS/sqldeveloper.sh
```

[^1]: [SQL Developer]()