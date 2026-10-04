#!/usr/bin/env python3
"""Validate shareable configs and installer syntax without deploying them."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SECRET = re.compile(r"-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{30,}")


def main():
    count = 0
    folders = [ROOT / name for name in ("config", "home", "scripts", "templates", "tests")]
    paths = [ROOT / "install.sh"]
    for folder in folders:
        if folder.exists():
            paths.extend(p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for path in paths:
        if path.is_symlink():
            raise SystemExit(f"Snapshot contains a symlink: {path}")
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".woff", ".woff2", ".ttf"}:
                continue
            raise
        if SECRET.search(text):
            raise SystemExit(f"Possible credential in {path}")
        if path.is_relative_to(ROOT / "config") or path.is_relative_to(ROOT / "home"):
            if "/home/oni" in text:
                raise SystemExit(f"Nonportable home path in {path}")
        if path.suffix == ".json":
            json.loads(text)
        elif path.suffix == ".toml":
            tomllib.loads(text)
        elif path.suffix == ".py":
            compile(text, str(path), "exec")
        elif path.suffix == ".sh" or path.name in {".bashrc", ".bash_profile"}:
            subprocess.run(["bash", "-n", str(path)], check=True)
        elif path.suffix == ".lua" and shutil.which("lua"):
            subprocess.run(["lua", "-e", f"assert(loadfile({json.dumps(str(path))}))"], check=True)
        elif path.name in {".zshrc", ".zprofile"} and shutil.which("zsh"):
            subprocess.run(["zsh", "-n", str(path)], check=True)
        count += 1
    lock = json.loads((ROOT / "config/nvim/lazy-lock.json").read_text())
    assert {"alpha-nvim", "alpha-ascii.nvim", "nvim-treesitter"} <= lock.keys()
    print(f"Validated {count} text files; Neovim lockfile included.")


if __name__ == "__main__":
    main()
