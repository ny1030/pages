---
date: 2023-03-20
title: Microsoft SQL Serverのパフォーマンス解析
---

諸々の理由で業務システムのデータベース製品にSQL Serverを使っており、そこで問題が起きた際に解析できるようのメモ。

## RDS for SQL Server を使ってる場合

AWSのRDSでSQL Serverを使っている場合は、AWSネイティブの以下モニタリング機能を使うのがベター。

- 拡張モニタリング
	- CPU使用率の内訳が見れる（idleやsys, usrなど）
- Performance Insight
	- 時系列でロングランしているSQLや何で待機しているか等の情報が見れる

どちらもゼロダウンタイムで有効化ができる[^1]。
GCPやAzureは調べてないが、Azureは少なくとも同様のモニタリング機能があるのではと想定。

## 調査用のSQL

クラウド・オンプレ関わらず、SQL Serverにログインできるのであれば、以下クエリで各種調査を行う。

### 所要時間が大きい順のSQL
```sql
select top 100
    t1.total_elapsed_time / 1000 as "TotalElapsedTime(sec)"
    ,t1.execution_count as ExecCount
    ,t1.total_elapsed_time / t1.execution_count / 1000 as "AvgElapsedTime(sec)"
    ,t2.text as SQLtext
    ,t3.query_plan as SQLtext
from
    sys.dm_exec_query_stats as t1
    cross apply sys.dm_exec_sql_text(t1.sql_handle) as t2
    outer apply sys.dm_exec_query_plan(t2.plan_handle) as t3
order by
    "TotalElapsedTime(sec)" desc; 
```

### ページサイズ・断片化情報
テーブルやIndexのオブジェクトが肥大化・断片化しているか確認する
```sql
SELECT
    S.name AS 'schema name',
    O.name AS 'table name',
    IDX.name AS 'index name',
    IDXPS.avg_fragmentation_in_percent AS 'fragmentation(%)',
    IDXPS.page_count AS 'page count'
FROM
    sys.dm_db_index_physical_stats (DB_ID(),null,null,null,null) AS IDXPS
    LEFT OUTER JOIN  sys.objects AS O ON IDXPS.object_id = O.object_id
    LEFT OUTER JOIN  sys.schemas AS S ON O.schema_id = S.schema_id
    LEFT OUTER JOIN  sys.indexes AS IDX ON IDXPS.object_id = IDX.object_id  AND IDXPS.index_id = IDX.index_id
WHERE O.type = 'U'
AND   IDX.index_id > 0
ORDER BY
    IDXPS.avg_fragmentation_in_percent DESC
;
```

### CPU時間やIO回数
```sql
SELECT
    TOP 100
    t1.total_worker_time / t1.execution_count/ 1000 as "avg cputime(ms)",
    t1.max_worker_time /1000                         as "max cputime(ms)",
    t1.total_worker_time / 1000                      as "total cputime(ms)",
    t1.total_logical_reads / t1.execution_count      as "avg read count",
    t1.max_logical_reads                             as "max read count",
    t1.total_logical_reads                           as "total read count",
    t1.execution_count                               as "exec count",
    t2.text                                          as "sql text",
    t3.query_plan                                    as "query plan"
FROM
    sys.dm_exec_query_stats as t1
    cross apply sys.dm_exec_sql_text(t1.sql_handle) as t2
    outer apply sys.dm_exec_query_plan(t1.plan_handle) as t3
WHERE
    t2.text NOT LIKE '%dm_exec_query_stats%'
ORDER BY
    t1.total_worker_time DESC
;
```

[^1]: [DB インスタンスの設定](https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/Overview.DBInstance.Modifying.html#USER_ModifyInstance.Settings)
