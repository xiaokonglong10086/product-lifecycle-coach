#!/usr/bin/env python3
import argparse,re
from pathlib import Path
REQUIRED=['DESIGN_PRINCIPLES','SOURCE_CONFLICTS','FEATURE_IMPLEMENTATION_MATRIX','统一模拟业务内核','L3','L4','产品实验室','DECISIONS','OPEN_QUESTIONS','加载','空','失败','重试','刷新恢复','跨端','npm run build','截图']
FORBIDDEN=['无响应按钮','Toast 代替','静态卡片','TODO','Coming Soon']
def main():
 p=argparse.ArgumentParser();p.add_argument('file');p.add_argument('--strict',action='store_true');a=p.parse_args();x=Path(a.file)
 if not x.exists():print('FAIL: file not found');return 1
 t=x.read_text(encoding='utf-8');f=[]
 for i in REQUIRED:
  if i not in t:f.append('缺少：'+i)
 for i in FORBIDDEN:
  if i not in t:f.append('缺少禁止规则：'+i)
 if re.search(r'每轮只做|一个小闭环|只开发一个',t):f.append('错误使用逐链路小步模式')
 if not re.search(r'(所有|全部).*主功能.*L3',re.sub(r'\s+',' ',t)):f.append('没有要求全部主功能达到L3')
 if not re.search(r'(关键)?跨端.*L4',re.sub(r'\s+',' ',t)):f.append('没有要求关键跨端达到L4')
 if not re.search(r'Mock|模拟',t,re.I):f.append('没有明确底层服务可模拟')
 print('PASS' if not f else 'FAIL');[print('- '+i) for i in f];return 1 if a.strict and f else 0
if __name__=='__main__':raise SystemExit(main())
