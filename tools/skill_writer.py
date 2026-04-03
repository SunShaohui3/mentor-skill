#!/usr/bin/env python3
"""Skill 文件管理器。

管理导师 Skill 的文件操作：列出、初始化目录、组合生成 SKILL.md。
"""

import argparse
import json
import os
import sys


def list_skills(base_dir: str):
    """列出所有已生成的导师 Skill。"""
    if not os.path.isdir(base_dir):
        print("还没有创建任何导师 Skill。")
        return

    skills = []
    for slug in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, slug, "meta.json")
        if not os.path.exists(meta_path):
            continue
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        skills.append(
            {
                "slug": slug,
                "name": meta.get("name", slug),
                "version": meta.get("version", "?"),
                "updated_at": meta.get("updated_at", "?"),
                "profile": meta.get("profile", {}),
            }
        )

    if not skills:
        print("还没有创建任何导师 Skill。")
        return

    print(f"共 {len(skills)} 个导师 Skill：\n")
    for skill in skills:
        profile = skill["profile"]
        desc_parts = [profile.get("field", ""), profile.get("role", "")]
        desc = " / ".join([part for part in desc_parts if part])
        print(f"  /{skill['slug']} - {skill['name']}")
        if desc:
            print(f"    {desc}")
        updated = skill["updated_at"][:10] if len(skill["updated_at"]) > 10 else skill["updated_at"]
        print(f"    版本 {skill['version']} / 更新于 {updated}")
        print()


def init_skill(base_dir: str, slug: str):
    """初始化导师 Skill 目录结构。"""
    skill_dir = os.path.join(base_dir, slug)
    dirs = [
        os.path.join(skill_dir, "versions"),
        os.path.join(skill_dir, "memories", "chats"),
        os.path.join(skill_dir, "memories", "notes"),
        os.path.join(skill_dir, "memories", "public"),
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    print(f"已初始化目录：{skill_dir}")


def combine_skill(base_dir: str, slug: str):
    """合并 memory.md 和 persona.md 生成完整 SKILL.md。"""
    skill_dir = os.path.join(base_dir, slug)
    meta_path = os.path.join(skill_dir, "meta.json")
    memory_path = os.path.join(skill_dir, "memory.md")
    persona_path = os.path.join(skill_dir, "persona.md")
    skill_path = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在：{meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    memory_content = ""
    if os.path.exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            memory_content = f.read().strip()

    persona_content = ""
    if os.path.exists(persona_path):
        with open(persona_path, "r", encoding="utf-8") as f:
            persona_content = f.read().strip()

    name = meta.get("name", slug)
    profile = meta.get("profile", {})
    desc_parts = [profile.get("field", ""), profile.get("role", ""), profile.get("style_summary", "")]
    desc_parts = [part for part in desc_parts if part]
    description = "，".join(desc_parts) if desc_parts else name

    skill_md = f"""---
name: mentor-{slug}
description: {name}，{description}
user-invocable: true
---

# {name}

{description}

---

## PART A：Mentorship Memory
{memory_content}

---

## PART B：Persona
{persona_content}

---

## 运行规则

1. 你是{name}的导师化身，不是通用 AI 助手。
2. 先根据 PART B 决定如何分析、提问和反馈。
3. 再结合 PART A 的真实互动场景与指导记忆补足上下文。
4. 保持 ta 原本的表达风格、边界感和反馈力度。
5. 没有依据的信息不要编造，必要时直接说资料不足。
"""

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_md)

    print(f"已生成：{skill_path}")


def main():
    parser = argparse.ArgumentParser(description="导师 Skill 文件管理器")
    parser.add_argument("--action", required=True, choices=["list", "init", "combine"])
    parser.add_argument("--base-dir", default="./mentors", help="基础目录")
    parser.add_argument("--slug", help="导师代号")
    args = parser.parse_args()

    if args.action == "list":
        list_skills(args.base_dir)
    elif args.action == "init":
        if not args.slug:
            print("错误：init 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == "combine":
        if not args.slug:
            print("错误：combine 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == "__main__":
    main()
