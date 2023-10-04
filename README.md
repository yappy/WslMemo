# WslMemo

WSL (Windows Subsystem for Linux) の覚え書き。
最初にやることリスト。

## 3行まとめ

ストアを開いて

* WSL2
  * Windows Subsystem for Linux と Ubuntu, Debian のような個別のディストロが
  あるが、違いはよく分からない。前者は改めてディストロを選択してインストールする
  必要があるかも？
  個人的には Raspberry Pi に合わせて Debian を使用している。
* VSCode
* Windows Terminal

Windows Terminal は Windows 11 2022 Update (22H2) で既定のターミナルとなった。
それ以前の場合はストアで。

ストアが使えない場合はそれぞれ頑張ってダウンロードしてきてインストールする。
学校や会社の PC はそうなりがちなので頑張る。

## 3行でない手順

* Windows で github 上でこのファイルを見る。
* WSL を入れる。
* Linux に入れたら git をインストールしつつ、ここのリポジトリを Linux 上に手に入れる。
* それを読みながら VSCode と Windows Terminal を入れる。

```sh
# apt 使用の場合
sudo apt install git
git clone https://github.com/yappy/WslMemo
```

## ターミナル

### Windows Terminal - ストアが使えない場合

github に個別インストールパッケージがあるのでこれを利用する。\
<https://github.com/microsoft/terminal/releases>

自動更新はされないので新しくしたい場合はその都度ここを訪れる。

PreInstallKit でない普通のパッケージをダウンロードする。

1. ダブルクリックしてみる。
1. ダメなら、PowerShell で
`Add-AppxPackage Microsoft.WindowsTerminal_<versionNumber>.msixbundle`
を実行する。
1. ダメなら、Windows 10 を新しくするか VC++ v14 Desktop Framework Package
なるものを入れてみる。
1. ダメなら、会社の PC に Windows Update がかかるのを待って再チャレンジ。

詳しくは github トップの README に書いてある。
<https://github.com/microsoft/terminal>

### 一部ディレクトリの色が見づらい

黒地に濃い青は見えない。

#### 解1: Windows Terminal を使う

デフォルトで WSL が起動する窓は conhost.exe と言って、歴史的には Windows 1.01 上で
MS-DOS アプリケーションを動かすために導入されたものらしい。
cmd.exe が動くのと同じもので、そういえば cmd.exe は DOS 窓と呼ばれるのでした。

文字コードその他いろいろに関して互換性を保ちつつ改良するのが無理になったので、
Microsoft 公式オープンソースソフトウェアとして Windows Terminal が開発された。
Windows に同梱はされないが、ストアで検索してポチれば OK。無料。
ストアが使えない会社の PC 等は github にパッケージリリースがある (前述)。
conhost.exe は互換性のため以降もサポートされるが、さすがに歴史を感じすぎるので
コンソールを使う開発者はとりあえずこれを入れておけばよさそう。

とりあえず評判はよい。
タブも使えて PowerShell も WSL も全部これでいける。
Ctrl + C でコピーできなかったのも conhost.exe のせい。これも解消する。

これでデフォルト背景色がちょっと明るい黒になり、青色が見えるようになる
(青色も薄くなっている気がするが目の錯覚かもしれない)。

#### 解2: dircolors を設定する

.bashrc でホームディレクトリに `.dircolors` ファイルがあればそれを使うように
なっているので、`dircolors -p` コマンドでデフォルト値を出力した後
それを編集する。

```bash
# Output defaults
dircolors -p > .dircolors

# <edit>

# Apply
source ~/.bashrc
```

`DIR` などの `34=blue` になっているところを `36=cyan` あたりに変更すれば
だいたい同じ印象のまま視認性が改善する。

```bash
# Text color codes:
# 30=black 31=red 32=green 33=yellow 34=blue 35=magenta 36=cyan 37=white
# Background color codes:
# 40=black 41=red 42=green 43=yellow 44=blue 45=magenta 46=cyan 47=white
```

### プロンプトのカレントディレクトリが見づらい

こちらも Windows Terminal へ移行すれば自動的に改善する。

#### Windows Terminal を使わない場合

.bashrc の以下の行が設定箇所。

```bash
if [ "$color_prompt" = yes ]; then
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
```

34(blue) を例えば 36(cyan) にする。

### Tab 自動補完時のビープ音がうるさい

`/etc/inputrc` を編集。

```sh
# uncomment
set bell-style none
```

## WSL2

WSL1 からの移行ガイドを含む。

公式ドキュメントトップ:
<https://docs.microsoft.com/ja-jp/windows/wsl/>

インストールガイド:
<https://learn.microsoft.com/ja-jp/windows/wsl/install>

### インストール

Windows 10 の十分なバージョンまたは Windows 11 ならば wsl.exe で必要なものが
だいたい揃うようになった。

Windows Terminal でないとインストール中に盛大に文字化けしてエラーが出た場合に
何も分からないと思われるため、Windows Terminal 推奨。
管理者権限が必要。

```ps
wsl --help
wsl --list --online
wsl --install <Distribution Name>
```

Distribution Name を指定しない (公式の `wsl --install` の通りに実行する) と
デフォルトで Ubuntu がインストールされるため注意(一敗)。
よく見ると下に書いてある。
ディストリビューションの削除は --unregister コマンドでできる
(何でアンインストールじゃないんだ)。
しかしスタートメニューに残る気もするのでそこからアンインストールする。
しかし Windows Terminal のメニューに残る気もするので Windows Terminal を
再インストールする。。

### WSL の有効化

公式だと wsl.exe が全部やってくれる風なことを書いているが、やってくれない気もする。
wsl.exe が古いだけかもしれない。
機能が有効化されていません的なエラーが出た場合は以下を実行する。

管理者権限で PowerShell を開き、以下を実行する。
(WSL1 が動いているなら既に有効になっているはず)
コントロールパネルの "Windows 機能の有効化" 相当っぽい。

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

### 仮想マシン機能の有効化

Windows の仮想マシン機能っぽい何か。
WSL2 は仮想マシン上で Linux kernel を動作させる。

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

ここで **再起動** が必要らしい。

### BIOS 仮想化機能有効化

上記まででうまくいかない場合、BIOS(UEFI) で仮想化機能が無効になっている可能性がある。
確認方法は以下。

1. タスクマネージャ
1. パフォーマンス
1. CPU
1. "仮想化" の欄

設定方法は PC によって異なる。。

1. 起動時に F2 か Delete キーあたりを連打する。
1. Advanced とか Virtualization あたりの設定項目を探す。
1. 有効にする。

Intel CPU と AMD CPU では名前も仕様も違う。どうして…。

* Intel
  * VT-X
  * VMX
  * Intel Virtualization Technology
* AMD
  * AMD-V
  * SVM (Secure Virtual Machine)

とか大体そんな感じの名前。

### Linux kernel の更新

現在の Windows 内に Linux kernel が同梱されている衝撃。
更新しなくてもまあまあ動くかもしれないし、更新しないと動かない場合もあるらしい。
最近はログインするだけで自動でアップデートをお知らせしてくれるようになった。親切。

```powershell
wsl.exe --update
```

カーネルバージョン確認は WSL 内で

```sh
uname -r
```

<https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi>\
だいたい wsl.exe で事足りそうだが、一応最新のインストーラはここにある。

### WSL1 からの移行

インストールされているディストリビューションと WSL version のリスト

```powershell
wsl --list --verbose
```

以下のコマンドで少し待てばかなり簡単にバージョン移行できる。
(WSL1 に戻すのも可)

```powershell
wsl --set-version <distribution name> <versionNumber>

# 例:
wsl --set-version Debian 2
```

新規インストール時のバージョンを 2 にするには
(WSL1 を使っていたのでなければおそらく不要)

```powershell
wsl --set-default-version 2
```
