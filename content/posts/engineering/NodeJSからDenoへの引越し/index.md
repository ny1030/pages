---
date: "2022-12-10"
title: NodeJSからDenoへの引越し
---

※順次追記
# Context

jsランタイム環境であるDenoが最近目にするので、勉強のためにNodejsで書いたコードをDenoに引越ししてみる。

Deno: https://deno.land/

# 処理別の実装方法

## JSONのconfigをスクリプトに読み込む
- Nodejs
`node-config` モジュールを使って以下のように、JSONファイルをオブジェクトとして読み込む。
```
const conf = require('config'); //JSONファイルは ./config/default.json

const INTERVAL = conf.interval;
const LOWER_LIMIT = conf.lowerLimit;
const UPPER_LIMIT = conf.upperLimit;
```
- Deno
最も簡単と思われる方法は以下のようにnpmをインポートする。
```
import config from "npm:config";
console.log(config);
```
ただし、この機能自体はDenoが作られた経緯（脱npm）とは反するもので、Deno社も渋々npmをサポートしているように見える。[^1]

また、npmのサポートは実験的な機能でまだサポートされてないパッケージもあるので、極力使わないほうがいいかもしれない。

### 方法1. Denoで公開されているModuleを使う
npmが使えない -> ならDenoで公開しているModuleを使う、という方法。Moduleは以下で公開されている。

https://deno.land/x

configで検索して[出てきたModule](https://deno.land/x/load_config_files@0.3.0)を使ってみる。Documentに書いてる例を参考に、以下のような構造のディレクトリを作成する。
```plaintext
{project_root}
├── app1.ts
└── config
    └── prod
        └── app1.json
```
設定ファイルが  `app1.json` で、スクリプトが `app1.ts` とする。

```ts
import {
    Config,
    CONFIG_FORMATTERS,
    ConfigFormatter,
    loadConfig,
    LoadConfigOptions,
} from "https://deno.land/x/load_config_files@0.3.0/mod.ts";

const options: LoadConfigOptions = { verbose: false };

const [formatterId, configRootPath, ...segments] = Deno.args;
const configRootUrl = new URL(configRootPath, "file:" + Deno.cwd());
const config: Config = await loadConfig(configRootUrl, segments, options);
const formatter: ConfigFormatter = CONFIG_FORMATTERS[formatterId];

const output: string = await formatter(config);
console.log(output);
```

割りと長いが、実行時に以下のようなオプションを引数で渡すことで読み込みできることを確認。
```
formatterId: 設定ファイルをパースする時の形式 (shell, json, spring_shell)
configRootPath: configファイルのRootフォルダのパス（例の場合はconfig）
segments: config配下にフォルダ/ファイルが複数ある時の絞り込むオプションかと思う。例では、prodとapp1を指定。
```
実行時のコマンドは以下のようになる。
```bash
deno run --allow-read --allow-net=deno.land app1.ts json config prod app1
```
毎度実行する際に、上記のようなコマンドを打つのは辛いので、スクリプトランナーなるものを使うのが良さそう。Denoでは[velociraptor](https://github.com/jurassiscripts/velociraptor)が名前もそれっぽいので使いやすそう。

ちなみに、設定ファイルを指定するパスは スクリプトファイルから見た相対パスでなく、project_rootのディレクトリから見た相対パスであるので注意。今回は両者とも同じ場所だが、更にフォルダを作ってスクリプトと設定ファイルを入れた場合は、`{作成したフォルダ名}/config` と指定しなければならない。
上手く動かない際は、 `const options: LoadConfigOptions = { verbose: false };` のオプションをtrueにするとログが出力されるのでオススメ。

### 方法2. Deno標準機能だけで実装する
サードパーティを使わない方法も試してみたので、こちらに記載。チュートリアルのexampleに載っている例を参考に、以下のようにjsonファイルを読み込む。[^2]

```ts
import conf from "./config/config.json" assert { type: "json" };
console.log(conf);
```

単一のファイルを読み込む場合にはこちらのほうがシンプルだが、環境ごとに設定ファイルを分けたい場合などは結局引数から情報を渡す必要があるので、同じ感じにはなりそう。

[^1]: [Compatibility with Node and npm](https://deno.com/blog/changes#compatibility-with-node-and-npm)
[^2]: [Importing JSON](https://examples.deno.land/importing-json)