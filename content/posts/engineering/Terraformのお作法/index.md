---
date: 2022-05-23
title: Terraformのお作法
---

## 基本コンセプト
### Composition
コンポジションはインフラモジュールの集合体であり、論理的に分離された複数の領域（例：AWSリージョン、複数のAWSアカウント）にまたがることが可能である。コンポジションは、組織全体やプロジェクトに必要な完全なインフラストラクチャを表現するために使用される。

コンポジションは、インフラストラクチャーモジュールで構成され、リソースモジュールで構成され、個々のリソースを実装する。
![](Pasted%20image%2020220523111241.png)


## 作成すべきファイル
- main.tf: モジュール、ローカル、データソースを呼び出して、すべてのリソースを作成
- outpputs.tf: main.tfで作成されたリソースからの出力
- variables.tf: main.tfで使用される変数の宣言
- terraform.tfvars: 環境特有の変数の値を宣言

ref: [terraform-best-practices](https://github.com/antonbabenko/terraform-best-practices)**

