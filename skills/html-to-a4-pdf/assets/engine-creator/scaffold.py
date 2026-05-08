#!/usr/bin/env python3
"""
engine-creator · 새 문서 엔진 스캐폴더

사용법:
    python scaffold.py 계약서
    python scaffold.py 사업계획서

동작:
    현재 작업 폴더에 <도메인명>/ 폴더를 새로 만들고,
    templates/ 내용을 복사하면서 {DOMAIN} placeholder를 치환한다.
"""

import os
import sys
import shutil
import argparse


def validate_domain(domain: str) -> str:
    """Return a safe folder name for the generated engine."""
    if not domain or domain in {".", ".."}:
        raise ValueError("domain must be a non-empty folder name")
    if os.path.isabs(domain) or "/" in domain or "\\" in domain or ".." in domain:
        raise ValueError("domain must be a simple folder name, not a path")
    return domain


def scaffold(domain: str, force: bool = False):
    try:
        domain = validate_domain(domain)
    except ValueError as exc:
        print(f"[에러] 잘못된 도메인명: {exc}", file=sys.stderr)
        sys.exit(1)

    here = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(here, "templates")
    shared_assets_dir = os.path.abspath(os.path.join(here, ".."))
    target_root = os.path.abspath(domain)

    if os.path.exists(target_root):
        if not force:
            print(f"[에러] 이미 존재: {target_root}")
            print("       덮어쓰려면 --force")
            sys.exit(1)
        shutil.rmtree(target_root)

    # 템플릿 순회하면서 복사 + placeholder 치환
    for root, dirs, files in os.walk(templates_dir):
        # __pycache__ 등 제외
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        rel = os.path.relpath(root, templates_dir)
        dst_dir = os.path.join(target_root, rel) if rel != "." else target_root
        os.makedirs(dst_dir, exist_ok=True)

        for name in files:
            src = os.path.join(root, name)
            dst = os.path.join(dst_dir, name)

            # 텍스트 파일은 치환, 바이너리는 그대로 복사
            try:
                with open(src, "r", encoding="utf-8") as f:
                    content = f.read()
                content = content.replace("{DOMAIN}", domain)
                with open(dst, "w", encoding="utf-8") as f:
                    f.write(content)
            except UnicodeDecodeError:
                shutil.copy2(src, dst)

    # 생성된 엔진이 레포 밖에서도 독립적으로 PDF 변환까지 수행할 수 있게
    # 공통 A4 셸과 변환기를 함께 복사한다.
    for shared_name in ("a4-base.css", "convert.py"):
        shared_src = os.path.join(shared_assets_dir, shared_name)
        if os.path.exists(shared_src):
            shutil.copy2(shared_src, os.path.join(target_root, shared_name))

    print(f"[완료] 엔진 생성: {target_root}")
    print(f"       → python {target_root}/render.py {target_root}/data.json --pdf --open")


def main():
    parser = argparse.ArgumentParser(description="새 문서 엔진 스캐폴더")
    parser.add_argument("domain", help="생성할 엔진 폴더명 (예: 계약서, 사업계획서, report)")
    parser.add_argument("--force", action="store_true", help="기존 폴더가 있으면 덮어쓰기")
    args = parser.parse_args()

    scaffold(args.domain, force=args.force)


if __name__ == "__main__":
    main()
