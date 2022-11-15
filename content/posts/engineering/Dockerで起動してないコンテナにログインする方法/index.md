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
 `docker run` のオプションで `-it` を指定することで、コンテナが終了してもログイン出来るようになる。`-it` はそれぞれ独立したオプションで、`-i(interactive)` , `-t(tty)` [^1]
 
コマンドとしては以下のような感じ：

```
docker run -it --entrypoint /bin/sh {container_name}
```

- `container_name` は `docker images` で確認。`docker build -t {name}:{tag}` でビルド時に名前を指定可能。

### docker composeの場合
docker composeでも同様の事をしたい場合は、docker-compose.yamlで以下のオプションを追加すればよい。
```
tty: true
stdin_open: true

* service.{service_name} の階層に書く
```

[^1]: [Docker run リファレンス](https://docs.docker.jp/engine/reference/run.html)
