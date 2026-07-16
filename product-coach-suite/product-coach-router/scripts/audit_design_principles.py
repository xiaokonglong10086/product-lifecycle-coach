#!/usr/bin/env python3
import argparse,re
from pathlib import Path
REQUIRED=['适用范围与权威顺序','核心设计理念','审计问题','一票否决','当前可变方案','已明确放弃的方向','待确认候选']
def main():
 p=argparse.ArgumentParser();p.add_argument('file');p.add_argument('--strict',action='store_true');a=p.parse_args();x=Path(a.file)
 if not x.exists(): print('FAIL: file not found'); return 1
 t=x.read_text(encoding='utf-8');f=[f'缺少：{i}' for i in REQUIRED if i not in t]
 c=len(re.findall(r'^###\s+\d+\.',t,re.M))
 if c<3:f.append('核心原则少于3条')
 if c>15:f.append('核心原则超过15条，可能混入具体方案')
 if re.search(r'React|Zustand|Redux|API 路径|数据库表|按钮位于|左侧第|右侧第',t,re.I):f.append('混入技术或页面实现细节')
 print('PASS' if not f else 'FAIL');[print('- '+i) for i in f];return 1 if a.strict and f else 0
if __name__=='__main__':raise SystemExit(main())
