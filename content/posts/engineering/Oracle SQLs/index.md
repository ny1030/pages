---
date: "2022-05-17"
title: Oracle SQLs
---
### 一般用途
- {USER_NAME } というユーザのオブジェクト権限確認
```
SELECT grantee, table_name, privilege FROM dba_tab_privs WHERE grantee = 'USER_NAME';
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

### 特定用途
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

TODO: 
- スニペット化