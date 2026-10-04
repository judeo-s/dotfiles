"""Ensure refreshing a deployed snapshot does not accumulate code changes."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("normalize", ROOT / "scripts/normalize.py")
normalize = importlib.util.module_from_spec(spec)
spec.loader.exec_module(normalize)


class NormalizeTests(unittest.TestCase):
    def test_comment_monitor_example_is_not_used_as_the_active_monitor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("home", "config", "templates"):
                shutil.copytree(ROOT / name, root / name)
            path = root / "config/hypr/hyprland.lua"
            comment = '-- hl.monitor({\n--     mode = "3840x2160@60",\n--     scale = 2,\n-- })\n'
            path.write_text(comment + 'hl.monitor({ mode = "1920x1080@60", scale = 1 })\n')
            original_root = normalize.ROOT
            normalize.ROOT = root
            try:
                normalize.normalize()
                text = path.read_text()
                self.assertTrue(text.startswith(comment))
                self.assertEqual(text.count('local machine = require("machine")'), 1)
                self.assertIn("mode = machine.mode", text)
                self.assertNotIn('hl.monitor({ mode = "1920x1080@60"', text)
            finally:
                normalize.ROOT = original_root

    def test_normalizing_an_already_portable_snapshot_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("home", "config", "templates"):
                shutil.copytree(ROOT / name, root / name)
            original_root = normalize.ROOT
            normalize.ROOT = root
            try:
                normalize.normalize()
                first = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                normalize.normalize()
                second = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                self.assertEqual(first, second)
            finally:
                normalize.ROOT = original_root
