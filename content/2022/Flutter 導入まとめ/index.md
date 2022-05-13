---
date: "2021-12-15"
title: Flutter 導入まとめ
---

## １．環境セットアップ（２時間くらい）

### Flutter

１．SDKのダウンロード・解凍

[Install](https://flutter.dev/docs/get-started/install)

２．PATH設定

以下をPATHに追加（ホームディレクトリの名前は適宜変更する）

```jsx
/Users/{username}/flutter/bin
```

３．確認

以下のコマンドが実行できることを確認する

```jsx
flutter
```

### Android

１．Android Studioダウンロード⇛インストール

[Install](https://developer.android.com/studio?hl=ja&gclid=CjwKCAjw8KmLBhB8EiwAQbqNoJ6FGOMXbFIo4QDZVpbigkO_VdXJgy_zTpzITT4qJhhk4w2z8mEmVxoCoV0QAvD_BwE&gclsrc=aw.ds)

２．確認

```jsx
flutter doctor
```

※最初は５分くらい時間かかる

の結果でAndroid Studioがチェックマーク入ってるのを確認
![[Pasted image 20220513215817.png]]

４．Andoroid toolchainのエラー解消

・Command-Line Toolsのインストール（AndoroidSDKの設定画面からできる）

![[Pasted image 20220513215852.png]]

・Andoroidライセンスの許可

```jsx
flutter doctor --android-licenses
```

※ javaのPATH通ってないとエラー出る

５．Android toolchainがチェックついてることを確認

```jsx
flutter doctor
```

![[Pasted image 20220513215916.png]]

６．FlutterプラグインをAndoroid Studioからインストール

![[Pasted image 20220513215944.png]]

### XCode（iOS）

１．XCodeをインストール

２．Cocoapodをインストール

```jsx
brew install cocoapods
brew link --overwrite cocoapods
```

※バージョン指定している理由はエラー回避しようとした結果

３．XCodeにチェックがついてることを確認

```jsx
flutter doctor
```

![[Pasted image 20220513220013.png]]

## ２．Flutterプロジェクト作成・デモアプリ実行（30分）

１．以下のように作成

![[Pasted image 20220513220039.png]]

２．仮想デバイス（iOS）を実装

![[Pasted image 20220513220108.png]]
![[Pasted image 20220513220127.png]]

３．仮想デバイス（Andoroid）を実装
![[Pasted image 20220513220156.png]]
![[Pasted image 20220513220209.png]]

System Image：何でもいいらしいのでPieに
![[Pasted image 20220513220235.png]]
![[Pasted image 20220513220251.png]]

４．アプリの実行
![[Pasted image 20220513220307.png]]
Android：
![[Pasted image 20220513220324.png]]

iOS：同じ見た目
![[Pasted image 20220513220346.png]]
## Appendix．UIのデザインツール

３−１．Flutter Studio

WEB上でデザイン⇛コード生成できるが、

・慣れが必要そう、機能的にFigmaに劣ってそう

・コードを完全には使えない（クラス名がデフォルト、構文？が違う）

[AppBuilder 2 20180529-19:35](https://flutterstudio.app/)

３−２．Figma to Flutter

・生成されるコードがイマイチ

[Figma to Flutter](https://aloisdeniel.github.io/figma-to-flutter/)

３−３．Adobe XD

これは使ってないが、一番マシな気がする。ただし有償