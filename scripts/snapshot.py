#!/usr/bin/env python3
"""Refresh an explicit allowlist of dotfiles; never copy application profiles."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIGS = [
    "hypr", "caelestia", "foot", "kitty", "btop", "cava", "fuzzel",
    "gtk-3.0", "gtk-4.0", "htop", "nvtop", "qtengine", "zed/themes",
    "nwg-displays/config", "dolphinrc", "starship.toml",
]
NVIM = ["init.lua", "lazy-lock.json", "lua", "README.md", "BINDINGS.md", "prettierrc.json", ".prettierrc.json"]
THEMES = ["BetterDiscord", "Vencord", "Equicord", "legcord", "vesktop", "equibop"]
EXCLUDED = {".git", "__pycache__", ".DS_Store", "node_modules", "machine.lua", "machine.env"}


def copy(source, dest):
    if not source.exists():
        return
    if source.is_dir():
        for item in sorted(source.iterdir()):
            if item.name not in EXCLUDED:
                copy(item, dest / item.name)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Dereference generated theme links; don't export absolute home symlinks.
        shutil.copy2(source, dest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--wallpapers", action="store_true")
    parser.add_argument("--refresh", action="store_true", help="Permit replacing existing snapshots")
    args = parser.parse_args()
    if (ROOT / "config").exists() and not args.refresh:
        parser.error("config/ already exists; use --refresh after reviewing local repository edits")
    home = args.home.resolve()
    for name in CONFIGS:
        copy(home / ".config" / name, ROOT / "config" / name)
    for name in NVIM:
        copy(home / ".config/nvim" / name, ROOT / "config/nvim" / name)
    if not (home / ".config/nvim/.prettierrc.json").exists():
        copy(home / ".config/nvim/prettierrc.json", ROOT / "config/nvim/.prettierrc.json")
    for name in dict.fromkeys(THEMES):
        copy(home / ".config" / name / "themes", ROOT / "config" / name / "themes")
    copy(home / ".config/spicetify/Themes", ROOT / "config/spicetify/Themes")
    for name in [".zshrc", ".zprofile", ".bashrc", ".bash_profile"]:
        copy(home / name, ROOT / "home" / name)
    copy(home / ".local/state/caelestia/scheme.json", ROOT / "assets/caelestia-scheme.json")
    if args.wallpapers:
        folder = home / "Pictures/Wallpapers"
        if folder.is_dir():
            for image in sorted(folder.iterdir()):
                if image.is_file() and image.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                    copy(image, ROOT / "wallpapers" / image.name)
        current = home / ".local/state/caelestia/wallpaper/path.txt"
        if current.exists():
            name = Path(current.read_text().strip()).name
            if (ROOT / "wallpapers" / name).is_file():
                (ROOT / "assets/wallpaper.json").write_text(json.dumps({"file": name}, indent=2) + "\n")
    # Include a dependency snapshot as a reference, not a blind installation list.
    try:
        result = subprocess.run(["pacman", "-Q"], check=True, capture_output=True, text=True)
        (ROOT / "packages").mkdir(exist_ok=True)
        (ROOT / "packages/current-versions.txt").write_text(result.stdout)
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    from normalize import normalize
    normalize()
    print(f"Snapshot copied to {ROOT}. Review changes before publishing.")


if __name__ == "__main__":
    main()
