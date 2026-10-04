#!/usr/bin/env python3
"""Install copied configs with a timestamped, restorable backup manifest."""
import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DESKTOP = {"hypr", "caelestia", "fuzzel", "gtk-3.0", "gtk-4.0", "qtengine", "nwg-displays", "dolphinrc"}
SHELL = {"foot", "kitty", "starship.toml", "btop", "cava", "htop", "nvtop"}


def exists(path):
    return path.exists() or path.is_symlink()


def config_group(name):
    if name == "nvim":
        return "nvim"
    if name in DESKTOP:
        return "desktop"
    if name in SHELL:
        return "shell"
    return "themes"


def detect_virgl():
    try:
        result = subprocess.run(["glxinfo", "-B"], capture_output=True, text=True, timeout=10)
        return "virgl" in result.stdout.lower()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def write_manifest(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def machine_settings(home, args):
    settings = home / ".config/caelestia/machine.env"
    previous = None
    if settings.is_file():
        match = re.search(r"^CAELESTIA_VIRGL_WORKAROUND=(0|1)$", settings.read_text(), flags=re.M)
        if match:
            previous = match[1] == "1"
    if args.graphics == "auto":
        enabled = previous if previous is not None else detect_virgl()
    else:
        enabled = args.graphics == "virgl"
    display = home / ".config/hypr/machine.lua"
    old = display.read_text() if display.is_file() else None
    if old is not None and args.monitor_mode is None and args.monitor_scale is None:
        monitor = old
    elif old is not None:
        # Keep output names and other local choices when overriding mode/scale.
        monitor = "local machine = (function()\n" + old + "\nend)()\n"
        if args.monitor_mode is not None:
            monitor += f"machine.mode = {json.dumps(args.monitor_mode)}\n"
        if args.monitor_scale is not None:
            monitor += f"machine.scale = {args.monitor_scale}\n"
        monitor += "return machine\n"
    else:
        mode = args.monitor_mode or "preferred"
        scale = args.monitor_scale if args.monitor_scale is not None else 1
        monitor = (
            "-- Machine-local display settings.\n"
            f"return {{ mode = {json.dumps(mode)}, scale = {scale} }}\n"
        )
    return enabled, monitor


def preflight(items, home):
    for source, relative in items:
        target = home / relative
        if ROOT.is_relative_to(target.resolve()):
            raise SystemExit(f"Repository is inside a destination being replaced: {target}")
        if isinstance(source, Path) and not source.exists():
            raise SystemExit(f"Missing snapshot source: {source}")
        ancestor = target.parent
        while not exists(ancestor):
            ancestor = ancestor.parent
        if not ancestor.is_dir():
            raise SystemExit(f"Destination parent is not a directory: {ancestor}")


def restore(manifest_path, home, dry_run):
    manifest_path = manifest_path.resolve()
    data = json.loads(manifest_path.read_text())
    if Path(data["home"]).resolve() != home:
        raise SystemExit("Backup belongs to a different home directory")
    if (manifest_path.parent / "RESTORED").exists():
        raise SystemExit("This backup has already been restored")
    pending = []
    # Check the entire backup before restoring anything, not partway through.
    for entry in reversed(data["entries"]):
        if entry.get("restored"):
            continue
        relative = Path(entry["relative"])
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit("Invalid backup entry")
        target = home / relative
        old = manifest_path.parent / "original" / relative
        if entry["had_original"] and not exists(old):
            raise SystemExit(f"Missing original backup: {old}")
        displaced = manifest_path.parent / "after-install" / relative
        if exists(target) and exists(displaced):
            raise SystemExit(f"Post-install backup already exists: {displaced}")
        pending.append((entry, target, old, displaced))
    for entry, target, old, displaced in pending:
        print(f"Restore {target}")
        if dry_run:
            continue
        if exists(target):
            displaced.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(displaced))
        if entry["had_original"]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old), str(target))
        entry["restored"] = True
        write_manifest(manifest_path, data)
    if not dry_run:
        (manifest_path.parent / "RESTORED").touch()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--only", choices=["all", "desktop", "nvim", "shell", "themes"], default="all")
    parser.add_argument("--graphics", choices=["auto", "virgl", "native"], default="auto")
    parser.add_argument("--monitor-mode")
    parser.add_argument("--monitor-scale", type=float)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore", type=Path)
    args = parser.parse_args()
    home = args.home.resolve()
    if args.restore:
        restore(args.restore, home, args.dry_run)
        return
    if home == Path.home().resolve():
        for name, default in (("XDG_CONFIG_HOME", home / ".config"), ("XDG_STATE_HOME", home / ".local/state")):
            value = os.environ.get(name)
            if value and Path(value).expanduser().resolve() != default.resolve():
                parser.error(f"Nonstandard {name} is not supported; this snapshot uses {default}")
    if args.monitor_scale is not None and (not math.isfinite(args.monitor_scale) or args.monitor_scale <= 0):
        parser.error("Monitor scale must be positive")
    if args.monitor_mode is not None and not re.fullmatch(r"(?:preferred|highrr|highres|\d+x\d+(?:@\d+(?:\.\d+)?)?)", args.monitor_mode):
        parser.error("Monitor mode must be preferred, highrr, highres, or WIDTHxHEIGHT[@HZ]")
    # Deliberately copy: theme generators can rewrite configs without modifying Git.
    items = []
    for source in sorted((ROOT / "config").iterdir()):
        if args.only == "all" or config_group(source.name) == args.only:
            # Only replace exported theme subdirectories, never entire app profiles.
            if config_group(source.name) == "themes":
                items.extend((child, Path(".config") / source.name / child.name) for child in sorted(source.iterdir()))
            else:
                items.append((source, Path(".config") / source.name))
    if args.only in {"all", "shell"}:
        items.extend((p, Path(p.name)) for p in sorted((ROOT / "home").iterdir()))
    if args.only in {"all", "desktop"}:
        if (ROOT / "wallpapers").is_dir():
            items.extend((p, Path("Pictures/Wallpapers") / p.name) for p in sorted((ROOT / "wallpapers").iterdir()))
        if (ROOT / "assets/caelestia-scheme.json").exists():
            items.append((ROOT / "assets/caelestia-scheme.json", Path(".local/state/caelestia/scheme.json")))
        if (ROOT / "assets/wallpaper.json").exists():
            name = json.loads((ROOT / "assets/wallpaper.json").read_text())["file"]
            if Path(name).name != name:
                raise SystemExit("Wallpaper name must be a filename, not a path")
            if (ROOT / "wallpapers" / name).is_file():
                items.append((str(home / "Pictures/Wallpapers" / name) + "\n", Path(".local/state/caelestia/wallpaper/path.txt")))
    preflight(items, home)
    if args.only in {"all", "desktop"}:
        enabled, monitor = machine_settings(home, args)
    backup = home / ".local/share/dotfiles-backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    manifest = {"home": str(home), "entries": []}
    if not args.dry_run:
        backup.mkdir(parents=True)
        write_manifest(backup / "manifest.json", manifest)
        print(f"Backup manifest: {backup / 'manifest.json'}", flush=True)
    for source, relative in items:
        target = home / relative
        print(f"Install {target}")
        if args.dry_run:
            continue
        had_original = exists(target)
        if had_original:
            saved = backup / "original" / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(saved))
        manifest["entries"].append({"relative": str(relative), "had_original": had_original})
        # Write incrementally so a partial install can still be restored.
        write_manifest(backup / "manifest.json", manifest)
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(source, str):
            target.write_text(source)
        elif source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    if args.only in {"all", "desktop"}:
        print(f"VirGL workaround: {'enabled' if enabled else 'disabled'}")
        if not args.dry_run:
            (home / ".config/caelestia/machine.env").write_text(f"CAELESTIA_VIRGL_WORKAROUND={int(enabled)}\n")
            (home / ".config/hypr/machine.lua").write_text(monitor)


if __name__ == "__main__":
    main()
