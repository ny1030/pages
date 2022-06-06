### 単発実行

1. 現在の状態を確認
```
aws ec2 describe-images --image-ids ami-ffa5df99
```

2. タグを付与
```
aws ec2 create-tags --resources ami-ffa5df99 --tags Key=system_id,Value=599453524280/prd01-tky-NewUTME-frontapp-
```

⇨再度実行しても同じKey/Valueなら結果は変わらないことを確認

