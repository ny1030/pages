---
date: 2022-06-22
title: Spring Boot のJDBCコネクションプール（HikariCP）のロギング方法
---

## やりたいこと
Spring Boot で オンラインアプリケーションを作成した時に、DBとの接続をコネクションプール（以降コネプ）を用いる時に、コネプのサイズが適正かどうかを確認するためにログに使用状況を出したい。
*前提として、使用するコネプライブラリはSpring Boot 2.0のデフォルトであるHikariCPとする。

## 設定方法の例
logback.xmlに以下のようなloggerディレクティブを追加する。
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
	    <encoder>
	      <pattern>%msg%n</pattern>
	    </encoder>
	</appender>
    <logger name="com.zaxxer.hikari" level="DEBUG" additivity="false">
        <appender-ref ref="STDOUT"/>
    </logger>
    <root level="INFO">
       <appender-ref ref="STDOUT" />
    </root>
</configuration>
```
上記設定をおこなうことで、以下のようなコネプ使用状況のログが30秒間隔で出力されることを確認。
```
...
2020-06-04T02:26:18+00:00 serviceA.xxxxxx.debug  {"hostName":"xxxxxx","level":"DEBUG","time":"2020-06-04T02:26:18.473763Z","message":"HikariPool-2 - Pool stats (total=10, active=0, idle=10, waiting=0)"}
2020-06-04T02:26:47+00:00 serviceA.xxxxxx.debug  {"hostName":"xxxxxx","level":"DEBUG","time":"2020-06-04T02:26:47.881731Z","message":"HikariPool-1 - Pool stats (total=20, active=0, idle=20, waiting=0)"}
2020-06-04T02:26:48+00:00 serviceA.xxxxxx.debug  {"hostName":"xxxxxx","level":"DEBUG","time":"2020-06-04T02:26:48.473995Z","message":"HikariPool-2 - Pool stats (total=10, active=0, idle=10, waiting=0)"}
...
```
messageに出力されている内容を抜粋すると以下の通り。
```
HikariPool-2 - Pool stats (total=10, active=0, idle=10, waiting=0)
```
それぞれ説明すると、
- HikariPool-2：コネプで設定しているJDBCのデータソース名。今回はWriterとReaderでそれぞれデータソースを設定したので、1と2がそれぞれ出ている。
- Pool stats：コネプの利用状況
	- total：確保しているpoolの最大数。
	- active：現在利用されているpoolの数。
	- idle：total - active の数。つまり待機状態のpool数。
	- waiting：poolを割り当てるのを待っているタスクの数？