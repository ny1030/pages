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
![](Pasted%20image%2020220612155127.png)

４．Andoroid toolchainのエラー解消

・Command-Line Toolsのインストール（AndoroidSDKの設定画面からできる）

![](Pasted%20image%2020220612155223.png)

・Andoroidライセンスの許可

```jsx
flutter doctor --android-licenses
```

※ javaのPATH通ってないとエラー出る

５．Android toolchainがチェックついてることを確認

```jsx
flutter doctor
```

![](Pasted%20image%2020220612155500.png)

６．FlutterプラグインをAndoroid Studioからインストール

![](Pasted%20image%2020220612155444.png)

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

![](Pasted%20image%2020220612155515.png)

## ２．Flutterプロジェクト作成・デモアプリ実行（30分）

１．以下のように作成

![](Pasted%20image%2020220612155530.png)

２．仮想デバイス（iOS）を実装

![](Pasted%20image%2020220612155608.png)
![](Pasted%20image%2020220612155552.png)

３．仮想デバイス（Andoroid）を実装
![](Pasted%20image%2020220612155628.png)
![](Pasted%20image%2020220612155645.png)

System Image：何でもいいらしいのでPieに
![](Pasted%20image%2020220612155701.png)
![](Pasted%20image%2020220612155719.png)

４．アプリの実行
![](Pasted%20image%2020220612155738.png)
Android：
![](Pasted%20image%2020220612155759.png)

iOS：同じ見た目
![](Pasted%20image%2020220612155820.png)
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