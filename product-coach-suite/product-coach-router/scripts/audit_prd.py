#!/usr/bin/env python3
"""Audit a product-function PRD in Markdown, text, or DOCX format."""
from __future__ import annotations
import argparse,json,re,zipfile
from dataclasses import asdict,dataclass
from pathlib import Path
from xml.etree import ElementTree as ET
HEADING_RE=re.compile(r'^(#{1,6})\s+(.+?)\s*$',re.M)
MERMAID_RE=re.compile(r'```mermaid\s*(.*?)```',re.I|re.S)
IMAGE_RE=re.compile(r'!\[[^\]]*\]\([^\)]+\)')
NUMBERED_STEP_RE=re.compile(r'^\s*(?:\d+[\.、]|Step\s*\d+[:：])',re.M|re.I)
REQUIRED={'PRODUCT_OVERVIEW':['产品概述'],'USERS_SCENARIOS':['目标用户','使用场景'],'STRUCTURE':['产品结构','页面关系'],'COMPLETE_FLOW':['完整产品总流程','完整产品流程'],'CORE_USER_FLOW':['核心用户流程','用户流程'],'INTERNAL_LOGIC':['产品内部运作逻辑','内部运作逻辑'],'COMMON_RULES':['通用组件','交互规则'],'CROSS_RULES':['跨功能','异常处理'],'QUALITY':['质量监控','成功标准'],'NFR':['非功能需求'],'OPEN_QUESTIONS':['待确认']}
FORBIDDEN={'PRODUCT_COACH':r'产品教练(?:版|结论|建议|取舍|判断)?','DOC_VERSION':r'\b(?:PRD\s*)?V\s*\d+(?:\.\d+)+\b|文档版本|产品目标版本|原始版本','PHASE_CODE':r'\bP0(?:A|B)?\b|\bP1\b|\bP2\b','BASELINE':r'基线','PROCESS_LANGUAGE':r'上一版|前一版|原版本|相比旧版|功能完整性对照|本版|版本变更|修订摘要|开发批次|开发阶段|路线图|生命周期治理','CHAPTER_ZERO':r'(?m)^\s*(?:第\s*)?0(?:\.\d+)?[\.、\s]','FRD_TITLE':r'\bFRD\b','GOVERNANCE':r'工程落地版|内部产品基线|内部产品治理'}
DETAIL=['页面布局','页面位置','触发条件','操作流程','操作步骤','展示内容','字段','产品规则','交互反馈','状态','异常','恢复','数据去向','验收标准']
@dataclass
class Finding: severity:str;code:str;message:str;evidence:str=''
@dataclass
class Loaded: text:str;drawings:int=0;alt_texts:list[str]|None=None
def load(path:Path)->Loaded:
 if path.suffix.lower()!='.docx':return Loaded(path.read_text(encoding='utf-8'),0,[])
 with zipfile.ZipFile(path) as zf:xml=zf.read('word/document.xml')
 root=ET.fromstring(xml);ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'};paras=[]
 for p in root.findall('.//w:p',ns):
  text=''.join((t.text or '') for t in p.findall('.//w:t',ns)).strip()
  if not text:continue
  style=p.find('./w:pPr/w:pStyle',ns);val=style.attrib.get('{%s}val'%ns['w'],'') if style is not None else ''
  m=re.search(r'(?:Heading|标题)\s*([1-6])',val,re.I) or re.fullmatch(r'([1-6])',val)
  if m:text='#'*int(m.group(1))+' '+text
  paras.append(text)
 alts=[]
 for n in root.findall('.//wp:docPr',ns):
  for k in ('title','descr','name'):
   if n.attrib.get(k):alts.append(n.attrib[k])
 return Loaded('\n'.join(paras),len(root.findall('.//w:drawing',ns)),alts)
def section(text,terms):
 ms=list(HEADING_RE.finditer(text))
 for i,m in enumerate(ms):
  if any(t in m.group(2) for t in terms):
   level=len(m.group(1));end=len(text)
   for later in ms[i+1:]:
    if len(later.group(1))<=level:end=later.start();break
   return text[m.end():end]
 pos=[text.find(t) for t in terms if t in text]
 return text[min(pos):min(pos)+4500] if pos else ''
def audit(doc:Loaded,suffix:str):
 t=doc.text;f=[]
 for code,alts in REQUIRED.items():
  if not any(x in t for x in alts):f.append(Finding('HIGH','MISSING_'+code,'缺少必要内容：'+'/'.join(alts)))
 for code,pat in FORBIDDEN.items():
  hits=re.findall(pat,t,re.I)
  if hits:f.append(Finding('HIGH',code,'正式文档包含禁止的版本、教练或过程语言','、'.join(map(str,hits[:8]))))
 complete=section(t,['完整产品总流程','完整产品流程']);internal=section(t,['产品内部运作逻辑','内部运作逻辑']);blocks=MERMAID_RE.findall(t)
 if suffix in {'.md','.txt'}:
  if not MERMAID_RE.findall(complete):f.append(Finding('HIGH','NO_COMPLETE_FLOW_DIAGRAM','完整产品流程章节没有真正的 Mermaid 流程图'))
  if len(blocks)<3:f.append(Finding('HIGH','INSUFFICIENT_FLOW_TYPES','至少需要三类流程图',str(len(blocks))))
  if not MERMAID_RE.findall(internal):f.append(Finding('HIGH','NO_INTERNAL_LOGIC_DIAGRAM','内部运作章节缺少独立流程图'))
 else:
  alt=' '.join(doc.alt_texts or [])
  if doc.drawings<3:f.append(Finding('HIGH','INSUFFICIENT_EMBEDDED_DIAGRAMS','DOCX 至少应嵌入三类流程图',str(doc.drawings)))
  if not re.search(r'完整产品.*流程|产品总流程',alt+t):f.append(Finding('HIGH','NO_IDENTIFIABLE_COMPLETE_FLOW','未检测到完整产品总流程图标题或替代文本'))
  if not re.search(r'核心用户.*流程|用户旅程',alt+t):f.append(Finding('HIGH','NO_IDENTIFIABLE_CORE_USER_FLOW','未检测到核心用户流程图'))
  if not re.search(r'内部运作|内部处理|产品内部',alt+t):f.append(Finding('HIGH','NO_IDENTIFIABLE_INTERNAL_FLOW','未检测到内部运作图'))
  for term in ['入口','失败','重试','确认','结果']:
   if term not in complete:f.append(Finding('HIGH','COMPLETE_FLOW_THIN','完整流程缺少 '+term));break
  for term in ['任务登记','待确认','人工','写入','质量']:
   if term not in internal:f.append(Finding('HIGH','INTERNAL_FLOW_THIN','内部运作缺少 '+term));break
 visuals=len(blocks)+len(IMAGE_RE.findall(t))+doc.drawings
 if visuals==0:f.append(Finding('HIGH','NO_VISUAL_FLOW','没有检测到流程图'))
 hits=[x for x in DETAIL if x in t]
 if len(hits)<10:f.append(Finding('HIGH','FUNCTION_DETAIL_TOO_THIN','功能正文细节不足','、'.join(hits)))
 if len(NUMBERED_STEP_RE.findall(t))<8:f.append(Finding('MEDIUM','TOO_FEW_OPERATION_STEPS','连续操作步骤过少'))
 if not any(x in t for x in ['页面布局','ASCII','线框','┌']):f.append(Finding('MEDIUM','NO_PAGE_LAYOUT','缺少页面布局或线框定义'))
 high=[x for x in f if x.severity=='HIGH'];med=[x for x in f if x.severity=='MEDIUM'];verdict='FAIL' if high else ('PASS WITH CONCERNS' if med else 'PASS')
 return verdict,f,{'characters':len(t),'drawings':doc.drawings,'mermaid_blocks':len(blocks),'detail_markers':hits,'numbered_steps':len(NUMBERED_STEP_RE.findall(t))}
def main():
 p=argparse.ArgumentParser();p.add_argument('prd');p.add_argument('--strict',action='store_true');p.add_argument('--json',action='store_true');a=p.parse_args();path=Path(a.prd);v,f,s=audit(load(path),path.suffix.lower());payload={'verdict':v,'stats':s,'findings':[asdict(x) for x in f]}
 print(json.dumps(payload,ensure_ascii=False,indent=2) if a.json else '\n'.join([v]+[f'[{x.severity}] {x.code}: {x.message} {x.evidence}' for x in f]));return 0 if (not a.strict or v=='PASS') else 1
if __name__=='__main__':raise SystemExit(main())
