#!/usr/bin/env python3
"""Apply the portable adaptations to a freshly refreshed snapshot."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def normalize():
    for path in (ROOT / "home").glob(".*"):
        if path.is_file():
            text = path.read_text().replace("/home/oni/.opencode/bin", "$HOME/.opencode/bin")
            text = text.replace("if uwsm check may-start; then", "if command -v uwsm >/dev/null 2>&1 && uwsm check may-start; then")
            if path.name == ".bashrc":
                text = re.sub(r'^export PATH=\$HOME/\.opencode/bin:\$PATH$', 'export PATH="$HOME/.local/bin:$HOME/.opencode/bin:$PATH"', text, flags=re.M)
            path.write_text(text)
    path = ROOT / "home/.zshrc"
    text = path.read_text()
    text = re.sub(r'^export PATH=\$HOME/\.opencode/bin:\$PATH$', 'export PATH="$HOME/.local/bin:$HOME/.opencode/bin:$PATH"', text, flags=re.M)
    text = re.sub(r'^eval "\$\(starship init zsh\)"$', 'command -v starship >/dev/null 2>&1 && eval "$(starship init zsh)"', text, flags=re.M)
    for plugin in ("zsh-autosuggestions", "zsh-syntax-highlighting"):
        source = f"/usr/share/zsh/plugins/{plugin}/{plugin}.zsh"
        text = re.sub(r"^source " + re.escape(source) + r"$", f"[[ -r {source} ]] && source {source}", text, flags=re.M)
    path.write_text(text)
    path = ROOT / "config/hypr/hyprland.lua"
    text = path.read_text()
    if not re.search(r'^\s*local machine = require\("machine"\)', text, flags=re.M):
        text = re.sub(r'^[ \t]*hl\.monitor\(\{.*?\}\)', '''local machine = require("machine")
hl.monitor({
    output = machine.output or "",
    mode = machine.mode or "preferred",
    position = "auto",
    scale = machine.scale or 1,
})''', text, count=1, flags=re.S | re.M)
    path.write_text(text)
    (ROOT / "config/caelestia/start.sh").write_text((ROOT / "templates/caelestia-start.sh").read_text())
    # The old one-off installer is superseded by the repository installer.
    (ROOT / "config/caelestia/install.sh").unlink(missing_ok=True)
    path = ROOT / "config/nvim/lua/config/lazy.lua"
    if path.exists():
        text = re.sub(
            r"^\t\tvim\.fn\.getchar\(\)\n",
            "\t\tif #vim.api.nvim_list_uis() > 0 then\n\t\t\tvim.fn.getchar()\n\t\tend\n",
            path.read_text(),
            flags=re.M,
        )
        path.write_text(text)
    # The formatter looks for .prettierrc.json, but the original snapshot
    # called the file prettierrc.json. Keep the original and supply its alias.
    prettier = ROOT / "config/nvim/prettierrc.json"
    destination = prettier.with_name(".prettierrc.json")
    if prettier.exists() and not destination.exists():
        destination.write_text(prettier.read_text())


if __name__ == "__main__":
    normalize()
