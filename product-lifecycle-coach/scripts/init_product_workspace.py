#!/usr/bin/env python3
"""Initialize a lightweight product workspace for a solo product manager."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TEMPLATE_MAP = {
    "PRODUCT_STATE.md": "CURRENT_PRODUCT.md",
    "DECISIONS.md": "DECISIONS.md",
    "NEXT_TASK_CARD.md": "NEXT.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a lightweight product workspace with only current state, decisions, and next work."
    )
    parser.add_argument("--path", default=".", help="Project root in which to create product/.")
    parser.add_argument("--product-name", required=True, help="Product name inserted into CURRENT_PRODUCT.md.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    parser.add_argument(
        "--complex",
        action="store_true",
        help="Also create project inventory, current-version alignment, and product-map files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "assets" / "templates"
    project_root = Path(args.path).expanduser().resolve()
    product_root = project_root / "product"
    product_root.mkdir(parents=True, exist_ok=True)
    if args.complex:
        for directory in ("specs", "changes", "releases", "research", "evaluations"):
            (product_root / directory).mkdir(exist_ok=True)

    template_map = dict(TEMPLATE_MAP)
    if args.complex:
        template_map.update(
            {
                "SOURCE_INVENTORY.md": "SOURCE_INVENTORY.md",
                "CURRENT_VERSION_ALIGNMENT.md": "CURRENT_VERSION_ALIGNMENT.md",
                "PROGRAM_MAP.md": "PROGRAM_MAP.md",
            }
        )

    created: list[str] = []
    skipped: list[str] = []

    for source_name, target_name in template_map.items():
        source = templates / source_name
        target = product_root / target_name
        if target.exists() and not args.force:
            skipped.append(str(target))
            continue
        if not source.exists():
            raise FileNotFoundError(f"Missing template: {source}")
        content = source.read_text(encoding="utf-8")
        if source_name == "PRODUCT_STATE.md":
            content = content.replace("[name]", args.product_name, 1)
        target.write_text(content, encoding="utf-8")
        created.append(str(target))

    result = {
        "status": "已完成",
        "product_root": str(product_root),
        "created": created,
        "skipped": skipped,
        "mode": "复杂项目" if args.complex else "独立产品经理轻量模式",
        "document_policy": "只有当前工作真正需要时，才创建 PRD、AI、工程、任务或 QA 文档。",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
