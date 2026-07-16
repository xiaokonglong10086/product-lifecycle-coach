# DOCX 最终质量门

最终交付前必须直接审查最终 DOCX：

```bash
python scripts/audit_prd.py output.docx --strict
```

改写既有文档时：

```bash
python scripts/audit_prd_coverage.py source.docx output.docx --strict
```

审查失败不得交付。不得只审查 Markdown 或生成前提纲。

视觉审查必须渲染 DOCX 为逐页图片并检查每一页：流程图可读、表格不截断、标题不孤立、页眉页脚无版本或教练语言、中文标点和标题断行正常、无异常空白页。修复后重新渲染全部页面。

只有脚本 PASS、三类流程图真实嵌入可读、视觉检查通过时才能交付。