# WSL

ここに既にいろいろ書いてあるような気もする。

<https://learn.microsoft.com/ja-jp/windows/wsl/filesystems>

## Windows ファイルの実行

Linux の中から `.exe` を省略せずにコマンドを打つと、不思議な力が働いて
Windows のファイルを実行することができる。
これを使うと WSL 内から `wsl.exe` を呼ぶことも可能。

## Linux ファイルシステムを Windows エクスプローラで開く

エクスプローラの左ペインをよく見ると Linux が増えている。
OS 間のファイルの転送も楽。

exe の実行を応用して、以下のコマンドで Linux カレントディレクトリを
エクスプローラで表示することが可能。

```sh
# In Linux
explorer.exe .
```

## Windows ファイルシステムを Linux から開く

`/mnt` 以下に Windows ファイルシステムのドライブがマウントされている。
パーミッションの挙動に制約がある感じがするので、可能ならこの中で作業するのは
避けたほうがよい気がする。

```sh
# C drive
cd /mnt/c
```

## Linux GUI アプリ

<https://learn.microsoft.com/ja-jp/windows/wsl/tutorials/gui-apps>

実はいつの間にか実行できるようになっている。
新しいバージョンの Windows と WSL で実行するだけ。

## Windows のメモリが枯渇する

いきなり Windows 側でメモリ不足のエラーが出てびっくりする。
タスクマネージャを見ると Vmmem というタスクが大量のメモリを食っている。

原因は Linux のファイルシステムのキャッシュ。
元来 OS はメモリのある限りファイル I/O の結果はキャッシュとしてメモリに残して
おこうとするが、
WSL ではそれをハイパーバイザでハンドルして動的に割り当てる。
キャッシュ領域はメモリが足りなくなった時に解放されその目的のために使用されるが、
それは Linux の中での話で Windows でメモリが足りなくなった時に
Linux のキャッシュを解放してもらうような仕組みにはなっていない。

### wsl を再起動する

なんやかんやでこれが一番簡単。

```sh
wsl.exe --shutdown
```

### キャッシュを捨てる

デバイスファイルに数字を書き込むとファイルシステムのキャッシュをコントロールできる。
(vm は Virtual Machine ではなく Virtual Memory。
ハイパーバイザとは関係なく、OS の仮想メモリ管理システム。)

```sh
sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"
```

### WSL 用のメモリ上限を設定する

`%USERPROFILE%\.wslconfig`

```txt
[wsl2]
memory=6GB
```

昔は搭載メモリの 80% がデフォルトだったが、Build 20175 からは
`min(physical / 2, 8GiB)` がデフォルトらしい。
80% は Windows 側がやばい気もするけど、思いっきり使わせたい時もあるだろうから
難しいところ。

```sh
# Physical Memory 16 GiB
$ free -h
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       2.4Gi       5.4Gi       2.4Mi       145Mi       5.4Gi
Swap:          2.0Gi       1.0Mi       2.0Gi
```

Linux からは (仮想化された) 物理メモリとファイルシステムキャッシュは
`free` コマンドで見れる。
free が本当に全く使っていない空きメモリで、available がいざとなったらキャッシュを
追い出して使える分も含めた利用可能メモリ。

### autoMemoryReclaim

<https://learn.microsoft.com/ja-jp/windows/wsl/wsl-config>

experimental の autoMemoryReclaim で CPU があまり使われていないのを検出した時に
自動でメモリを返すようにできる、らしい。
ただし gradual に設定すると cgroup v2 が有効になるため、v1 に依存した
システムが不具合を起こすかもしれない、らしい。
いつ experimental を脱却するのかも不明。もうしているかもしれない。

## 仮想ディスクの掃除

WSL2 になりただの仮想マシンとなってしまったため、ゲスト OS 上でファイルを消しても
仮想ディスクファイルが大きくなったまま戻らない。
docker を連打した、事故ってクソデカファイルを作ってしまった、
いつの間にか肥大化していた、等の場合。

[Python スクリプトを用意しました](./tools/README.md)

Microsoft の github に issue が上がっている。

<https://github.com/microsoft/WSL/issues/4699>

Optimize-VHD コマンドでコンパクション可能だそうだが、Windows Pro でないと存在しない。
diskpart コマンドなら Windows Home でも存在する。

1. %LocalAppData% 内で `ext4.vhdx` を検索し、パスを得る。
ファイルを Shift + 右クリックで "パスのコピー" ができる。
1. PowerShell を管理者権限で立ち上げる。
Windows + R でファイル名を指定して実行。この時 Ctrl + Shift + Enter で決定すると
管理者権限で実行できる。
1. 以下のように仮想マシンをシャットダウンしてから diskpart コマンドで
コンパクションを行う。

```powershell
wsl --shutdown
diskpart
# open window Diskpart
select vdisk file="C:\...\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

`diskpart /s <script>` であらかじめ用意したコマンドスクリプトを実行することも
できるらしい。

WSL はシャットダウン状態でシェルを開こうとすると自動的に起動する。

## 移行 or バックアップ/リストア

```powershell
wsl.exe --export
wsl.exe --import
```

で可能らしい。(未検証)
