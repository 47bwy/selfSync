# -*- encoding: utf-8 -*-
'''
@Time    :   2025/05/08 16:58:42
@Author  :   47bwy
@Desc    :   None
'''

import json
import os
import re
import zipfile
from base64 import b64encode
from datetime import datetime, timezone

EXPORT_ZIP = "/Users/apri/Downloads/597300db0f7054b476356d66d64dcb91f48f289030ad0e36ffb344708b04d735-2025-05-08-08-55-14-b8ab07cb15ae4d9e9b8e406b77bb43bb.zip"  # 导出的 ZIP 文件名
OUTPUT_DIR = "/Users/apri/Documents/chatgpt_markdown"    # 输出 Markdown 文件的目录


def slugify(title):
    return re.sub(r'[^\w\- ]', '', title).replace(' ', '_')[:50]


def format_time(raw):
    if isinstance(raw, (int, float)):  # 如果是 Unix 时间戳（秒）
        dt = datetime.fromtimestamp(raw, tz=timezone.utc)  # 使用 UTC 时区
    elif isinstance(raw, str):  # 如果是 ISO 8601 格式字符串
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    else:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%d_%H-%M")


def get_create_time(item):
    if "create_time" in item:
        return item["create_time"]
    mapping = item.get("mapping", {})
    for node in mapping.values():
        message = node.get("message")
        if message and "create_time" in message:
            return message["create_time"]
    return datetime.now().isoformat()  # fallback


def extract_images(content):
    # 如果有图片链接或 Base64 编码
    image_urls = re.findall(r'(https?://[^\s]+(?:\.jpg|\.jpeg|\.png|\.gif|\.bmp|\.svg))', content)
    base64_images = re.findall(r'data:image/[a-zA-Z]+;base64,[^\s]+', content)
    return image_urls, base64_images


def parse_chat(item):
    title = item.get("title", "untitled")
    raw_time = get_create_time(item)
    time = format_time(raw_time)
    messages = item.get("mapping", {})

    conversation = []
    for node in messages.values():
        msg = node.get("message")
        if not msg:
            continue
        role = msg.get("author", {}).get("role", "system")
        content_parts = msg.get("content", {}).get("parts", [])

        for part in content_parts:
            if isinstance(part, str):
                # 查找图片链接
                image_urls, base64_images = extract_images(part)
                if image_urls:
                    for url in image_urls:
                        part += f"\n\n![图片](<{url}>)"
                if base64_images:
                    for base64_data in base64_images:
                        part += f"\n\n![图片](<{base64_data}>)"

                if part.strip():
                    conversation.append((role, part.strip()))
            else:
                # 处理非字符串类型的 part
                print(f"警告：非字符串类型的 part: {part}")
                conversation.append((role, str(part)))

    return title, time, conversation


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with zipfile.ZipFile(EXPORT_ZIP, 'r') as zip_ref:
        zip_ref.extractall("extracted_data")

    json_path = os.path.join("extracted_data", "conversations.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"转换中，共 {len(data)} 条对话...")

    for i, item in enumerate(data):
        title, time, conversation = parse_chat(item)
        filename = f"{time}_{slugify(title)}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            for role, content in conversation:
                prefix = "🧑 **User:**" if role == "user" else "🤖 **ChatGPT:**"
                f.write(f"{prefix}\n\n{content}\n\n---\n\n")

    print(f"✅ 完成！Markdown 文件已保存在 {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
