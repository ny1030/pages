---
date: "2023-08-03"
title: AWSリソースの移行をFormer2で実施
---

# Background
本番環境だけ作っていたシステムがあり、DBMSなどの大幅なバージョンアップを計画しており、流石にテストが必要ということで、検証環境を別AWSアカウントに作ることになった。
EC2, RDSなどのリソースしかない簡単なスタックだが、SGの設定なども移行するとなると割と面倒なので、既存のリソースを使った方法で楽に作れないかを模索。

以下のFormer2という既存のリソースからCloudFormationやTerraformのコードを生成するツールがあることを発見。
[https://github.com/iann0036/former2](https://github.com/iann0036/former2)

## Former2の使用
以下のWebサイトで自身のAWSアカウントのクレデンシャルなどを登録すると、SDK APIでリソースを解析してテンプレートを生成してくれる模様
[https://former2.com/#](https://former2.com/#)

ただ、流石に上記のサイトにクレデンシャルを登録するのは気が引けるので、Dockerを利用してスタンドアロンでFormer2を使う方法を試した。

### Former2（スタンドアロン版）の使い方

- 以下リポジトリをクローンする
[https://github.com/iann0036/former2](https://github.com/iann0036/former2)

- rootディレクトリで `docker compose up -d` でビルドおよび起動をする

- 127.0.0.1 をブラウザで開くと、Former2が表示される

![](../../../Pasted%20image%2020230803183023.png)

