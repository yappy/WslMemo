# systemd

## 公式ドキュメント

<https://learn.microsoft.com/ja-jp/windows/wsl/systemd>

## 概要

カーネルの初期化後に初めて作られるユーザプロセス (PID = 1)。
そこから先のシステム全体の起動、および動作中のサービス管理を行う。
古くは init (process) が使われていたが、
最近の Linux ではより現代的な systemd に置き換えられている。

init は run level とか言っていたやつ (多分 systemd でも互換機能提供はしている) で、
`/etc/init.d` とかに名前が残っている。
設計が古くシーケンシャルなので、最近のマルチコアが生かせず起動が遅い原因にもなっていた。
systemd は根本から並列設計でそこは解消されているものの、
依存性をしっかり宣言しないと壊れる可能性がある。

## systemd on WSL2

最近の Ubuntu (WSL2 のデフォルトでもある) ではデフォルト有効になっているらしい。

```sh
$ systemctl

System has not been booted with systemd as init system (PID 1). Can't operate.
Failed to connect to bus: Host is down
```

`systemctl` コマンドが変なエラーを吐く場合は有効化されていない。
その場合は

1. `/etc/wsl.conf` を開き、下記の行を追加する。
1. `wsl.exe --shutdown` で VM を終了させ、再度 WSL を開いて再起動する。

```ini
[boot]
systemd=true
```

これでシステムデーモン的なもの (常駐ソフトウェア) を利用可能になる。

* SSH Server (sshd)
* cron
* docker

## Windows からの自動起動

`systemctl enable <service>` でシステム起動時に任意のプログラムを
自動起動するようにできるし、systemd のタイマ機能や cron を使えば
定期的なプログラム実行をできるが、それは VM + Linux が起動している間のみの話である。

WSL 自体を自動起動するのは Windows の仕組みで行う必要がある。
逆にそれさえしてしまえば後は systemd にすべて任せられる。

Windows の cron みたいなシステムが "タスクスケジューラ" である。
コマンドラインツールもあるが、なんか設定可能項目が少ない気がするので
GUI 推奨かもしれない…。

Windows 上で wsl.exe のフルパスを得るには `where.exe` がよい。

```sh
$ where.exe wsl
C:\Windows\System32\wsl.exe
C:\Users\(USER)\AppData\Local\Microsoft\WindowsApps\wsl.exe
```

1. Windows Key
1. そのままキーボード入力で検索できるので、"task" とか入れる。
1. "タスクスケジューラ" を開く。タスクマネージャーではない。
1. タスクスケジューラ(ローカル) > タスクスケジューラライブラリ 以下にフォルダ構造で
  整理されているので、いい感じにフォルダを作る。
