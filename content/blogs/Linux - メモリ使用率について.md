## Hello
- freeコマンド
	- total : 合計
	- used : カーネルとプロセスが使用している
	- shared : tmpfsに使われている
	- free : 余っている
	- buffers : バッファキャッシュのメモリサイズ
	- cache : ページキャッシュのメモリサイズ
	- available : 実質的な空きメモリ
		- free + buff/cache (解放可能な部分)
![Pasted image 20220425152016.png](app://local/Users/01579137/code/github.com/ny1030/note/attachment/Pasted%20image%2020220425152016.png?1650867616628)
- sar コマンド
物理メモリ使用量が表示される
[sar -r でメモリ使用状況を確認する - ablog](https://yohei-a.hatenablog.jp/entry/20090322/1237744536)

- vmstat
	- 

#Linux #Command