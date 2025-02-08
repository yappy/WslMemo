# WslMemo

WSL (Windows Subsystem for Linux) その他いろいろの覚え書き。
新しい Windows マシンをまともな状態にセットアップするために、最初にやることリスト。

## リンク

無事インストールできた後のことはこちら

* [WSL](wsl.md)
* [VSCode](vscode.md)
* [便利ツール集](tools/README.md)

## Windows テク

* 隠しファイルと拡張子の表示をオンにする。
  * Windows 8 あたりからフォルダオプションを出さなくても切り替えられるように
  なったっぽいので探してみるのも吉。
* 右クリックする時に Shift を押し続けていると出てくるメニューが変わる。
  * Windows 11 だと大分違う。
* `Windows+R` でファイル名を指定して実行
  * `Ctrl+Shift+Enter` で管理者権限で実行できる。
  * `cmd`: 昔ながらの DOS 窓。
  * `powershell`: PowerShell。Windows Terminal がないうちはとりあえずこれで。
  (Windows Terminal インストール後も結局中で PowerShell を動かすことになる)
* エクスプローラでパスに環境変数を使用
  * `%userprofile%`
  * `%appdata%`

## まとめ

* winget
  * Windows にインストールされているソフトウェアを
    apt / yum のようなノリで管理できる。
  * 入れられるようなら推奨
* WSL (新規にインストールするなら勝手に WSL2 が入る)
  * Windows の中で (正確には横で) 動く Linux 環境。
  * WSL2 は仮想マシン方式。
  * 個人的には Raspberry Pi に合わせて Debian を使用している。
* Windows Terminal
  * デフォルトで入っているターミナルは互換性維持のため変更を入れにくいので、
    分かってる人はこれを入れてほしいという Microsoft 公式の結構ちゃんとした
    コンソール。
  * DOS 窓、powershell、WSL 全てに対応。シェル自体ではなくそれの GUI 的なところ。
* VSCode
  * テキストエディタ。

Windows Terminal は Windows 11 2022 Update (22H2) で既定のターミナルとなった。
らしい。それ以前の場合はストアで。

winget やストアが使えない場合はそれぞれ頑張ってダウンロードしてきてインストールする。
学校や会社の PC はそうなりがちなので頑張る。

## 攻略フローチャート

* Windows のブラウザから github 上でこのファイルを見る。
* winget を入れる。
* (Windows Git を入れてもいいと思う場合、)`winget install Git` をインストールし、
  このリポジトリを Windows 上に手に入れる。
* WSL を入れる。
* Linux に入れたら Git をインストールしつつ、このリポジトリを Linux 上に手に入れる。
* それを読みながら VSCode と Windows Terminal を入れる。

```sh
# apt 使用の場合
# 最初から入っているなら不要
sudo apt install git
git clone https://github.com/yappy/WslMemo
```

winget 導入後、真っ先に Windows Terminal を入れてもよいが、
後から WSL を入れると設定に WSK の増えなかったりでトラブルを起こすかもしれないし、
最近は直っているかもしれない。

## winget

<https://learn.microsoft.com/ja-jp/windows/package-manager/winget/>

おそらくこの公式の説明が一番正確。
入れられそうなら入れるのを強く推奨。

~~要は apt / yum のぱくり。~~
使い勝手はほぼ同じです。

新しい Windows では最初から入っているっぽい。
とりあえず `winget -v` と打ってみよう。
しかしバージョンが古いと動作が怪しい可能性あり。
v1.2 系はやばいらしい。。依存関係のサポートも v1.6.2631 かららしい。

winget 自身のアップデートは何だかよく分からない。
ストアから入れると自動更新されるし推奨のようだが、GitHub のトップの readme に
従うのがよいのかもしれない。

<https://github.com/microsoft/winget-cli>

分かりづらいが、ストア等での名前は App Installer というらしい。
分かりづらい。

### 使い方

`winget` と入れると出てくる。

* `winget search`
  * 入れたいものがある時はまずこれでそれっぽいものを探す。
* `winget install <ID>`
  * それっぽい名前で通る気もするけど、ID をコピペするのが確実な気がする。
  IDentifier だし。
  * `--id <ID>` で ID 検索によるフィルタになるらしい。
* `winget uninstall <ID>`
* `winget list`
  * インストール済み一覧を表示する。winget を使わずに入れたものも表示されて
  びっくりするかもしれない。リポジトリに存在すればアップデートもできる。
* `winget upgrade <ID>`
  * アプリを指定しなければアップデートを確認するのみ。
  * コマンドラインから自動で安定最新版にアップデートできる。
  こういうのでいいんだよこういうので。

### winget と msstore

`winget search` するとソースの欄に `msstore` と `winget` の2つが出てくることがある。
Python の公式サイトには以下のように書いてあったりする。

> Microsoft store版は簡単かつ安全にインストールできる反面、
Python Launcher がインストールされない、
ディレクトリやレジストリへのアクセスが仮想化される、などの制限があります。
このため、アプリケーションによっては、 不具合が発生する 場合があります。

かなり怪しいことが書いてあるので、公式案内で自信満々にストア版を推奨している場合以外は
winget の方を選んだ方が無難かもしれない。

## Windows Terminal

<https://learn.microsoft.com/ja-jp/windows/terminal/install>

これも公式の解説が一番新しくて正確と思われる。

```powershell
> winget search "Windows Terminal"
名前                     ID                                バージョン   ソース
--------------------------------------------------------------------------------
Windows Terminal         9N0DX20HK701                      Unknown      msstore
Windows Terminal Preview 9N8G5RFZ9XK3                      Unknown      msstore
Windows Terminal         Microsoft.WindowsTerminal         1.19.10573.0 winget
Windows Terminal Preview Microsoft.WindowsTerminal.Preview 1.20.10572.0 winget
```

既に入っていた場合は winget upgrade してあげよう。

```powershell
> winget list Terminal
名前               ID                        バージョン   ソース
-----------------------------------------------------------------
Windows ターミナル Microsoft.WindowsTerminal 1.19.10573.0 winget
```

### winget/ストアが使えない場合

github に個別インストールパッケージがあるのでこれを利用する。\
<https://github.com/microsoft/terminal/releases>

自動更新はされないので新しくしたい場合はその都度ここを訪れる。

PreInstallKit でない普通のパッケージをダウンロードする。

1. ダブルクリックしてみる。
1. ダメなら、PowerShell で
`Add-AppxPackage Microsoft.WindowsTerminal_<versionNumber>.msixbundle`
を実行する。
1. ダメなら、Windows を新しくするか VC++ v14 Desktop Framework Package
なるものを入れてみる。
1. ダメなら、会社の PC に Windows Update がかかるのを待って再チャレンジ。

詳しくは github トップの README に書いてある。\
<https://github.com/microsoft/terminal>

実は依存先が見つからないエラーの場合は以下の手法で突破できる可能性がある。

1. <https://www.nuget.org/> へ行く。
1. 見つからないパッケージ名で検索 (例: Microsoft.UI.Xaml.2.8)
1. .NET 系ツールでのインストールコマンドが表示されているが、おそらくそんなものは
  使えない環境と思われるので、右ペインに "Download package" というリンクがある。
1. .nupkg ファイルを .zip にリネーム、展開。
1. `tools/AppX` 以下にパッケージがあるので x64 を `Add-AppxPackage` でインストール。

### 設定

タブ追加 "+" ボタンの右にある下矢印を押す (または `Ctrl+,`) と、設定画面を開ける。

* 既定のプロファイル
  * 新しいタブを開いた時に何を開くか。
  PowerShell か WSL かで好みの方を設定するとよい。
* 既定のターミナルアプリケーション
  * Windows コンソールホストというのが Ctrl+C でコピーできない古くてアレな
  conhost.exe なので、Windows Terminal にしておくと吉。
  * Windows が新しくないと出てこないかも。
* その他も一通り眺めておくと吉

### 諸事情

(読まなくても OK)

デフォルトで WSL が起動する窓は conhost.exe と言って
(※Windows 11 あたりから違うかも)、歴史的には Windows 1.01 上で
MS-DOS アプリケーションを動かすために導入されたものらしい。
cmd.exe が動くのと同じもの (※最近は以下略) で、
そういえば cmd.exe は DOS 窓と呼ばれるのでした。

conhost.exe や Windows Terminal は CUI プログラムの標準入出力を画面でやりとりする
GUI アプリケーション。
cmd.exe は CUI アプリケーション。
C あたりで printf プログラムを書いて exe を実行すると (昔は) conhost.exe で
動いていたはず(理解者理解)。

文字コードその他いろいろに関して互換性を保ちつつ改良するのが無理になったので、
Microsoft 公式オープンソースソフトウェアとして Windows Terminal が開発された。
Windows に同梱はされないが、winget/ストアで検索してポチれば OK。無料。
(※Windows 11 の新しいバージョンでは同梱され始めたかも)
ストアが使えない会社の PC 等は github にパッケージリリースがある (前述)。
conhost.exe は互換性のため以降もサポートされるが、さすがに歴史を感じすぎるので
コンソールを使う開発者はとりあえず Windows Terminal を入れておけばよさそう。

とりあえず評判はよい。
タブも使えて PowerShell も WSL も全部これでいける。
Ctrl + C でコピーできなかったのも conhost.exe のせい。これも解消する。

## WSL (Windows Subsystem for Linux)

公式ドキュメントトップ:
<https://docs.microsoft.com/ja-jp/windows/wsl/>

インストールガイド:
<https://learn.microsoft.com/ja-jp/windows/wsl/install>

WSL1 からの移行ガイドを含む。

### 概要 (理解者向け)

Windows で Linux が動く。
ユーザランドは各ディストリビューションの公式 elf バイナリがそのまま動く
(WSL1 の時はびっくりしたが WSL2 ではまあそりゃ、といった感じ)。

* WSL1
  * Linux のシステムコールを Windows Kernel の機能を利用して実現する。
  Linux Kernel は使わない。
* WSL2
  * ただの仮想マシン。WSL 用にカスタマイズされた Linux カーネルを動かす。
  * 正確には Hyper-V ハイパーバイザの上で Windows と Linux が同時に動く。

### インストール

Windows 10 の十分なバージョンまたは Windows 11 ならば wsl.exe で必要なものが
だいたい揃うようになった。
wsl.exe がない場合は winget かストアでそれっぽいものを持ってくる。

Windows Terminal でないとインストール中に盛大に文字化けしてエラーが出た場合に
何も分からないと思われるため、Windows Terminal 推奨。
(この辺りは Windows 11 からかなり改善されていると思われる)
管理者権限が必要。

```powershell
wsl --help
wsl --list --online
wsl --install [Distribution Name]
```

Distribution Name を指定しない (公式の `wsl --install` の通りに実行する) と
デフォルトで Ubuntu がインストールされるため注意(一敗)。
よく見ると下に書いてある。
どれがよいのかよくわからない人は Ubuntu が無難と思われる。
ディストリビューションの削除は --unregister コマンドでできる
(何でアンインストールじゃないんだ)。

### WSL の有効化

公式だと wsl --install が全部やってくれる風なことを書いているが、
やってくれない気もする。
wsl.exe が古いとか、WSL1 を使っていたとかだと有効化シーケンスが
走らないとかかもしれない。
Windows 11 でクリーンインストール状態から wsl.exe に任せた場合は大丈夫だった。

機能が有効化されていません的なエラーが出た場合は以下を実行する。

管理者権限で PowerShell を開き、以下を実行する。
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
このあたりは BIOS (UEFI) とか HyperVisor とかが絡んでいそうな雰囲気があるので、
何か変だったらとりあえず再起動する。

### BIOS 仮想化機能有効化

上記まででうまくいかない場合、BIOS (UEFI) で仮想化機能が無効になっている可能性がある。
確認方法は以下。

1. タスクマネージャ
1. パフォーマンス
1. CPU
1. "仮想化" の欄が有効になっているか確認

設定方法は PC によって異なる。。

1. 起動時に F2 か Delete キーあたりを連打して BIOS (UEFI) の設定画面を出す。
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
`winget upgrade` からも可能になっている気がするし、
Linux の中から `apt upgrade` もできるようにもなった気がする。

```powershell
wsl.exe --update
```

カーネルバージョン確認は WSL 内で

```sh
$ uname -r
5.15.167.4-microsoft-standard-WSL2
```

### WSL1 からの移行 (または 1 に戻す)

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

### Tab 自動補完時のビープ音がうるさい

`/etc/inputrc` を編集。

```sh
# uncomment
set bell-style none
```

### 一部ディレクトリの色が見づらい

Windows Terminal ならデフォルト背景色がちょっと明るい黒になり、解決する。

conhost.exe だと黒地に濃い青は見えない。

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

.bashrc の以下の行が設定箇所。

```bash
if [ "$color_prompt" = yes ]; then
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
```

34(blue) を例えば 36(cyan) にする。
