---
date: "2022-05-18"
title: AWS ECR Commands
---
- apple というECRリポジトリの developタグの imageDigest を確認
```
aws ecr describe-images --repository-name apple --image-ids imageTag=develop | jq .imageDetails[].imageDigest
```

- 認証後にPull (AWSアカウントIDは12345678とする)
```
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 12345678.dkr.ecr.ap-northeast-1.amazonaws.com
```

TODO: 
- スニペット化
