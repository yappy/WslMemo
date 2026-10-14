#!/bin/bash

set -euxo pipefail

has_command() {
    if command -v "$1" >/dev/null 2>&1; then
        return 0
    fi
    echo "Warning: $1 not found" >&2
    return 1
}

if has_command apt; then
    sudo apt upgrade --update
fi

if has_command rustup; then
    rustup update
fi
if has_command cargo && has_command cargo-install-update; then
    cargo install-update --all
fi

if has_command brew; then
    brew update
    brew upgrade
    brew cleanup
fi

# Do at last because it causes WSL shutdown
if has_command wsl.exe; then
    wsl.exe --update
fi
