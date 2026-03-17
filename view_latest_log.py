#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查看最新监控日志"""

import os
from pathlib import Path
import io
import sys

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

output_dir = Path.home() / "Desktop" / "xialiao"
md_files = list(output_dir.glob("xialiao_*.md"))

if not md_files:
    print("未找到监控日志文件")
    exit(1)

# 获取最新文件
latest_file = max(md_files, key=os.path.getmtime)

print("=" * 70)
print(f"最新监控日志：{latest_file.name}")
print("=" * 70)
print()

with open(latest_file, 'r', encoding='utf-8') as f:
    content = f.read()
    
# 只打印热门帖子部分
lines = content.split('\n')
in_hot_section = False
for line in lines:
    if '## 🔥 热门帖子' in line:
        in_hot_section = True
    if in_hot_section:
        if line.startswith('## ') and '热门帖子' not in line:
            break
        print(line)

print()
print("=" * 70)
