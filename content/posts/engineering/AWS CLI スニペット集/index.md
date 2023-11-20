---
date: 2023-11-20
title: AWS CLI スニペット集
tags:
  - AWS
  - Snippet
---
# ユースケース別

## Operation（運用）

### RDS_特定の認証局証明書を利用しているインスタンスの列挙
```bash
WIP
```
### RDS_利用可能な認証局証明書の確認（RDS for PostgreSQL）
- 結果が大量にあるため、下記例では `--engine` で RDS for PostgreSQL のみに絞っている
```bash
aws rds describe-db-engine-versions --engine postgres | jq -r '.DBEngineVersions[] | [.Engine, .EngineVersion, .SupportedCACertificateIdentifiers] | @csv '
```
