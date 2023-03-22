# WslMemo
WSL (Windows Subsystem for Linux) の覚え書き。
最初にやることリスト。

3行まとめ: ストアを開いて
* Windows Terminal
* WSL2
  * Windows Subsystem for Linux と Ubuntu, Debian のような個別のディストロが
  あるが、違いはよく分からない。前者は改めてディストロを選択してインストールする
  必要があるかも？
  個人的には Raspberry Pi に合わせて Debian を使用している。
* vscode

Windows Terminal は Windows 11 2022 Update (22H2) で既定のターミナルとなった。
それ以前の場合はストアで。

# ターミナル

## Windows Terminal - ストアが使えない場合
github に個別インストールパッケージがあるのでこれを利用する。
https://github.com/microsoft/terminal/releases

自動更新はされないので新しくしたい場合はその都度ここを訪れる。

PreInstallKit でない普通のパッケージをダウンロードする。

1. ダブルクリックしてみる。
1. ダメなら、PowerShell で
`Add-AppxPackage Microsoft.WindowsTerminal_<versionNumber>.msixbundle`
を実行する。
1. ダメなら、Windows 10 を新しくするか VC++ v14 Desktop Framework Package
なるものを入れてみる。

詳しくは github トップの README に書いてある。
https://github.com/microsoft/terminal

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

### Windows Terminal を使わない場合
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
https://learn.microsoft.com/ja-jp/windows/wsl/install

## インストール
以前のやり方は古くなった。
Windows 10 の十分なバージョンまたは Windows 11 ならば wsl.exe で必要なものが
すべて整う。

Windows Terminal でないとインストール中に盛大に文字化けしてエラーが出た場合に
何も分からないと思われるため、Windows Terminal 推奨。
管理者権限が必要。

```
wsl --help
wsl --list --online
wsl --install <Distribution Name>
```

Distribution Name を指定しないとデフォルトで Ubuntu がインストールされるため
注意(一敗)。
ディストリビューションの削除は --unregister コマンドでできる
(何でアンインストールじゃないんだ)。
しかしスタートメニューに残る気もするのでそこからアンインストールする。
しかし Windows Terminal のメニューに残る気もするので Windows Terminal を
再インストールする。。

## WSL の有効化 (旧)
管理者権限で PowerShell を開き、以下を実行する。
(WSL1 が動いているなら既に有効になっているはず)
コントロールパネルの "Windows 機能の有効化" 相当っぽい。
```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

## 仮想マシン機能の有効化 (旧)
Windows の仮想マシン機能っぽい何か。
WSL2 は仮想マシン上で Linux kernel を動作させる。
BIOS で仮想化機能を有効にしておく必要がある可能性がある。
```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
ここで **再起動** が必要らしい。

## Linux kernel の更新 (旧)
https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

現在の Windows 内に Linux kernel が同梱されている衝撃。
更新しなくてもまあまあ動くかもしれないし、更新しないと動かない場合もあるらしい。

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

新規インストール時のバージョンを 2 にするには
(WSL1 を使っていたのでなければおそらく不要)
```
wsl --set-default-version 2
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
最近は WSL 内で促されるようになった気がする。
wsl.exe で可能 (WSL から Windows コマンドを実行する場合は .exe が必要)。
```
wsl.exe --update
```

カーネルバージョン確認は WSL 内で
```
uname -r
```

## WSL の移行 or バックアップ/リストア
```
wsl.exe --export
wsl.exe --import
```
で可能らしい。(未検証)
