# Debian Memo

DEBIAN JP Project\
<https://www.debian.or.jp/index.html>

## apt で main 以外も使う

`/etc/apt/sources.list` を書き換える。

参考: <https://debian-handbook.info/browse/ja-JP/stable/apt.html#sect.apt-sources.list.stable>

Debian フリーソフトウェアガイドラインに適合したもののみを使いたいわけではないなら
contrib, non-free を追加する。

## apt ソースを日本のミラーサイトにする

こっちの方がアップデートが速い。
なんとなくセキュリティに関してはそのままにする。
参考: <https://www.debian.or.jp/using/mirror.html>

`deb http://ftp.jp.debian.org/debian <version> <main|contrib|non-free>...`

Raspberry Pi は何もしなくても自動で日本のサーバを見に行くようになった気がする。
他は謎。

## debian-backports を追加する

`deb http://ftp.jp.debian.org/debian <version>-backports main contrib non-free`

stable に入っているバージョンが古く、新しいものを使いたいときに。
git や cmake など。
新しいバージョンを stable の古いライブラリでビルドしたものが置いてある。
デフォルトではインストールされないので安心。
`-t` オプションで指定インストールできる。

`apt show -a <pkg>`

`apt install -t <version>-backports <pkg>`

## 32 bit ELF の実行 (マニアックな作業向け)

準備が整っていない場合のエラーが ENOENT になるようで、エラーメッセージが分かりにくい。

<https://askubuntu.com/questions/454253/how-to-run-32-bit-app-in-ubuntu-64-bit>

```sh
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386
sudo apt-get install multiarch-support
```
