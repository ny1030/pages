---
date: 2022-06-23
title: MySQL, MaridDBでスロークエリを出力する設定
---

## 1. 記録するログファイルを作成
今回は例として、 `/tmp`  に`slow.log` を作成し、このファイルにスロークエリを記録するようにする。
- ファイル作成&権限付与：
```bash
touch /tmp/slow.log
sudo chown mysql:mysql -R /tmp/slow.log
```
- 権限確認
```bash
ls -l

output:
-rw-r--r-- 1 mysql mysql  451 Jun 22 17:21 slow.log
```
-> ownerがmysqlになっている

## 2. スロークエリを出力する設定を有効化
MySQLの設定ファイルである `my.cnf` にスロークエリを出力する設定を入れる。今回は５秒以上のクエリを出力する。
`/etc/my.cnf` にあるファイルを開き、以下を記載：
```
[mysqld]
...
long_query_time=5
slow_query_log_file=/tmp/slow.log
slow_query_log=1
...
```
記載できたらMySQLを再起動
```
service restart mysqld
```
## 3.確認
MySQLにログインし、以下のクエリを実行
```
SELECT SLEEP(5);
```
`/tmp/slow.log`を確認すると、無事にスロークエリとして出力されていた。
```
...
# Time: 220622 17:21:43
# User@Host: root[root] @ localhost []
# Thread_id: 118  Schema:   QC_hit: No
# Query_time: 5.000241  Lock_time: 0.000000  Rows_sent: 1  Rows_examined: 0
# Rows_affected: 0  Bytes_sent: 63
SET timestamp=1655918503;
SELECT SLEEP(5);
...
```
