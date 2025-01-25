# 便利ツール集

## Windows

### vhdx.py

WSL2 の仮想ディスクファイルサイズを最適化します。

* Windows 専用
  * Windows 版 python が必要。
* 管理者権限が必要
  * diskpart の実行のため。
  * vhdx ファイルの検索には不要。

```powershell
py vhdx.py -h
py vhdx.py find -h
py vhdx.py compact -h
```

#### vhdx.py find

```powershell
py vhdx.py find [--dir DIR]
```

仮想ディスクファイル (ext4.vhdx) を検索する。
通常は環境変数 `%LocalAppData%` 内にあるのでデフォルトではそこを検索する。
`--dir` は通常指定する必要はない。

#### vhdx.py compact

```powershell
py vhdx.py compact VHDX
```

指定した仮想ディスクファイルのサイズを最適化する。
`wsl.exe --shutdown` で全仮想マシンを停止させた後、
テンポラリファイルとして `diskpart` スクリプトを作成し、実行する。
ファイル名には `vhdx.py find` の結果をコピペすればよい。

### vhdx_(cmd).bat

`vhdx.py` のバッチファイル版です。
バッチファイルの制約により出力がやや不親切ですが、
Windows 版 python がなくても動きます。
管理者権限も自動で要求します。

#### vhdx_find.bat

#### vhdx_compact.bat

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
