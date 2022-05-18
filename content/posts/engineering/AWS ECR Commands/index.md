---
date: "2022-05-18"
title: AWS ECR Commands
---
- apple というECRリポジトリの developタグの imageDigest を確認
```
aws ecr describe-images --repository-name apple --image-ids imageTag=develop | jq .imageDetails[].imageDigest
```

TODO: 
- スニペット化
