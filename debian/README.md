# Debian Memo
DEBIAN JP Project
https://www.debian.or.jp/index.html


## apt で main 以外も使う
/etc/apt/sources.list を書き換える。

参考: https://debian-handbook.info/browse/ja-JP/stable/apt.html#id-1.9.10.6

Debian フリーソフトウェアガイドラインに適合したもののみを使いたいわけではないなら
contrib, non-free を追加する。


## apt ソースを日本のミラーサイトにする
こっちの方がアップデートが速い。
なんとなくセキュリティに関してはそのままにする。
参考: https://www.debian.or.jp/using/mirror.html

`deb http://ftp.jp.debian.org/debian <version> <main|contrib|non-free>...`


## debian-backports を追加する
`deb http://ftp.jp.debian.org/debian <version>-backports main contrib non-free`

stable に入っているバージョンが古く、新しいものを使いたいときに。
git や cmake など。
新しいバージョンを stable の古いライブラリでビルドしたものが置いてある。
デフォルトではインストールされないので安心。
`-t` オプションで指定インストールできる。

`apt show -a <pkg>`

`apt install -t <version>-backports <pkg>`
