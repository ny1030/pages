---
date: "2022-05-18"
title: AWS-CLI ECR Commands
---
### imageDigest を確認
- e.g. apple というECRリポジトリの developタグ
```
aws ecr describe-images --repository-name apple --image-ids imageTag=develop | jq .imageDetails[].imageDigest
```

### イメージのPull
#### 1. 認証
```
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 12345678.dkr.ecr.ap-northeast-1.amazonaws.com
```
##### 補足
- AWSアカウントIDは例として12345678とする
- ECRの接続情報はFQDNまたはURL（htttps://~）どちらの表記でも上手くいった。
- `--region` で指定するリージョンは、ECRリポジトリと同じリージョンにする（us-east-1では無いので注意）
- `ecr:GetAuthorizationToken` のRoleが必要なので事前に権限付与しておく
##### TroubleShooting
以下のエラーが出る場合がある
```
Error saving credentials: error storing credentials - err: exit status 1, out: `Post "http://ipc/registry/credstore-updated": dial unix Library/Containers/com.docker.docker/Data/backend.sock: connect: connection refused`
```
[Qiitaの記事](https://qiita.com/P2eFR6RU/items/180d6de4c52f36b7adc0) を参考に、`$HOME/.docker/config.json` の `credsStore` の項目を削除することでエラーが消えることを確認（ただし、あくまで応急的な対応）

#### 2. Pull
`docker pull 12345678.dkr.ecr.ap-northeast-1.amazonaws.com/{repository_name}/{image_name}:{tag_name}`
↓
`docker images` でPullできたことを確認

##### 補足
- `ecr:BatchGetImage` のRoleが必要