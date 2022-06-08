---
date: "2022-06-06"
title: EC2インスタンス/AMIにタグを付与
---

### 単発実行

1. 現在のインスタンスの状態を確認
```
aws ec2 describe-images --image-ids ami-xxxxxx
```

2. タグを付与(例として `system:front` というTagを付与する)
```
aws ec2 create-tags --resources ami-ffa5df99 --tags Key=system,Value=front
```

⇨再度実行しても同じKey/Valueなら結果は変わらないことを確認

3. `system`のタグが付いてるリソースを列挙
```
aws ec2 describe-images --filter Name="tag-key",Values="system"
```
- ワイルドカードによる検索も可能
```
aws ec2 describe-images --filter Name="tag-key",Values="sys*"
```

### Reference
[describe-instances — AWS CLI 1.25.2 Command Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)
[describe-images — AWS CLI 1.25.4 Command Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-images.html)
