---
date: 2022-09-07
title: AWS CLI Snapshot Commands
---

- 特定のvolumeIdのSnapshot一覧を確認したい時
	- 取得日時が新しい順に表示されてそう
```
aws ec2 describe-snapshots --filters Name="volume-id,Values=${volume}"
```
[describe-snapshots — AWS CLI 2.7.29 Command Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-snapshots.html)

