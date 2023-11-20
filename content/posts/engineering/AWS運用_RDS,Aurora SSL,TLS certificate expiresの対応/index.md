---
date: 2023-11-20
title: AWS運用_RDS,Aurora SSL,TLS certificate expiresの対応
tags:
  - AWS
  - Operation
---
# 概要
AWS RDS/Auroraを利用しており、クライアントがSSL/TLSを使って接続している場合、Amazon RDS 認証局証明書（rds-ca-2019）の更新が2024/08までに必要。
[(AWS Document) SSL/TLS 証明書のローテーション](https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL-certificate-rotation.html)

# 対象の調査

## 対象となるRDSの列挙
[RDS_特定の認証局証明書を利用しているインスタンスの列挙](../AWS%20CLI%20スニペット集/index.md#RDS_特定の認証局証明書を利用しているインスタンスの列挙) のコマンドで対象インスタンスを調べる
上記結果で、rds-ca-2019を利用しているものが更新が必要。また、更新可能な証明書は [RDS_利用可能な認証局証明書の確認（RDS for PostgreSQL）](../AWS%20CLI%20スニペット集/index.md#RDS_利用可能な認証局証明書の確認（RDS for PostgreSQL）) のように確認できる
## SSL/TLSを利用しているか調査
[(AWS Document) PostgreSQL DB インスタンスで SSL を使用する](https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html)
まずはRDS側でSSL接続を利用しているかどうかは `rds.force_ssl` で確認可能
```bash
$ aws rds describe-db-cluster-parameters  --db-cluster-parameter-group-name default.aurora-postgresql13 | jq '.Parameters[] | select(.ParameterName == "rds.force_ssl")'
```
出力例： ParameterValueが0のため、SSLは必須ではない。SSL接続が確立できない場合はSSL接続が利用されない。
```json
{
  "ParameterName": "rds.force_ssl",
  "ParameterValue": "0",
  "Description": "Force SSL connections.",
  "Source": "system",
  ...
}
```

