---
date: "2022-06-06"
title: EC2インスタンスにタグを付与
---

### 単発実行

1. 現在のインスタンスの状態を確認
```
aws ec2 describe-images --image-ids ami-xxxxxx
```

2. タグを付与(例としてsystem : front というTagを付与する)
```
aws ec2 create-tags --resources ami-ffa5df99 --tags Key=system,Value=front
```

⇨再度実行しても同じKey/Valueなら結果は変わらないことを確認

3. `system`のタグが付いてるリソースを列挙
```
aws ec2 describe-images --filter Name="tag-key",Values="system"
```

### Reference
[describe-instances — AWS CLI 1.25.2 Command Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)
