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

## 仮想ディスクの掃除

WSL2 になりただの仮想マシンとなってしまったため、ゲスト OS 上でファイルを消しても
仮想ディスクファイルが大きくなったまま戻らない。
docker を連打した、事故ってクソデカファイルを作ってしまった、
いつの間にか肥大化していた、等の場合。

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

WSL はシャットダウン状態でシェルを開こうとすると自動的に起動する。

## 移行 or バックアップ/リストア

```powershell
wsl.exe --export
wsl.exe --import
```

で可能らしい。(未検証)
