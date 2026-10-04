"""Exercise the public installer without touching package managers or real HOME."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def env(self, home):
        env = os.environ.copy()
        env["HOME"] = str(home)
        for name in ("XDG_CONFIG_HOME", "XDG_STATE_HOME", "XDG_DATA_HOME"):
            env.pop(name, None)
        return env

    def test_public_config_only_installer_in_a_fresh_home(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), "--config-only", "--skip-plugins", "--only", "nvim"],
                env=self.env(home), text=True, capture_output=True, check=True,
            )
            self.assertTrue((home / ".config/nvim/init.lua").exists())
            self.assertFalse((home / ".config/hypr").exists())
            self.assertNotIn("activate the desktop", result.stdout)

    def test_nonstandard_xdg_directory_is_rejected_before_copying(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            env = self.env(home)
            env["XDG_CONFIG_HOME"] = str(home / "custom-config")
            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), "--config-only", "--skip-plugins"],
                env=env, text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Nonstandard XDG_CONFIG_HOME", result.stderr)
            self.assertEqual(list(home.iterdir()), [])

    @unittest.skipUnless(shutil.which("nvim"), "Neovim not installed")
    def test_plugin_failure_returns_nonzero_to_the_installer(self):
        # Mock the package/network layer; exercise Neovim's actual exit behavior.
        setup = '''
package.loaded["lazy"] = { install = function() end, restore = function() end }
package.loaded["lazy.core.config"] = { plugins = { broken = { url = "example", _ = { installed = true } } } }
package.loaded["lazy.core.plugin"] = { has_errors = function() return true end }
'''
        env = os.environ.copy()
        env["DOTFILES_NVIM_BOOTSTRAP"] = str(ROOT / "scripts/bootstrap-nvim.lua")
        result = subprocess.run(
            ["nvim", "--headless", "-u", "NONE", "+lua " + setup,
             "+lua dofile(vim.env.DOTFILES_NVIM_BOOTSTRAP)"],
            env=env, text=True, capture_output=True, timeout=15,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Plugin installation failed: broken", result.stderr)
