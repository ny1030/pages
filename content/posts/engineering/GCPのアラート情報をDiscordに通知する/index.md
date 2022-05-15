---
date: "2022-05-15"
title: GCPのアラート情報をDiscordに通知する
---

## やりたいこと
- 運用しているシステムで時折、CPU使用率が100%を超過しアクセス不可になる。
- Compute Engine（GCE）のインスタンスを再起動することで上記事象は直るので、復旧時間を短くするために、通知することでできるだけ早く気付けるようにする。
- 通知先として、スマホから手軽に見れてWebhookで楽に設定できるDiscordを使ってみる。
- 通知のロジックを超カンタンな図で表すと以下のような形：
![](Pasted%20image%2020220515184502.png)

## やったこと
### 通知ポリシーの作成（GCP管理画面）
GCEのCPU使用率が95%以上の状態が何分間以上続いたら通知するか、といった条件をGCPの管理画面から設定する。これはGCEの画面のオブザーバビリティのタブから画像のように設定。
![](Pasted%20image%2020220515184226.png)

### 通知チャンネルの作成（GCP管理画面）
通知ポリシーと似た名前だがこちらは通知先を設定するサービス。画像の通りSlackやWebhook、（見えてないけど）SMSやEmailの設定が可能。今回はDiscordに通知したかったので通知したいDiscordチャンネルのWebhook URLを設定。
![](Pasted%20image%2020220515184245.png)

### トラブルシューティング
上記の設定を終えたところで、通知チャンネルから「TEST CONNECTION」があったので試しに実行。
![](Pasted%20image%2020220515184302.png)
「successfully sent」と出ているがDiscordチャンネルを見るとメッセージが届いてない。。

#### GCP側のログ確認
Cloud Logging で 確認したところ、同タイミングで400エラーが出ていることを確認 😇
![](Pasted%20image%2020220515184321.png)

#### curlで送ってみる
件のDiscordにcurlで試しにPOSTをしてみたところ、
```
$ curl -H 'Content-Type: application/json' -d '{"data": "Hello World"}' https://discord.com/api/webhooks/{YOUR_PATH}

{"message": "Cannot send an empty message", "code": 50006}
```
というメッセージが返ってきた。status codeを調べると400なのでGCPと同じエラーっぽい。

微修正して以下のようなPOSTをしたところ通知が成功。
```
$ curl -H 'Content-Type: application/json' -d '{"content": "Hello World"}' https://discord.com/api/webhooks/{YOUR_PATH}
```
どうやらdiscordではJSONのpayloadに設定する key が "content" じゃないとエラーになる模様。なのでGCPではおそらく、content以外の key名を設定していてエラーが返ってきている？

#### 最終的にCloud Function で実装
以上のような経緯でWebhookで単純に送ることはできなかったため、同じような人がいないか調べたところ Cloud Functions で自前で作るのが良いとのこと。以下のような手順でCloud Functionsで実装を試してみた。

1. Cloud Pub/Subのトピックを作成
2. 通知チャンネルで通知先に Cloud Pub/Sub -> 上記トピックを選択
3. Cloud Functionsを作成
	- トリガーのタイプ：Cloud Pub/Sub
	- ランタイム：Nodejs
	- ソースは以下の通り

```
const { IncomingWebhook } = require('@slack/webhook');
/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event Event payload.
 * @param {!Object} context Metadata for the event.
 */
exports.notify = (event, context) => {
  const message = event.data
    ? Buffer.from(event.data, 'base64').toString()
    : 'Hello, World';
  console.log(message);

  const body = {
      "content": message
    };
    // discordに通知
    const webhook = new IncomingWebhook('https://discord.com/api/webhooks/{YOUR_PATH}');
    //await webhook.send(body);
    webhook.send(body);
  return 'Discord notification sent successfully';
};
```
package.json
```
{
  "name": "sample-pubsub",
  "version": "0.0.1",
  "dependencies": {
    "@google-cloud/pubsub": "^0.18.0",
    "@slack/webhook": "^6.1.0"
  }
}
```

このFunctionをDeployして、再度テストしたところ無事に送信されたことを確認
![](Pasted%20image%2020220515184342.png)
