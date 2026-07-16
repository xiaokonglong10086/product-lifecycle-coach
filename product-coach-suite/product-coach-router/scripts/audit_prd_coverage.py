#!/usr/bin/env python3
"""Conservative omission detector for rewritten PRDs."""
from __future__ import annotations
import argparse,json,re
from dataclasses import asdict,dataclass
from pathlib import Path
from audit_prd import load
META=re.compile(r'产品教练|上一版|前一版|本版|版本|修订|变更|目录|文档用途|更新日期|适用对象|^#+|^\s*[-|:]?\s*$|^\s*\|?\s*---',re.I)
CRITICAL=['必须','不得','只','默认','最多','至少','支持','显示','隐藏','写入','覆盖','追加','只读','左侧','右侧','上方','下方','固定','折叠','按钮','字段','状态','失败','重试','恢复','人工确认','AI','来源','优先级','数据去向','阈值','通知','异常','验收']
@dataclass
class Rule:text:str;critical:bool;best_score:float=0.0;best_match:str=''
def norm(t):return re.sub(r'[，。；：、！？,.!?;:\'"“”‘’（）()\[\]{}<>/\\\-\s`*_#>|]','',t).lower()
def grams(t):return {t[i:i+2] for i in range(max(0,len(t)-1))} if len(t)>=2 else ({t} if t else set())
def sim(a,b):
 a,b=norm(a),norm(b)
 if not a or not b:return 0.0
 if a in b or b in a:return max(.82,min(len(a),len(b))/max(len(a),len(b)))
 ga,gb=grams(a),grams(b);return len(ga&gb)/len(ga|gb) if ga and gb else 0.0
def candidates(text):
 out=[]
 for raw in text.splitlines():
  line=raw.strip()
  if not line or META.search(line) or line.startswith('```'):continue
  if line.startswith('|') and line.endswith('|'):
   cells=[c.strip() for c in line.strip('|').split('|') if len(norm(c))>=6 and not re.fullmatch(r'[-:]+',c)]
   if len(cells)<2:continue
   line='；'.join(cells)
  line=re.sub(r'^[-*+]\s+','',line);line=re.sub(r'^\d+[\.、]\s*','',line)
  if 10<=len(norm(line))<=260:out.append(line)
 seen=set();res=[]
 for x in out:
  k=norm(x)
  if k not in seen:seen.add(k);res.append(x)
 return res
def audit(src,out,max_missing):
 rules=[Rule(x,bool(re.search(r'\d',x)) or any(k in x for k in CRITICAL)) for x in candidates(src)];lines=candidates(out);chunks=lines[:]
 for size in (2,3):
  for i in range(len(lines)-size+1):chunks.append('；'.join(lines[i:i+size]))
 on=norm(out)
 for r in rules:
  nr=norm(r.text)
  if nr and nr in on:r.best_score=1;r.best_match=r.text;continue
  for c in chunks:
   s=sim(r.text,c)
   if s>r.best_score:r.best_score=s;r.best_match=c
   if s>=.92:break
 th=.56;missing=[r for r in rules if r.best_score<th];critical=[r for r in rules if r.critical];cm=[r for r in critical if r.best_score<th];overall=(len(rules)-len(missing))/len(rules) if rules else 1;cc=(len(critical)-len(cm))/len(critical) if critical else 1;reasons=[]
 if overall<.72:reasons.append(f'总体规则覆盖率过低：{overall:.1%}')
 if cc<.80:reasons.append(f'关键细节覆盖率过低：{cc:.1%}')
 if len(cm)>max_missing:reasons.append(f'疑似遗漏关键规则过多：{len(cm)}')
 return {'verdict':'FAIL' if reasons else 'PASS','source_rules':len(rules),'critical_rules':len(critical),'overall_coverage':round(overall,4),'critical_coverage':round(cc,4),'reasons':reasons,'missing_critical':[asdict(r) for r in sorted(cm,key=lambda x:x.best_score)[:max_missing]]}
def main():
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('--strict',action='store_true');p.add_argument('--json',action='store_true');p.add_argument('--max-missing',type=int,default=30);a=p.parse_args();r=audit(load(Path(a.source)).text,load(Path(a.output)).text,a.max_missing)
 print(json.dumps(r,ensure_ascii=False,indent=2) if a.json else '\n'.join([r['verdict'],f"总体规则覆盖率：{r['overall_coverage']:.1%}",f"关键细节覆盖率：{r['critical_coverage']:.1%}"]+['[HIGH] '+x for x in r['reasons']]));return 0 if (not a.strict or r['verdict']=='PASS') else 1
if __name__=='__main__':raise SystemExit(main())
