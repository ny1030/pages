---
date: "2023-01-23"
title: Oracle SQLs
---
### General Use
- {USER_NAME } というユーザのオブジェクト権限確認
```
SELECT grantee, table_name, privilege FROM dba_tab_privs WHERE grantee = 'USER_NAME';
```
- SYSDBA権限をもつユーザ確認
```
SELECT * FROM V$PWFILE_USERS;
```
- 初期化パラメータの一覧
```
SELECT name,display_value,default_value,isdefault,description FROM V$PARAMETER;
```
- 隠しパラメータを調べる
```
select ksppinm as "parameter",
	   ksppstvl as "value"
from x$ksppi join x$ksppcv using (indx)
where ksppinm = '{隠しパラメータ名}';
```

- アクセスできるテーブル一覧
```
SELECT * FROM ALL_TABLES ORDER BY OWNER,TABLE_NAME;
```

### Specific Use
#### Parameter
- 気になるパラメータチェック
```
SELECT name,display_value,default_value,isdefault,description FROM V$PARAMETER WHERE name IN ('client_statistics_level') OR name like '_optim%';
```
- 気になる隠しパラメータ
```
select ksppinm as "parameter",
	   ksppstvl as "value"
from x$ksppi join x$ksppcv using (indx)
where ksppinm IN ('_optimizer_use_stats_on_conventional_dml','_optimizer_gather_stats_on_conventional_dml');
```
#### SQL Tuning
- 特定のSQL_IDの**Actual**の実行計画を確認する
```
SHOW parameter statistics_level;でstatistics_levelがtypicalの場合：
　- ALTER SESSION SET statistics_level=all;
　- <<対象のSQLを実行>>

SELECT * FROM table(DBMS_XPLAN.DISPLAY_CURSOR(`上記で実行したSQLのSQL_ID`, format=>``'ALL ALLSTATS LAST'``));
```
補足：
-  `statistics_level`　をALLに変えてから SQLを再実行するのが重要
- SQLを再実行する際に、全く同じテキストだとSQL_IDが変わらず `statistics_level = typical` の情報しか得られないのでコメントを入れるなどして別のSQLとして認識させることでActualの情報が取れる
- 最後のSQLを実行した際に、A-Rows, A-Timeのカラムが表示されていればActualの情報が取れている。

- 実行したSQLのSQL_IDを調べる
	SQL文にコメントを入れて `v$sql` から探す
```
SELECT * FROM AREA WHERE STORE = '117666' /* FINDME */; -- Sample SQL to find
SELECT SQL_ID,FIRST_LOAD_TIME,SQL_TEXT FROM v$sql WHERE SQL_TEXT LIKE '%FINDME%';
```
	実行された時刻（FIRST_LOAD_TIME）を使って `v$sql` から探す
```
SELECT SQL_ID,FIRST_LOAD_TIME,SQL_TEXT FROM v$sql ORDER BY FIRST_LOAD_TIME DESC;
```
