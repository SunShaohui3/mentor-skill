#!/usr/bin/env python3
"""微信聊天记录解析器。"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def detect_format(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".json":
        return "liuhen"
    if ext == ".csv":
        return "wechatmsg_csv"
    if ext in {".html", ".htm"}:
        return "wechatmsg_html"
    if ext in {".db", ".sqlite"}:
        return "pywxdump"
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            first_lines = f.read(2000)
        if re.search(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}", first_lines):
            return "wechatmsg_txt"
    return "plaintext"


def analyze_messages(messages: list, target_name: str) -> dict:
    target_msgs = [m for m in messages if target_name in m.get("sender", "")]
    user_msgs = [m for m in messages if target_name not in m.get("sender", "")]
    all_target_text = " ".join([m["content"] for m in target_msgs if m.get("content")])

    particles = re.findall(r"[啊呀呢吧嘛哦哈嗯]+", all_target_text)
    particle_freq = {}
    for particle in particles:
        particle_freq[particle] = particle_freq.get(particle, 0) + 1

    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
        r"\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
        r"\U00002702-\U000027B0\U0000FE00-\U0000FE0F"
        r"\U0001F900-\U0001F9FF]+",
        re.UNICODE,
    )
    emojis = emoji_pattern.findall(all_target_text)
    emoji_freq = {}
    for emoji in emojis:
        emoji_freq[emoji] = emoji_freq.get(emoji, 0) + 1

    msg_lengths = [len(m["content"]) for m in target_msgs if m.get("content")]
    avg_length = sum(msg_lengths) / len(msg_lengths) if msg_lengths else 0

    punctuation_counts = {
        "句号": all_target_text.count("。"),
        "感叹号": all_target_text.count("！") + all_target_text.count("!"),
        "问号": all_target_text.count("？") + all_target_text.count("?"),
        "省略号": all_target_text.count("...") + all_target_text.count("……"),
        "波浪号": all_target_text.count("~") + all_target_text.count("～"),
    }

    return {
        "target_name": target_name,
        "total_messages": len(messages),
        "target_messages": len(target_msgs),
        "user_messages": len(user_msgs),
        "analysis": {
            "top_particles": sorted(particle_freq.items(), key=lambda x: -x[1])[:10],
            "top_emojis": sorted(emoji_freq.items(), key=lambda x: -x[1])[:10],
            "avg_message_length": round(avg_length, 1),
            "punctuation_habits": punctuation_counts,
            "message_style": "short_burst" if avg_length < 20 else "long_form",
        },
        "sample_messages": [m["content"] for m in target_msgs[:50] if m.get("content")],
    }


def parse_wechatmsg_txt(file_path: str, target_name: str) -> dict:
    messages = []
    current_msg = None
    msg_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+)$")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            match = msg_pattern.match(line)
            if match:
                if current_msg:
                    messages.append(current_msg)
                timestamp, sender = match.groups()
                current_msg = {"timestamp": timestamp, "sender": sender.strip(), "content": ""}
            elif current_msg and line.strip():
                if current_msg["content"]:
                    current_msg["content"] += "\n"
                current_msg["content"] += line

    if current_msg:
        messages.append(current_msg)
    return analyze_messages(messages, target_name)


def parse_liuhen_json(file_path: str, target_name: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = []
    msg_list = data if isinstance(data, list) else data.get("messages", data.get("data", []))
    for msg in msg_list:
        messages.append(
            {
                "timestamp": msg.get("time", msg.get("timestamp", "")),
                "sender": msg.get("sender", msg.get("nickname", msg.get("from", ""))),
                "content": msg.get("content", msg.get("message", msg.get("text", ""))),
            }
        )
    return analyze_messages(messages, target_name)


def parse_plaintext(file_path: str, target_name: str) -> dict:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return {
        "raw_text": content,
        "target_name": target_name,
        "format": "plaintext",
        "message_count": 0,
        "analysis": {"note": "纯文本格式，需要结合人工判断。"},
    }


def main():
    parser = argparse.ArgumentParser(description="微信聊天记录解析器")
    parser.add_argument("--file", required=True, help="输入文件路径")
    parser.add_argument("--target", required=True, help="导师的名字或昵称")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--format", default="auto", help="文件格式")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)

    fmt = detect_format(args.file) if args.format == "auto" else args.format
    parsers = {
        "wechatmsg_txt": parse_wechatmsg_txt,
        "liuhen": parse_liuhen_json,
        "plaintext": parse_plaintext,
    }
    result = parsers.get(fmt, parse_plaintext)(args.file, args.target)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# 微信聊天记录分析 - {args.target}\n\n")
        f.write(f"来源文件：{args.file}\n")
        f.write(f"检测格式：{fmt}\n")
        f.write(f"总消息数：{result.get('total_messages', 'N/A')}\n")
        f.write(f"目标消息数：{result.get('target_messages', 'N/A')}\n\n")

        analysis = result.get("analysis", {})
        if analysis.get("top_particles"):
            f.write("## 高频语气词\n")
            for word, count in analysis["top_particles"]:
                f.write(f"- {word}: {count} 次\n")
            f.write("\n")

        if analysis.get("top_emojis"):
            f.write("## 高频 Emoji\n")
            for emoji, count in analysis["top_emojis"]:
                f.write(f"- {emoji}: {count} 次\n")
            f.write("\n")

        if analysis.get("punctuation_habits"):
            f.write("## 标点习惯\n")
            for punct, count in analysis["punctuation_habits"].items():
                f.write(f"- {punct}: {count} 次\n")
            f.write("\n")

        f.write("## 消息风格\n")
        f.write(f"- 平均消息长度：{analysis.get('avg_message_length', 'N/A')} 字\n")
        style = "短句连发型" if analysis.get("message_style") == "short_burst" else "长段落型"
        f.write(f"- 风格：{style}\n\n")

        if result.get("sample_messages"):
            f.write("## 消息样本（前 50 条）\n")
            for index, msg in enumerate(result["sample_messages"], 1):
                f.write(f"{index}. {msg}\n")

    print(f"分析完成，结果已写入 {args.output}")


if __name__ == "__main__":
    main()
