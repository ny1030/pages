---
date: 2021-10-22
title: ApacheのRedirect/Rewrite設定
---

## www無しドメイン -> www有りドメインにリダイレクト
参考：[Apache RewriteCond の基礎知識 | - WEB ARCH LABO](https://weblabo.oscasierra.net/apache-rewritecond-base/)
`{apache_dir}/conf/vhost`
```
<VirtualHost *:80>

...

	<Directory "/opt/blog">
	...
	</Directory>

RewriteEngine On
RewriteCond %{HTTP_HOST} !^www\. [NC]
RewriteCond %{REQUEST_URI} !^/admin/
RewriteRule ^(.*)$ http://www.%{HTTP_HOST}%{REQUEST_URI} [R=301,L]

...

</VirtualHost>
```
 - RewriteEngine On: このディレクティブを書かないとRewriteは動かない。言い換えるとここだけコメントアウトすればRewriteを無効にできる。
 - RewriteCond: この条件に合致（true）したらRewriteRuleにしたがってURLの書き換えをおこなう。
	 - 今回の例：サーバのホスト名`%{HTTP_HOST}` でwww.が先頭にない `!^www\.`とき。（大文字小文字は区別しない`[NC]`）
	 - RewriteCondを複数記述した場合はデフォルトではAND条件になる。ORにしたい場合は末尾に `[OR]` を指定する。
- RewriteRule: URLの書き換えルールを書いている。リダイレクトのステータスコードを末尾に記載。
	- `[L]` をつけると振り分けが終わる（それ以降の処理は無視される）が、Rewrite後に再度評価が実行されるのでループに注意とのこと。再度評価をしたくない場合、`[END]` をつければいいとのこと。[.htaccess に RewriteRule 書くときは、[L]フラグをつけても](https://qiita.com/ezaki/items/87c2dff8f7753ef048d2)
