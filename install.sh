#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
config_only=0
dry_run=0
only=all
graphics=auto
mode=""
scale=""
plugins=1
shell_default=0
while (($#)); do
    case "$1" in
        --config-only) config_only=1; shift ;;
        --dry-run) dry_run=1; shift ;;
        --only) only="${2:?Missing group}"; shift 2 ;;
        --graphics) graphics="${2:?Missing graphics mode}"; shift 2 ;;
        --monitor-mode) mode="${2:?Missing mode}"; shift 2 ;;
        --monitor-scale) scale="${2:?Missing scale}"; shift 2 ;;
        --skip-plugins) plugins=0; shift ;;
        --set-shell) shell_default=1; shift ;;
        -h|--help)
            printf '%s\n' 'Usage: bash install.sh [options]' \
                '  --config-only          Copy configs without installing packages' \
                '  --dry-run              Print planned copies; make no changes' \
                '  --only GROUP           all, desktop, nvim, shell, themes' \
                '                         Partial installs require --config-only' \
                '  --graphics MODE        auto, virgl, native (default: auto)' \
                '  --monitor-mode MODE    preferred or e.g. 1920x1080@60' \
                '  --monitor-scale SCALE  Positive display scale' \
                '                         Existing machine settings are preserved unless overridden' \
                '  --skip-plugins         Skip Neovim plugin installation' \
                '  --set-shell            Set your login shell to Zsh using chsh'
            exit 0 ;;
        *) printf 'Unknown option: %s\n' "$1" >&2; exit 2 ;;
    esac
done
[[ "$only" =~ ^(all|desktop|nvim|shell|themes)$ ]] || { printf 'Invalid group\n' >&2; exit 2; }
[[ "$graphics" =~ ^(auto|virgl|native)$ ]] || { printf 'Invalid graphics mode\n' >&2; exit 2; }
if [[ "$only" != all && "$config_only" != 1 && "$dry_run" != 1 ]]; then
    printf 'Use --config-only with partial installs.\n' >&2; exit 2
fi
if (( EUID == 0 )); then
    printf 'Run as your normal user, not root.\n' >&2; exit 1
fi
args=(--only "$only" --graphics "$graphics")
[[ -z "$mode" ]] || args+=(--monitor-mode "$mode")
[[ -z "$scale" ]] || args+=(--monitor-scale "$scale")
if (( dry_run )); then
    python3 "$ROOT/scripts/deploy.py" "${args[@]}" --dry-run
    exit
fi
# Validate options before any package installation or backup changes.
python3 "$ROOT/scripts/deploy.py" "${args[@]}" --dry-run >/dev/null
if (( ! config_only )); then
    bash "$ROOT/scripts/packages.sh"
fi
if (( shell_default )) && ! command -v zsh >/dev/null 2>&1; then
    printf '%s\n' '--set-shell requires Zsh to be installed.' >&2
    exit 1
fi
python3 "$ROOT/scripts/deploy.py" "${args[@]}"
export PATH="$HOME/.local/bin:$PATH"
if (( plugins )) && [[ "$only" == all || "$only" == nvim ]]; then
    if command -v nvim >/dev/null 2>&1; then
        # restore honours the committed lazy-lock.json rather than updating everything.
        DOTFILES_NVIM_BOOTSTRAP="$ROOT/scripts/bootstrap-nvim.lua" \
            nvim --headless '+lua dofile(vim.env.DOTFILES_NVIM_BOOTSTRAP)'
    else
        printf 'Neovim not found; install it, then run :Lazy restore.\n' >&2
    fi
fi
if (( shell_default )); then
    chsh -s "$(command -v zsh)"
fi
printf '\nInstalled config group: %s\n' "$only"
if [[ "$only" == all || "$only" == desktop ]]; then
    printf 'Log out and start Hyprland to activate the desktop.\n'
    printf 'Start Caelestia manually: sh ~/.config/caelestia/start.sh\n'
    printf 'Optional network service: sudo systemctl enable --now NetworkManager\n'
fi
