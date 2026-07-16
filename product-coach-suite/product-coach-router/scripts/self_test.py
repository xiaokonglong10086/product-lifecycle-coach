#!/usr/bin/env python3
import subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]

def run(args):
 r=subprocess.run([sys.executable,*map(str,args)],text=True,capture_output=True);print(r.stdout);print(r.stderr);return r.returncode

with tempfile.TemporaryDirectory() as td:
 td=Path(td)
 principles=td/'DESIGN_PRINCIPLES.md';principles.write_text('# 产品设计理念\n## 适用范围与权威顺序\n## 核心设计理念\n### 1. 清晰\n审计问题：是否清晰\n一票否决：混乱\n### 2. 真实\n审计问题：是否真实\n一票否决：造假\n### 3. 可用\n审计问题：是否可用\n一票否决：不可用\n## 当前可变方案\n## 已明确放弃的方向\n## 待确认候选',encoding='utf-8')
 task=td/'CODEX_MASTER_TASK.md';task.write_text((root/'assets/templates/CODEX_MASTER_TASK.md').read_text(encoding='utf-8'),encoding='utf-8')
 codes=[run([root/'scripts/audit_design_principles.py',principles,'--strict']),run([root/'scripts/audit_design_validation_task.py',task,'--strict']),run([root/'scripts/audit_preservation.py',root])]
 sys.exit(0 if all(c==0 for c in codes) else 1)
