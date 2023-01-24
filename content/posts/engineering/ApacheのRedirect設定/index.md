---
date: 2021-10-22
title: ApacheのRedirect/Rewrite設定
---

## Case1 www無しドメイン -> www有りドメインにリダイレクト
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
	 - RewriteCondを複数記述した場合はデフォルトではAND条件になる。ORにしたい場合は末尾に `[OR]` を指定する。例では2つ目のRewriteCondにおいて `/admin` のパスはリライトしないように条件を追加。
- RewriteRule: URLの書き換えルールを書いている。リダイレクトのステータスコードを末尾に記載。
	- `[L]` をつけると振り分けが終わる（それ以降の処理は無視される）が、Rewrite後に再度評価が実行されるのでループに注意とのこと。再度評価をしたくない場合、`[END]` をつければいいとのこと。[.htaccess に RewriteRule 書くときは、[L]フラグをつけても](https://qiita.com/ezaki/items/87c2dff8f7753ef048d2)
- 併せてhttpsにリダイレクトしたい場合はRewriteRuleで指定しているプロトコルをhttpsにする。

## Case2 www有りドメイン -> www無しドメインにリダイレクト

`{apache_dir}/conf/vhost`
```
<VirtualHost *:80>

...

	<Directory "/opt/blog">
	...
	</Directory>

RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteCond %{REQUEST_URI} !^/admin/
RewriteRule ^(.*)$ http://%1$1 [R=301,L]

...

</VirtualHost>
```
-  `%1` は RewriteCond で指定している `(.*)` キャプチャされたパターン。`http://www.example.com` の場合は `example.com` が入る。

## 補足
- 上記は http に対するリダイレクト設定。https向けには、`<VirtualHost *:443>` ディレクティブが定義されているファイル）に同じ設定を加える。

## Case3 http -> httpsへリダイレクト
`{apache_dir}/conf/vhost`
```
<VirtualHost *:80>

...

	<Directory "/opt/blog">
	...
	</Directory>

RewriteEngine On
RewriteCond %{HTTP_HOST} ^(.*)$ [NC]
RewriteCond %{REQUEST_URI} !^/admin/
RewriteRule ^(.*)$ https://%1$1 [R=301,L]

...

</VirtualHost>
```
- Case2を若干変えた程度
