---
date: 2022-11-09
title: AWS RDS/Aurora で 特定のインスタンスタイプがどのAZで使えるか調べる方法
---

## 背景

AWSのEC2やRDSを使用するにあたり、インスタンスタイプを選定した上で使っているが、最近リリースされた新しめのインスタンス（この記事の時点だとr6iとか）を使う場合、特定のリージョンやAZで使えない場合がある。

その場合の確認方法として、EC2であれば管理コンソールのEC2の画面から対応しているリージョン・AZを調べることが出来るが、RDSでは同様のインターフェースは現状提供されていない。

## 確認方法

### 対応リージョン

対応リージョンについては、管理コンソールから確認できないものの、価格票のページから同等の情報を確認することが可能 [^1] 
[^1]: https://aws.amazon.com/jp/rds/aurora/pricing/

ただし、AWS曰くまれに価格票が更新される際に使えるけど乗ってないケースがあるので、その際はリロードするなりしてくれとのこと。

### 対応AZ

対応しているリージョンが分かった後に、そのリージョンで対応しているAZ（Availability Zone）を調べる場合は CLIコマンド `describe-orderable-db-instance-options` で確認が可能である [^2]
[^2]: https://docs.aws.amazon.com/cli/latest/reference/rds/describe-orderable-db-instance-options.html

例として、TokyoリージョンのAurora for PostgreSQL 14.3 の r6i.large が使えるAZを確認するコマンドは以下の通りである。
```
$ aws rds describe-orderable-db-instance-options --region ap-northeast-1 --engine aurora-postgresql --engine-version 14.3 --db-instance-class db.r6i.large --query 'OrderableDBInstanceOptions[].{EngineVersion:EngineVersion,DBInstanceClass:DBInstanceClass,AvailabilityZones:AvailabilityZones}'
```

出力結果は以下の通り。1c は現状では使えないみたい。

```
[
    {
        "EngineVersion": "14.3",
        "DBInstanceClass": "db.r6i.large",
        "AvailabilityZones": [
            {
                "Name": "ap-northeast-1a"
            },
            {
                "Name": "ap-northeast-1d"
            }
        ]
    }
]
```
