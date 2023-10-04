# おすすめ Debian パッケージ

## 欲しい

なんで最初から入ってないんだシリーズ (Ubuntu じゃないからかもしれない。。)

* bash-completion
* less

いざというときないとイラっとくるシリーズ

* curl (Web API を叩くかもしれない人向け。ダウンロードは wget で。)

人類は C 言語から逃れることはできないシリーズ

* build-essential (C/C++ 基本セット。欲しいかは人による。)

## 最新版 (backport) が欲しい (ことがある)

`sudo apt install -t <version>-backports <package>`

古いのでいいなら通常インストールでよい。

* git

## PPA を追加する場合

* software-properties-common (for apt-add-repository)
* dirmngr (for apt-add-repository)
