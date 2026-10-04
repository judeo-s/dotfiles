#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /etc/os-release
if [[ "${ID:-}" != arch && "${ID:-}" != archarm && " ${ID_LIKE:-} " != *" arch "* ]]; then
    printf 'Package installation supports Arch/Arch ARM. Use --config-only elsewhere.\n' >&2
    exit 1
fi
if (( EUID == 0 )); then
    printf 'Run as your normal user; this script invokes sudo when required.\n' >&2
    exit 1
fi
mapfile -t packages < <(awk 'NF && $1 !~ /^#/ {print $1}' "$ROOT/packages/arch.txt")
sudo pacman -Syu --needed "${packages[@]}"

cache="${XDG_CACHE_HOME:-$HOME/.cache}/dotfiles-build"
mkdir -p "$cache"
if command -v paru >/dev/null 2>&1; then
    helper=paru
elif command -v yay >/dev/null 2>&1; then
    helper=yay
else
    [[ -d "$cache/paru/.git" ]] || git clone https://aur.archlinux.org/paru.git "$cache/paru"
    (cd "$cache/paru"; makepkg --syncdeps --install --needed)
    helper=paru
fi

# Two Caelestia dependencies have x86-only AUR metadata but compile on ARM.
# Build from source with real dependencies; never use --nodeps or ignorearch.
if [[ "$(uname -m)" == aarch64 ]]; then
    for package in libcava python-materialyoucolor; do
        if pacman -Q "$package" >/dev/null 2>&1; then
            continue
        fi
        directory="$cache/$package"
        [[ -d "$directory/.git" ]] || git clone "https://aur.archlinux.org/$package.git" "$directory"
        python3 "$ROOT/scripts/patch-aur.py" "$directory/PKGBUILD"
        (cd "$directory"; env LC_ALL=C.UTF-8 makepkg --syncdeps --install --needed)
    done
fi
"$helper" -S --needed caelestia-shell

mapfile -t tools < <(awk 'NF && $1 !~ /^#/ {print $1}' "$ROOT/packages/editor-tools.txt")
sudo pacman -S --needed "${tools[@]}"
# CSS/HTML/JSON language servers are npm-distributed; use a user-owned prefix.
npm install --global --prefix "$HOME/.local" vscode-langservers-extracted yaml-language-server
printf '\nPackages installed. Optional language tools can also be managed via :Mason.\n'
