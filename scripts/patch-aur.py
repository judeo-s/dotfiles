#!/usr/bin/env python3
"""Apply the two native ARM build adaptations tested on this VM."""
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
if path.parent.name not in {"libcava", "python-materialyoucolor"}:
    raise SystemExit("Only the documented Caelestia dependency recipes can be patched")
text = path.read_text()
match = re.search(r"^arch=\(([^\n]*)\)", text, flags=re.M)
if not match:
    raise SystemExit("AUR recipe changed: arch declaration not found; review PKGBUILD")
if "aarch64" not in match[1] and "'any'" not in match[1] and '"any"' not in match[1]:
    text = text[:match.start()] + f"arch=({match[1]} 'aarch64')" + text[match.end():]
if path.parent.name == "python-materialyoucolor":
    command = "python -m build --wheel --no-isolation"
    if command not in text:
        raise SystemExit("Python build recipe changed; review PKGBUILD before adapting")
    if "CC=/usr/bin/gcc CXX=/usr/bin/g++" not in text:
        text = text.replace(command, f"CC=/usr/bin/gcc CXX=/usr/bin/g++ {command}")
path.write_text(text)
print(f"Adapted native ARM recipe: {path}")
