---
date: 2022-06-21
title: RDS CLI
---

- インスタンス情報をCSV出力（ヘッダなし）
```
aws rds describe-db-instances --query "DBInstances[].[DBInstanceIdentifier,DBInstanceClass,Engine,EngineVersion]" | jq -r ".[] | @csv" > rds_describe-db-instances.csv
```

- インスタンス情報をCSV出力（ヘッダあり）
```
aws rds describe-db-instances --query "DBInstances[].[DBInstanceIdentifier,DBInstanceClass,Engine,EngineVersion]" | jq -r '["DBInstanceIdentifier","DBInstanceClass","Engine","EngineVersion"],(.[])|@csv' > rds_describe-db-instances_with-header.csv
```