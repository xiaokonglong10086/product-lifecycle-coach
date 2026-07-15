#!/usr/bin/env python3
import shutil, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root/'scripts/validate_skill.py'), str(root)], check=True)
out=root.parent/'dist'
out.mkdir(exist_ok=True)
base=out/'skill'
zip_path=shutil.make_archive(str(base),'zip',root.parent,root.name)
print(zip_path)
