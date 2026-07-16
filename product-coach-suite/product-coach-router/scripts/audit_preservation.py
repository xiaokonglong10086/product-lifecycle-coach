#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
required={
'PRD':['references/preserved/prd-core.md','references/preserved/prd-authority-and-freeze.md','references/preserved/prd-contract.md','references/preserved/prd-flow-and-function-standard.md','references/preserved/docx-quality-gate.md','references/preserved/prd-gold-pattern.md','assets/templates/PRODUCT_FUNCTION_PRD.md','scripts/audit_prd.py','scripts/audit_prd_coverage.py'],
'功能验证':['references/preserved/validation-core.md','references/preserved/design-validation-standard.md','references/preserved/mock-data-standard.md','assets/templates/CODEX_MASTER_TASK.md','scripts/audit_design_validation_task.py'],
'理念/QA/迭代':['assets/templates/DESIGN_PRINCIPLES.md','scripts/audit_design_principles.py','references/preserved/implementation-qa-core.md','assets/templates/QA_REPORT.md','references/preserved/iteration-core.md','assets/templates/ITERATION_CHANGE_MAP.md']}
errors=[]
for group,paths in required.items():
 for p in paths:
  f=root/p
  if not f.exists() or f.stat().st_size<50:errors.append(f'{group} 缺失或过薄: {p}')
texts='\n'.join((root/p).read_text(encoding='utf-8',errors='ignore') for paths in required.values() for p in paths if (root/p).exists())
for term in ['完整产品总流程','核心用户流程','产品内部运作','L3','L4','产品实验室','统一模拟业务内核','刷新恢复','审查失败不得交付']:
 if term not in texts:errors.append('核心能力缺失: '+term)
if errors:
 print('FAIL');[print('- '+e) for e in errors];sys.exit(1)
print('PASS: preserved PRD and validation assets present')
