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

![](Pasted%20image%2020230803183023.png)

- 案内の通り、Chrome拡張機能をインストール
https://chrome.google.com/webstore/detail/former2-helper/fhejmeojlbhfhjndnkkleooeejklmigi

- 解析対象のリソースがあるAWSのクレデンシャルを入力

![](Pasted%20image%2020230803184247.png)

- Cloud Formation のパラメータを入力、とりあえずはここは未設定

![](Pasted%20image%2020230803184418.png)

- 最後にここの画面の緑色の Scan ボタンを押すとスキャンが始まる、不足している権限があると都度ポップアップで表示される。
- また右上にリージョンの設定があり、デフォルトではバージニア北部になっているので要確認。

![](Pasted%20image%2020230803184741.png)

- スキャンの途中でサイドバーからRDSを見てみると

**すげえ！！ちゃんと表示されてる。**
Describeの内容を表示してるだけなんだけど、自分の手元でこうやって一覧を見れるのはテンションが上がる。

![](Pasted%20image%2020230803185550.png)

### 気になったところ

#### スキャンする際に全てのリソースがスキャンされるのか？
全てをスキャンするのは便利であるものの、自身のM1 MacBookProだと、10分経過したあたりでブラウザが一度ハングした。全てスキャンした後の画面ではフィルタの機能などはあるのはわかるが、スキャンする前に特定のリソースをスキャンできないのか？

調べた＆使ってみた結果、出来なさそう。なのでリソースが沢山ある場合はスキャンに数時間かかることと、キャッシュされてない状態で開いた際にリソース情報のロードに時間を要することは念頭に置いて使った方がいい。

#### スキャンした情報は永続化できる？
Dockerプロセスを停止=>起動して試したが、スキャンした情報は残ってたので永続化はされてそう。ただし、Former2起動直後はリソース情報をロード中で、何も出てこないように見えるので注意。

### テンプレート作成可能なリソースタイプ
EC2やRDSなど基本的なサービスは対応しているが、以下のダッシュボードから確認した限りだとSecurity Groupなどは作成できない。
SecurityGroupに色んなルールを追加している場合は移行がめんどかったりするので、痒い所に手が届かない感じはする。

自分はChatGPTの力を借りて、SecurityGroupのルールを別アカウントに移行してくれるPythonスクリプトを作成した。

```python:migrateSG.py
import boto3
from dotenv import load_dotenv
import botocore
import os

# .envファイルから環境変数を読み込む
load_dotenv()
source_account_access_key = os.getenv("SOURCE_ACCESS_KEY")
source_account_secret_key = os.getenv("SOURCE_SECRET_KEY")
dest_account_access_key = os.getenv("DEST_ACCESS_KEY")
dest_account_secret_key = os.getenv("DEST_SECRET_KEY")

# INPUT情報
source_security_group_id = 'sg-xxxxx'
source_region = 'ap-northeast-1'
dest_security_group_name = 'security-group-sample'
dest_security_group_description = 'Created by SDK'
dest_region = 'ap-northeast-1'
dest_vpc_id = 'vpc-xxxxxxx'

# 元のアカウントからSecurity Group情報を取得
source_ec2 = boto3.client('ec2', aws_access_key_id=source_account_access_key, aws_secret_access_key=source_account_secret_key, region_name=source_region)
response = source_ec2.describe_security_groups(GroupIds=[source_security_group_id])
source_security_group_info = response['SecurityGroups'][0]
# 目的のアカウントでSecurity Groupを作成
dest_ec2 = boto3.client('ec2', aws_access_key_id=dest_account_access_key, aws_secret_access_key=dest_account_secret_key, region_name=dest_region)
response = dest_ec2.create_security_group(
    GroupName=dest_security_group_name,
    Description=dest_security_group_description,
    VpcId=dest_vpc_id
)

for rule in source_security_group_info['IpPermissions']:
    modified_rule = rule.copy()  # ルールをコピーして編集
    if 'UserIdGroupPairs' in modified_rule:
        # 移行先に存在しないセキュリティグループを除外する
        modified_rule['UserIdGroupPairs'] = [
            pair for pair in modified_rule['UserIdGroupPairs']
            if pair.get('GroupId') == response['GroupId']  # 移行先セキュリティグループに対するルールのみ残す
        ]
    try:
        if modified_rule.get('IpRanges') or modified_rule.get('Ipv6Ranges') or modified_rule.get('UserIdGroupPairs'):
            # ルールに許可するエントリが存在する場合のみ処理を実行
            dest_ec2.authorize_security_group_ingress(
                GroupId=response['GroupId'],
                IpPermissions=[modified_rule]
            )
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'InvalidPermission.Duplicate':
            print("Rule already exists in the destination security group. Skipping.")
        elif error_code == 'DependencyViolation':
            print("Dependency violation. Skipping rule with source SG:", modified_rule.get('UserIdGroupPairs'))
        else:
            print("Error:", e.response['Error']['Message'])

print("Security Group migration completed.")
```