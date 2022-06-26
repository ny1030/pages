---
date: 2022-06-19
title: VSCodeで引数付きのプログラムをデバッグモードで動かす時の設定例
---

## Python
以下のような引数付きのPythonスクリプトをVSCode上のデバッグモードで実行する場合
- コマンド
```
python 03_filter.py ../data/1653823316.json
```
- VSCode上の設定（launch.json）
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Python",
            "program": "03_filter.py",
            "cwd": "${workspaceFolder}/app/script",
            "request": "launch",
            "type": "python",
            "args": ["../data/1653823316.json"]
        }
    ]
}
```
上記のような設定をすることで動くことを確認。補足として、cwd (change work directory) を入れないと、実行した際に `../data/1653823316.json not found` みたいなエラーが出たので、相対パスでファイルを読み込むコマンドを実行する時とは入れておいたほうがいい。

## Nodejs
- コマンド
```
node 11_post.js ../data/1655618612.json
```
- VSCode上の設定（launch.json）
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Node (11_post.js)",
            "program": "11_post.js",
            "cwd": "${workspaceFolder}/app/script",
            "request": "launch",
            "args": ["../data/1655618612.json"],
            "runtimeExecutable": "/usr/local/bin/node",
            "skipFiles": [
                "<node_internals>/**"
            ],
            "type": "node"
        }
    ]
}
```
