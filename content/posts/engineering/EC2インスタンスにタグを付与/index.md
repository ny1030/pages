---
date: "2022-06-06"
title: EC2インスタンス/AMI/Snapshotにタグを付与
---

## 単発実行
### AMI
1. 現在のインスタンスのTagの状態を確認
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

### Snapshot
1. 現在のTagの状態を確認
	- snapshotIdをキーに確認する場合
	```
	VolumeId=$(aws ec2 describe-snapshots --snapshot-ids snap-xxxxxx | jq .Snapshots[].VolumeId | tr -d '"')
	aws ec2 describe-volumes --volume-ids $VolumeId
	```
	- AMIのImageIdをキーに確認する場合
	```
	SnapshotId=$(aws ec2 describe-images --image-ids ami-xxxxxxx | jq .Images[].BlockDeviceMappings[].Ebs.SnapshotId | tr -d '"')
	VolumeId=$(aws ec2 describe-snapshots --snapshot-ids ${SnapshotId} | jq .Snapshots[].VolumeId | tr -d '"')
	aws ec2 describe-volumes --volume-ids $VolumeId
	```

2. タグを付与
-> AMIと同じ。 `resource` に指定するIDをsnapshotIdにすればよい。

### Reference
[describe-instances — AWS CLI 1.25.2 Command Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)
[describe-images — AWS CLI 1.25.4 Command Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-images.html)
