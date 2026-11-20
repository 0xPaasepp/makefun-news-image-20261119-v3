"""news-image-20261119 v3 entrypoint.

Copies the pre-rendered entry.png (shipped in this repository, drawn at
build time by render.py with real Liberation glyphs) to the output path.
Standard library only; deterministic; no network. The output directory is
/output unless MAKEFUN_OUTPUT_DIR names another one.
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
