# WslMemo
WSL (Windows Subsystem for Linux) の覚え書き。
最初にやることリスト。

3行まとめ: ストアを開いて
* vscode
* Windows Terminal
* WSL2
  * Windows Subsystem for Linux と Ubuntu, Debian のような個別のディストロが
  あるが、違いはよく分からない。前者は改めてディストロを選択してインストールする
  必要があるかも？
  個人的には Raspberry Pi に合わせて Debian を使用している。

## 一部ディレクトリの色が見づらい
黒地に濃い青は見えない。

### 解1: Windows Terminal を使う
デフォルトで WSL が起動する窓は conhost.exe と言って、歴史的には Windows 1.01 上で
MS-DOS アプリケーションを動かすために導入されたものらしい。
cmd.exe が動くのと同じもので、そういえば cmd.exe は DOS 窓と呼ばれるのでした。

文字コードその他いろいろに関して互換性を保ちつつ改良するのが無理になったので、
Microsoft 公式オープンソースソフトウェアとして Windows Terminal が開発された。
Windows に同梱はされないが、ストアで検索してポチれば OK。無料。
ストアが使えない会社の PC 等は github にパッケージリリースがあるらしい (未検証)。
conhost.exe は互換性のため以降もサポートされるが、さすがに歴史を感じすぎるので
コンソールを使う開発者はとりあえずこれを入れておけばよさそう。

とりあえず評判はよい。
タブも使えて PowerShell も WSL も全部これでいける。
Ctrl + C でコピーできなかったのも conhost.exe のせい。
これも解消する。

これでデフォルト背景色がちょっと明るい黒になり、青色が見えるようになる
(青色も薄くなっている気がするが目の錯覚かもしれない)。

### 解2: dircolors を設定する
.bashrc でホームディレクトリに `.dircolors` ファイルがあればそれを使うように
なっているので、`dircolors -p` コマンドでデフォルト値を出力した後
それを編集する。

```
# Output defaults
dircolors -p > .dircolors

# <edit>

# Apply
source ~/.bashrc
```

`DIR` などの `34=blue` になっているところを `36=cyan` あたりに変更すれば
だいたい同じ印象のまま視認性が改善する。
```
# Text color codes:
# 30=black 31=red 32=green 33=yellow 34=blue 35=magenta 36=cyan 37=white
# Background color codes:
# 40=black 41=red 42=green 43=yellow 44=blue 45=magenta 46=cyan 47=white
```

## プロンプトのカレントディレクトリが見づらい
こちらも Windows Terminal へ移行すれば自動的に改善する。

.bashrc の以下の行が設定箇所。

```
if [ "$color_prompt" = yes ]; then
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
```

34(blue) を例えば 36(cyan) にする。


## Tab 自動補完時のビープ音がうるさい
`/etc/inputrc` を編集。
```
# uncomment
set bell-style none
```

# WSL2
WSL1 からの移行ガイドを含む。

公式ドキュメントトップ:
https://docs.microsoft.com/ja-jp/windows/wsl/

インストールガイド:
https://docs.microsoft.com/ja-jp/windows/wsl/install-win10

## WSL の有効化
管理者権限で PowerShell を開き、以下を実行する。
(WSL1 が動いているなら既に有効になっているはず)
コントロールパネルの "Windows 機能の有効化" 相当っぽい。
```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

## 仮想マシン機能の有効化
Windows の仮想マシン機能っぽい何か。
WSL2 は仮想マシン上で Linux kernel を動作させる。
BIOS で仮想化機能を有効にしておく必要がある可能性がある。
```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
ここで **再起動** が必要らしい。

## Linux kernel の更新
https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

現在の Windows 内に Linux kernel が同梱されている衝撃。
更新しなくてもまあまあ動くかもしれないし、更新しないと動かない場合もあるらしい。

## WSL デフォルトバージョンの変更
新規インストール時のバージョンを 2 にする。

PowerShell で
```
wsl --set-default-version 2
```

## ディストリビューションのインストール
ストアで Linux で検索すると色々出てくるので好きなものをインストールする。

## WSL1 からの移行
インストールされているディストリビューションと WSL version のリスト
```
wsl --list --verbose
```

以下のコマンドで少し待てばかなり簡単にバージョン移行できる。
(WSL1 に戻すのも可)
```
wsl --set-version <distribution name> <versionNumber>

例:
wsl --set-version Debian 2
```

## 仮想ディスクの掃除
WSL2 になりただの仮想マシンとなってしまったため、ゲスト OS 上でファイルを消しても
仮想ディスクファイルが大きくなったまま戻らない。
docker を連打した、事故ってクソデカファイルを作ってしまった、
いつの間にか肥大化していた、等の場合。

Microsoft の github に issue が上がっている。

https://github.com/microsoft/WSL/issues/4699

Optimize-VHD コマンドでコンパクション可能だそうだが、Windows Pro でないと存在しない。
diskpart コマンドなら Windows Home でも存在する。

1. %LocalAppData% 内で `ext4.vhdx` を検索し、パスを得る。
ファイルを Shift + 右クリックで "パスのコピー" ができるぞ。
1. PowerShell を管理者権限で立ち上げる。
Windows + R でファイル名を指定して実行。この時 Ctrl + Shift + Enter で決定すると
管理者権限で実行できるぞ。
1. 以下のように仮想マシンをシャットダウンしてから diskpart コマンドで
コンパクションを行う。

```
wsl --shutdown
diskpart
# open window Diskpart
select vdisk file="C:\...\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

WSL はシャットダウン状態でシェルを開こうとすると自動的に起動する。

## Linux kernel のアップデート
管理者権限で PowerShell を開き、
```
wsl --update
```

カーネルバージョン確認は WSL 内で
```
uname -r
```
