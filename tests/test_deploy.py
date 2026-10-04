"""Exercise backup/restore and machine settings in disposable home directories."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DeployTests(unittest.TestCase):
    def deploy(self, home, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/deploy.py"), "--home", str(home), *args],
            text=True, capture_output=True, check=True,
        )

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.deploy(home, "--dry-run", "--graphics", "native")
            self.assertEqual(list(home.iterdir()), [])

    def test_backup_and_restore_existing_and_new_configs(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            original = home / ".config/foot"
            original.mkdir(parents=True)
            (original / "mine.ini").write_text("original settings\n")
            self.deploy(home, "--only", "shell")
            self.assertTrue((original / "foot.ini").exists())
            self.assertFalse((original / "mine.ini").exists())
            manifest = next((home / ".local/share/dotfiles-backups").glob("*/manifest.json"))
            (original / "new-edit.ini").write_text("keep this edit\n")
            self.deploy(home, "--restore", str(manifest))
            self.assertEqual((original / "mine.ini").read_text(), "original settings\n")
            self.assertFalse((home / ".config/kitty").exists())
            self.assertTrue((manifest.parent / "after-install/.config/foot/new-edit.ini").exists())

    def test_repeat_install_preserves_previous_machine_config(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.deploy(home, "--only", "desktop", "--graphics", "virgl", "--monitor-mode", "1920x1080@60")
            settings = home / ".config/caelestia/machine.env"
            self.assertIn("=1", settings.read_text())
            self.assertIn("1920x1080@60", (home / ".config/hypr/machine.lua").read_text())
            self.deploy(home, "--only", "desktop", "--graphics", "native")
            self.assertIn("=0", settings.read_text())
            manifests = sorted((home / ".local/share/dotfiles-backups").glob("*/manifest.json"))
            self.deploy(home, "--restore", str(manifests[-1]))
            self.assertIn("=1", settings.read_text())
            self.assertFalse((home / ".config/nvim").exists())

    def test_themes_leave_application_profiles_intact(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            profile = home / ".config/vesktop/settings.json"
            profile.parent.mkdir(parents=True)
            profile.write_text('{"my_setting": true}\n')
            self.deploy(home, "--only", "themes")
            self.assertEqual(json.loads(profile.read_text()), {"my_setting": True})
            self.assertTrue((profile.parent / "themes/caelestia.theme.css").exists())

    def test_full_install_restores_wallpaper_and_lockfile(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.deploy(home, "--graphics", "native")
            lock = json.loads((home / ".config/nvim/lazy-lock.json").read_text())
            self.assertIn("alpha-nvim", lock)
            selected = json.loads((ROOT / "assets/wallpaper.json").read_text())["file"]
            path = home / ".local/state/caelestia/wallpaper/path.txt"
            self.assertEqual(path.read_text().strip(), str(home / "Pictures/Wallpapers" / selected))
            self.assertTrue(Path(path.read_text().strip()).is_file())
            self.assertIn('require("machine")', (home / ".config/hypr/hyprland.lua").read_text())

    def test_invalid_scale_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with self.assertRaises(subprocess.CalledProcessError):
                self.deploy(home, "--monitor-scale", "nan")
            self.assertEqual(list(home.iterdir()), [])

    def test_missing_backup_is_detected_before_any_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            original = home / ".config/foot"
            original.mkdir(parents=True)
            (original / "mine.ini").write_text("original\n")
            self.deploy(home, "--only", "shell")
            manifest = next((home / ".local/share/dotfiles-backups").glob("*/manifest.json"))
            (manifest.parent / "original/.config/foot/mine.ini").unlink()
            (manifest.parent / "original/.config/foot").rmdir()
            installed = (original / "foot.ini").read_text()
            with self.assertRaises(subprocess.CalledProcessError):
                self.deploy(home, "--restore", str(manifest))
            self.assertEqual((original / "foot.ini").read_text(), installed)
            self.assertTrue((home / ".zshrc").exists())
            self.assertFalse((manifest.parent / "after-install").exists())

    def test_default_reinstall_preserves_local_machine_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.deploy(home, "--only", "desktop", "--graphics", "virgl")
            display = home / ".config/hypr/machine.lua"
            custom = 'return { mode = "2560x1440@144", scale = 1.5, output = "DP-1" }\n'
            display.write_text(custom)
            self.deploy(home, "--only", "desktop")
            self.assertEqual(display.read_text(), custom)
            self.assertIn("=1", (home / ".config/caelestia/machine.env").read_text())

    def test_invalid_parent_fails_before_replacing_other_configs(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / ".config").mkdir()
            (home / ".config/vesktop").write_text("not a directory\n")
            with self.assertRaises(subprocess.CalledProcessError):
                self.deploy(home, "--only", "themes")
            self.assertFalse((home / ".config/BetterDiscord").exists())
            self.assertFalse((home / ".local/share/dotfiles-backups").exists())


if __name__ == "__main__":
    unittest.main()
