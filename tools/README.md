# 便利ツール集

## Linux

### archive.py - ディレクトリをアーカイブしてバックアップ

```sh
# ホームディレクトリを固めて Windows の D ドライブに保存
./archive.py ~ /mnt/d/wsl
```

指定したディレクトリをまるごと tar.bz2 圧縮し、
現在日時やホスト名からいい感じのファイル名をつけ、指定したディレクトリに保存する。
いったん /tmp に tar.bz2 を出力し、最後に指定したディレクトリにコピーする。

WSL をまるごとバックアップするなら `wsl.exe --export` が存在するが、
少なくとも WSL では大抵の場合ホームディレクトリをコピーすれば事足りると思われる。
別 PC への引っ越し、バージョンアップ (`apt full-upgrade`) 前のバックアップに。

### allclean.py - 生成物をすべて clean

```sh
$ ./allclean.py --help
usage: allclean.py [-h] [--make] [--cargo] root

Find build file and clean

positional arguments:
  root        root dir

options:
  -h, --help  show this help message and exit
  --make      Find **/Makefile and `make clean`
  --cargo     Find **/Cargo.toml and `cargo clean`

$ ./allclean.py --make --cargo ~
```

C/C++ や Rust のビルド生成物が多すぎる時に。
バックアップや仮想ディスクの最適化前に。

※cargo clean はともかく make clean はものによっては危険かもしれないので自己責任で。

## Windows
