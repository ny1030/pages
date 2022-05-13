---
date: "2022-05-03"
title: Linux - メモリ使用率について
---
## freeコマンド
- total : 合計
- used : カーネルとプロセスが使用している
- shared : tmpfsに使われている
- free : 余っている
- buffers : バッファキャッシュのメモリサイズ
- cache : ページキャッシュのメモリサイズ
- available : 実質的な空きメモリ
	- free + buff/cache (解放可能な部分)
![](Pasted%20image%2020220511234524.png)
## sar コマンド
物理メモリ使用量が表示される = buffers, cacheが含まれた使用量
[sar -r でメモリ使用状況を確認する - ablog](https://yohei-a.hatenablog.jp/entry/20090322/1237744536)
