#!/bin/bash

set -euxo pipefail

sudo apt upgrade --update

rustup update
cargo install-update --all

brew update
brew upgrade
brew cleanup

# Do at last because it causes WSL shutdown
wsl.exe --update
