---
date: "2022-03-05"
title: Drupal関連のコマンド
---

### マイナーバージョンアップ

※スペック低すぎると失敗するので、4コア8GBに事前スケールアップした

- バージョン確認

`composer outdated "drupal/*"`

- druplaのrootディレクトリで以下を実行

sudo `composer update drupal/core "drupal/core-*" --with-all-dependencies`
sudo `composer update drupal/core --with-dependencies`

[参考](https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer)
### housekeeping(キャッシュ削除)
`drush -y wd-del all`
