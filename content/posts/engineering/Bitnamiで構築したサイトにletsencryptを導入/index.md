---
date: 2022-08-21
title: Bitnamiで構築したサイトにletsencryptを導入する手順
---

参考：[Generate And Install A Let's Encrypt SSL Certificate For A Bitnami Application](https://docs.bitnami.com/aws/how-to/generate-install-lets-encrypt-ssl/)

基本は以下のbitnami提供のToolを実行するだけでOK

```
sudo /opt/bitnami/bncert-tool
```

対話形式で以下の事項が聞かれるので回答
- サイトのドメイン名
	- このタイミングでAレコードに上記ドメイン <-> 当該ホストのIP が設定されてないと、名前解決できないというエラーが出るので事前にDNSレコード（Aレコード）を設定しておくのがベター
- wwwドメインを設定するか
- メールアドレス
- 最終確認