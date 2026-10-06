# Oni's dotfiles

My configs and a small installer so I don't have to set everything up from scratch
on a new computer, VM, or server.

Mostly built around Arch Linux / Arch Linux ARM: Neovim, Zsh + Starship,
Foot, and a Hyprland desktop with Caelestia. Also includes wallpapers and
matching app themes.

## Install

On a fresh Arch install, get the system and graphics drivers ready first, then
run this as your normal user with sudo access:

```bash
sudo pacman -Syu --needed git python
git clone https://github.com/judeo-s/dotfiles.git ~/dotfiles
cd ~/dotfiles
bash install.sh
```

This upgrades the system, installs packages (including Caelestia through the AUR),
backs up existing configs, copies mine into place, and installs Neovim plugins.
Expect a few prompts during the AUR builds.

For a server or a machine where I only want the shell or editor:

```bash
bash install.sh --config-only --only shell
bash install.sh --config-only --only nvim
```

Config-only installs need Python 3.11+ and the relevant apps already installed.
They can also be used on other Linux distributions.

## A few useful options

```bash
# Preview the files that would be copied
bash install.sh --dry-run

# Copy everything without installing packages or Neovim plugins
bash install.sh --config-only --skip-plugins

# VirGL VM (my Apple M4 setup)
bash install.sh --graphics virgl --monitor-mode '1920x1080@60'

# Physical hardware, with a custom display scale
bash install.sh --graphics native --monitor-scale 1.5

# Make Zsh the login shell
bash install.sh --set-shell
```

The config groups are `desktop`, `nvim`, `shell`, and `themes`.
Use `--config-only` with `--only`. Run `bash install.sh --help` for all options.

## Desktop setup

Log out and select Hyprland, or log in from a TTY—the included shell profiles
can start it through UWSM. To start Caelestia manually inside Hyprland:

```bash
sh ~/.config/caelestia/start.sh
```

Monitor settings live in `~/.config/hypr/machine.lua`. New installs use the
preferred resolution at scale 1; later installs keep those settings unless
you pass a monitor option. The VirGL setting lives in
`~/.config/caelestia/machine.env`.

The main shortcuts I use are Super + Enter for Foot, Super + Space for the
launcher, Super + A for the dashboard, and Super + 1–0 for workspaces.
Neovim shortcuts are in [config/nvim/BINDINGS.md](config/nvim/BINDINGS.md).

## Backups

Existing configs are saved in `~/.local/share/dotfiles-backups/`.
The installer prints the backup manifest path. To restore one, from this repo:

```bash
python scripts/deploy.py --restore "$HOME/.local/share/dotfiles-backups/TIMESTAMP/manifest.json"
```

Restore the newest backup first. Any edits made since installation are saved
in its `after-install/` folder. Restoring configs doesn't uninstall packages.

## Updating this repo

Configs are copied, not symlinked. After changing my live setup, I pull the
configs back into the repo with:

```bash
python scripts/snapshot.py --refresh --wallpapers
python scripts/check.py
git diff
```

Leave out `--wallpapers` to just refresh configs. The snapshot only picks up
the selected configs and themes, not app profiles, credentials, or histories.

## Credits

- [Caelestia](https://github.com/caelestia-dots/shell) for the desktop shell.
- [R7rainz/neovim-conf](https://github.com/R7rainz/neovim-conf) for the Neovim dashboard layout.

Included themes, wallpapers, and plugins belong to their respective authors.
