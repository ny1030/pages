---
date: 2022-06-26
title: FlutterでiOSアプリをTestFlightでリリースする手順
---

### 前提
- Apple Developer アカウントは作成済み
- Xcodeをインストールした端末（MacBookなど）が手元にある

### [Xcode] Xcodeプロジェクトの設定
- `{project_root}/ios/Runner.xcodeproj` をXcodeで開き、Auto-Signningやアイコンの画像など諸々の設定を実施する。基本は以下のFlutterドキュメントに倣って設定すれば良い。
https://docs.flutter.dev/deployment/ios#review-xcode-project-settings

### [Flutter] ビルドの実施
- `{project_root}`で以下を実施する。
```
flutter clean
flutter build ipa
```
-> 上記の結果として、`build/ios/archive/Runner.xcarchive` が出力される。

### [Xcode] TestFlightに配信
- `build/ios/archive/Runner.xcarchive` をXcodeで開く
![](Pasted%20image%2020220626161832.png)
- Distribute App -> App Store Connect -> Upload を順にクリック
![](Pasted%20image%2020220626161901.png)
![](Pasted%20image%2020220626161948.png)
![](Pasted%20image%2020220626162003.png)
- 以下はデフォルトのままの設定にしている
![](Pasted%20image%2020220626162117.png)
![](Pasted%20image%2020220626162124.png)
- Review画面が出てくるので、確認しUploadをクリックし暫く待つ
![](Pasted%20image%2020220626162310.png)
### [Browser] TestFlightで任意のグループやユーザにアプリを配信
- https://appstoreconnect.apple.com/ を開き、My Apps -> Test Flightへ
- 以下のように +ボタンから任意のグループやユーザを追加する
![](Pasted%20image%2020220626163223.png)
-> 追加されると以下のようなメールが各ユーザに届くので、メールのLinkからアプリをDownloadする。
`{APP_NAME} for iOS is now available to test.`
