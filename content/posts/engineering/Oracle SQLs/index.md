### 一般用途
- {USER_NAME } というユーザのオブジェクト権限確認
```
SELECT grantee, table_name, privilege FROM dba_tab_privs WHERE grantee = 'USER_NAME';
```
- 初期化パラメータの一覧
```
SELECT name,display_value,default_value,isdefault,description FROM V$PARAMETER;
```

### 特定用途
- 気になるパラメータチェック
```
SELECT name,display_value,default_value,isdefault,description FROM V$PARAMETER WHERE name IN ('client_statistics_level') OR name like '_optim%';
```