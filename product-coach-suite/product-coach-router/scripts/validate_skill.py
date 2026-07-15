#!/usr/bin/env python3
import re, sys, yaml
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
skill = root / 'SKILL.md'
errors=[]
if not skill.exists(): errors.append('SKILL.md missing')
else:
    text=skill.read_text(encoding='utf-8')
    m=re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m: errors.append('invalid frontmatter')
    else:
        data=yaml.safe_load(m.group(1)) or {}
        if set(data) != {'name','description'}: errors.append('frontmatter must contain only name and description')
        if data.get('name')!='product-coach-router': errors.append('unexpected skill name')
for p in ['agents/openai.yaml','references/shared/authority-contract.md','references/shared/responsibility-contract.md','references/shared/handoff-contract.md','references/shared/output-style-contract.md','references/subskills/discovery-direction.md','references/subskills/design-principles.md','references/subskills/product-function-prd.md','references/subskills/validation-development.md','references/subskills/implementation-qa.md','references/subskills/iteration-pilot.md','references/modules/engineering-spec.md','references/modules/ai-feature-spec.md','references/modules/mock-validation-data.md','references/modules/document-delivery.md']:
    if not (root/p).exists(): errors.append(f'missing {p}')
text=(root/'SKILL.md').read_text(encoding='utf-8') if skill.exists() else ''
for forbidden in ['PRODUCT_DECISIONS.md','OPEN_PRODUCT_DECISIONS.md']:
    if forbidden in text: errors.append(f'forbidden duplicate decision file: {forbidden}')
if errors:
    print('\n'.join('FAIL: '+e for e in errors)); sys.exit(1)
print('PASS: skill structure and contracts validated')
