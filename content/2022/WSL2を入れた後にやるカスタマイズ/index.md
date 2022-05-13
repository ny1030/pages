---
date: "2022-03-05"
title: SQLパフォーマンスチューニング
---
# WSL2を入れた後にやるカスタマイズ

※ OSは Ubuntu 20.04(LTS) を使用

-   まずはプロンプトを変更（ミニマルな内容にする）

```
#1.まずは現在の設定確認
user@DESKTOP-XXXXX:~$ **echo $PS1**
\\[\\e]0;\\u@\\h: \\w\\a\\]${debian_chroot:+($debian_chroot)}\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$

#2.PS1の値を書き換え
user@DESKTOP-XXXXX:~$ **PS1='\\[\\e[1;32m\\]\\W\\$ \\[\\e[m\\]'**
~$

#3.設定内容を永続化
~$ **echo "PS1='\\[\\e[1;32m\\]\\W\\$ \\[\\e[m\\]'" >> .bashrc**

#4.ターミナルを再起動して、設定が永続化されてること確認
~$
```

-   systemd を PID1（親プロセス）にする

```
#1.現状のプロセスを確認
~$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0    896   528 ?        Sl   16:13   0:00 /init
root       120  0.0  0.0    896    84 ?        Ss   16:19   0:00 /init

#2.dotnet-runtime-5.0などの依存モジュールをインストール
wget <https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb> -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

sudo apt-get update; \\
  sudo apt-get install -y apt-transport-https && \\
  sudo apt-get update && \\
  sudo apt-get install -y aspnetcore-runtime-5.0

sudo apt install -y daemonize dbus gawk libc6 libstdc++6 policykit-1 systemd systemd-container

sudo -s
apt install apt-transport-https
wget -O /etc/apt/trusted.gpg.d/wsl-transdebian.gpg <https://arkane-systems.github.io/wsl-transdebian/apt/wsl-transdebian.gpg>
chmod a+r /etc/apt/trusted.gpg.d/wsl-transdebian.gpg
cat << EOF > /etc/apt/sources.list.d/wsl-transdebian.list
deb <https://arkane-systems.github.io/wsl-transdebian/apt/> $(lsb_release -cs) main
deb-src <https://arkane-systems.github.io/wsl-transdebian/apt/> $(lsb_release -cs) main
EOF
apt update

#3.genieインストール
sudo apt install -y systemd-genie

#4.genieを実行
genie -s

#5.エラー解消

#5-1.systemd-remount-fs.serviceのエラーを解消する

dfでルートパーティション確認→/dev/sdb
sudo e2label /dev/sdb cloudimg-rootfs

#5-2.multipathd.socketのエラーを解消する
sudo systemctl disable multipathd.socket

#5-3.ssh.serviceのエラーを解消する
sudo ssh-keygen -A

#6.bashrcに設定記入

# Are we in the bottle?
if [[ ! -v INSIDE_GENIE ]]; then
  echo "Starting genie:"
  exec /usr/bin/genie -s
fi

#7.Ubuntu再起動後にPID1を確認

~$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.2  0.1 175028 13128 ?        Ss   21:40   0:01 systemd
root          50  0.0  0.1  51456 15596 ?        S<s  21:40   0:00 /lib/systemd/systemd-journald
root          72  0.0  0.0  19564  5228 ?        Ss   21:40   0:00 /lib/systemd/systemd-udevd

```

補足：systemdをPID1にしないと、systemctlを実行すると以下のようなエラーが出る

```
System has not been booted with systemd as init system (PID 1). Can't operate.
Failed to connect to bus: Host is down
```

-   WindowsのPATHを引き継がないように設定

```
1. 設定の追加

sudo vi /etc/wsl.conf
--
# WindowsのPATHを引き継がない設定を追記する
[interop]
appendWindowsPath = false

2. Widnowsコマンドプロンプトから再起動
--
wsl.exe --shutdown
```

-   Golangをインストール

```
# 1. Goのパッケージをダウンロード
~$ wget <https://go.dev/dl/go1.17.7.linux-amd64.tar.gz>

# 2. 展開
~$ sudo tar -C /usr/local -xzf go1.17.7.linux-amd64.tar.gz

# 3. PATHに追加・反映
~$ echo "PATH=$PATH:/usr/local/go/bin" >> .bashrc
~$ source .bashrc

# 4．動作確認
~$ go version
go version go1.17.7 linux/amd64
```

-   ghq（Gitリポジトリ管理ツール）をインストール

```
go install github.com/x-motemen/ghq@latest
echo "PATH=$PATH:~/go/bin" >> .bashrc

# dial tcp: lookup proxy.golang.org: no such host のエラー出た場合
go env -w GOPROXY=direct
```

-   AWS CLI 2をインストール

```
curl "<https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip>" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
~$ aws --version
aws-cli/2.4.23 Python/3.8.8 Linux/5.10.60.1-microsoft-standard-WSL2 exe/x86_64.ubuntu.20 prompt/off
```

-   AWS Session Managerをインストール

```
curl "<https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb>" -o "session-manager-plugin.deb"
sudo dpkg -i session-manager-plugin.deb
~$ session-manager-plugin

The Session Manager plugin was installed successfully. Use the AWS CLI to start a session.
```

## Proxy環境下の関連設定
### zscalerの場合
-   Linuxで証明書導入

```
/usr/share/ca-certificates/ 配下に任意のディレクトリ作成
/usr/share/ca-certificates/zscaler/ 配下に証明書を配置
/etc/ca-certificates.confに/usr/share/ca-certificates/ 以下の相対パスを追加
（ここではzscaler/zscaler.cer）
/usr/sbin/update-ca-certificatesを実行
```

-   aws

```
export AWS_CA_BUNDLE=~/zscaler_root.crt
```

-   git, conda, pip

```
１．最新のPythonの信頼する証明書リストを入手する。<https://curl.haxx.se/ca/cacert.pemからダウンロードする。>

２．このファイルの末尾に、テキスト形式で保存したzscalerのオレオレ証明書のテキストを追加する。

３．以下のパスに保存する# Windows%USERPROFILE%\\certs\\ca-bundle.crt

４．以下のコマンドをコマンドプロンプトで実行し、保存した証明書リストを使うように設定する。
pip config set global.cert %USERPROFILE%\\certs\\ca-bundle.crtconda config --set ssl_verify %USERPROFILE%\\certs\\ca-bundle.crtgit config --global http.sslVerify truegit config --global http.sslCAInfo path/to/ca-bundle.crt
```

-   DNS Resolver に8.8.8.8追加

```
#1. /etc/systemd/resolved.conf に以下を追加

---------------
[Resolve]
DNS=8.8.8.8

#2.再起動
systemctl restart systemd-resolved

#3.DNS確認
systemd-resolve --status

```