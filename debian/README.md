# Debian Memo

DEBIAN JP Project\
<https://www.debian.or.jp/index.html>

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
