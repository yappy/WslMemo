# Debian Memo

DEBIAN JP Project\
<https://www.debian.or.jp/index.html>

## apt の使い方

`apt` は従来の `apt-get` `apt-cache` をユーザフレンドリーにラップしたもの。
プログレスバーが出たりする。
公式的には人間が扱うなら `apt`、シェルスクリプト等から使うなら `apt-get` 推奨らしい。

日々のメンテ

* `apt update`
  * パッケージ一覧を最新の情報に更新。デイリーチェック。
    `sources.list` を書き換えた場合にも実行。
* `apt upgrade`
  * 更新があったらこれで。
* `apt full-upgrade`
  * 主にディストリビューションのバージョンアップ用。
  * 必要に応じてパッケージの削除も行うらしい？
* `apt autoremove`
* `apt autoremove --purge`
* `apt autopurge`
  * upgrade 後に言われたら。依存が無くなって不要になったパッケージを削除する。
  * purge は設定ファイルも消す。

インストール / アンインストール

* `apt list <query>`
  * パッケージ名検索。
* `apt search <query>`
  * 説明文から検索。
* `apt show <pkg>`
  * パッケージの詳細な説明を表示。
* `apt install <pkg>`
  * インストール。
* `apt remove <pkg>`
* `apt remove --purge <pkg>`
* `apt purge <pkg>`
  * アンインストール。
  * purge は設定ファイルも消す。

`dkpg` は `apt` が内部で使用している、より低レベルなパッケージ管理プログラム。
debian-package。
依存関係の解決機能がない。

そのパッケージでインストールされたファイルパスリストを表示

* `dpkg -L <pkg>`
  * ~~なんで apt でできないんだ~~

Debian Package は `*.deb` の形をしている。
このファイルを直接インストールしたい場合は相対パスを使って

* `apt install ./pkg.deb`

## apt で main 以外も使う

`/etc/apt/sources.list` を書き換える。

参考: <https://debian-handbook.info/browse/ja-JP/stable/apt.html#sect.apt-sources.list.stable>

Debian フリーソフトウェアガイドラインに適合したもののみを使いたいわけではないなら
contrib, non-free を追加する。

bookworm から non-free-firmware も増えた気がする。

## apt ソースを日本のミラーサイトにする

こっちの方がアップデートが速い。
なんとなくセキュリティに関してはそのままにする。
参考: <https://www.debian.or.jp/using/mirror.html>

`deb http://ftp.jp.debian.org/debian <version> main contrib non-free non-free-firmware`

Raspberry Pi は何もしなくても自動で日本のサーバを見に行くようになった気がする。
他は謎。

## debian-backports を追加する

`deb http://ftp.jp.debian.org/debian <version>-backports main contrib non-free non-free-firmware`

stable に入っているバージョンが古く、新しいものを使いたいときに。
新しいバージョンを stable の古いライブラリでビルドしたものが置いてある。
なんか最初から入っているようになったような気もする。

デフォルトではインストールされないので安心。
`-t` オプションで指定インストールできる。

`apt show -a <pkg>`

`apt install -t <version>-backports <pkg>`

## Debian をバージョンアップする

### 現在のバージョンを確認

番号とコードネームの対応は全く覚えられない。

```sh
$ cat /etc/debian_version
12.5
```

こちらだとよく分かる。

```sh
$ cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```

### リリースされているバージョンのコードネームを確認

日本語のページは古くて追従できていない。

<https://www.debian.org/releases/index.en.html>

### apt source の書き換え

`/etc/apt/sources.list` を開き、コードネームの部分をすべて置き換える。

例 (bullseye => bookworm)

```text
# deb http://ftp.jp.debian.org/debian bullseye ...
deb http://ftp.jp.debian.org/debian bookworm ...
```

その後、`apt update`。

### バックアップ

**必ずバックアップを取ること。**(一敗)

ホームディレクトリを丸ごとアーカイブして Windows のファイルシステム上に
置いておけば大体何とかなる。
`/etc` 以下は諸説あり。

壊れてしまったら `wsl.exe --unregister` で仮想マシンごと削除して、
新しいバージョンの Debian を新規インストールしたところに
バックアップをホームディレクトリに展開すれば OK。
むしろこっちの方がすっきりするかも。

### アップグレード

次のように分けて行うと安全度が増すらしい(公式より)。

```sh
apt upgrade --without-new-pkgs
apt full-upgrade
```
