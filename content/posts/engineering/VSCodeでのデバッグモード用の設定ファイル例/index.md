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
            "args": ["../data/thread/1653823316.json"]
        }
    ]
}
```
上記のような設定をすることで動くことを確認。補足として、cwd (change work directory) を入れないと、実行した際に `03_filter.py not found` みたいなエラーが出たので VSCodeのRootフォルダとプログラムの場所が同じで無い場合は入れておいたほうがいい。

## Nodejs
- コマンド
```
node 02_get.js
```
- VSCode上の設定（launch.json）
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Program",
            "program": "02_get.js",
            "cwd": "${workspaceFolder}/app/script",
            "request": "launch",
            "runtimeExecutable": "${HOME}/.nodebrew/node/v14.6.0/bin/node",
            "skipFiles": [
                "<node_internals>/**"
            ],
            "type": "node"
        }
    ]
}
```
