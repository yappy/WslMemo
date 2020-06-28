# WslMemo
WSL (Windows Subsystem for Linux) の覚え書き。
最初にやることリスト。

## 一部ディレクトリの色が見づらい
黒地に濃い青は見えない。

.bashrc でホームディレクトリに `.dircolors` ファイルがあればそれを使うように
なっているようなので、github から有名どころの色設定を頂いてきて
シンボリックリンクを張る。

```
git clone https://github.com/mavnn/mintty-colors-solarized
# 個人的には dircolors.256dark がおすすめ
ln -s dircolors-solarized/dircolors.<you_like> ~/.dircolors
source ~/.bashrc
```

ちなみに clone した中で `sudo make`
(sudo しないと作れない種類のファイルがあるっぽい)
するとテスト用のファイルセットの入ったディレクトリを作ってくれる。


## プロンプトのカレントディレクトリが見づらい
.bashrc の以下の行が設定箇所。

```
if [ "$color_prompt" = yes ]; then
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
```

34(blue) を例えば 36(cyan) にする。


## Tab 自動補完時のビープ音がうるさい
`/etc/inputrc` を編集。
```
# uncomment
set bell-style none
```
