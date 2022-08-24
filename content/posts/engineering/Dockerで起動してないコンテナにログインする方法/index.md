---
date: 2022-08-24
title: Dockerで起動してないコンテナにログインする方法
---

## 背景
Dockerにログインして、ディレクトリの構造などを確認したい場合、一般的なやり方だと以下のように起動しているコンテナのidを調べてログインをしている。
```
docker run {container_name}
docker ps
docker exec -it {container_id} /bin/sh
```
こちらの方法だと、Dockerfileで指定しているコマンドが起動直後に終了する場合、`docker ps`
 してもコンテナが既に終了しており、ログイン出来ないという事がある。

## 方法
 そのため、どうにかコンテナにログインする方法は無いか調べたところ、 `docker run` のオプションで `--entrypoint /bin/sh` を指定して、ENTRYPOINT (コンテナ起動時に最初に実行されるコマンド) を上書きするのが良い事がわかった。
 
コマンドとしては以下のような感じ：

```
docker run -it --entrypoint /bin/sh {container_name}
```

- `container_name` は `docker images` で確認。`docker build -t {name}:{tag}` でビルド時に名前を指定可能。

## 参考

[ENTRYPOINT（実行時に処理するデフォルトのコマンド）](https://docs.docker.jp/engine/reference/run.html#run-entrypoint)
