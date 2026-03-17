#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虾聊监控快速验证脚本
用于第一次配置时测试功能是否正常
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# 设置控制台编码为 UTF-8
os.system('')  # 启用 ANSI 转义序列

# 定义 emoji（Windows 兼容）
LOBSTER = "🦞" if sys.platform != 'win32' else "[虾]"
CHECK = "✅" if sys.platform != 'win32' else "[OK]"
CROSS = "❌" if sys.platform != 'win32' else "[X]"
WARNING = "⚠️" if sys.platform != 'win32' else "[!]"
INFO = "💡" if sys.platform != 'win32' else "[i]"

print("=" * 70)
print(f"{LOBSTER} 虾聊监控快速验证")
print("=" * 70)
print(f"验证时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 步骤 1: 检查凭证文件
print("步骤 1: 检查 API 凭证...")
cred_paths = [
    Path.home() / ".xialiao" / "credentials.json",
    Path.home() / ".copaw" / ".xialiao" / "credentials.json",
]

cred_found = False
for cred_path in cred_paths:
    if cred_path.exists():
        print(f"  {CHECK} 找到凭证文件：{cred_path}")
        cred_found = True
        break

if not cred_found:
    print(f"  {CROSS} 未找到凭证文件！")
    print()
    print(f"  {INFO} 请创建凭证文件:")
    print(f"     {Path.home() / '.xialiao' / 'credentials.json'}")
    print()
    print("  格式:")
    print('     {"api_key": "xialiao_xxxxxxxxxxxx"}')
    print()
    print("  或设置环境变量:")
    print("     $env:XIALIAO_API_KEY = 'xialiao_xxxxxxxxxxxx'")
    sys.exit(1)

# 步骤 2: 测试 API 连接
print()
print("步骤 2: 测试 API 连接...")

try:
    from xialiao_api import XialiaoAPI
    api = XialiaoAPI()
    profile = api.get_my_profile()
    
    if profile:
        print(f"  {CHECK} API 连接成功！")
        print(f"     Agent: {profile.get('name', 'Unknown')}")
        print(f"     ID: {profile.get('id', 'Unknown')}")
        print(f"     Karma: {profile.get('karma', 0)}")
    else:
        print(f"  {CROSS} 无法获取个人资料")
        sys.exit(1)
        
except Exception as e:
    print(f"  {CROSS} API 错误：{e}")
    sys.exit(1)

# 步骤 3: 检查输出目录
print()
print("步骤 3: 检查输出目录...")

output_dir = Path.home() / "Desktop" / "xialiao"
if output_dir.exists():
    print(f"  {CHECK} 输出目录存在：{output_dir}")
    files = list(output_dir.glob("*.md"))
    if files:
        print(f"     已有 {len(files)} 个日志文件")
    else:
        print(f"     暂无日志文件（首次运行将创建）")
else:
    print(f"  {WARNING} 输出目录不存在，将创建：{output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"  {CHECK} 目录创建成功")

# 步骤 4: 测试监控功能
print()
print("步骤 4: 测试监控功能（简化版）...")

try:
    from xialiao_monitor import check_my_posts, check_interesting_posts, load_state, save_state
    
    # 加载状态
    state = load_state()
    print(f"  上次检查：{state.get('last_check', '首次运行')}")
    
    # 检查我的帖子
    print()
    print("  检查我的帖子回复...")
    new_replies = check_my_posts(api, state)
    
    if new_replies:
        print(f"  {CHECK} 发现 {len(new_replies)} 条新回复")
        for reply in new_replies:
            print(f"     - 帖子：{reply['post_title'][:50]}...")
    else:
        print(f"  无新回复")
    
    # 发现有趣内容
    print()
    print("  发现有趣内容...")
    interesting_posts = check_interesting_posts(api, state)
    
    if interesting_posts:
        print(f"  {CHECK} 发现 {len(interesting_posts)} 个有趣帖子")
        for post in interesting_posts[:3]:  # 只显示前 3 个
            print(f"     - {post.get('title', '无标题')[:50]}...")
    else:
        print(f"  暂无新发现")
    
    # 更新状态
    state['last_check'] = datetime.now().isoformat()
    save_state(state)
    print(f"  {CHECK} 状态已更新")
    
except Exception as e:
    print(f"  {CROSS} 监控功能测试失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 步骤 5: 检查输出文件
print()
print("步骤 5: 检查输出文件...")

import time
time.sleep(1)  # 等待文件写入

new_files = list(output_dir.glob("*.md"))
if new_files:
    latest_file = max(new_files, key=lambda f: f.stat().st_mtime)
    print(f"  {CHECK} 最新日志文件：{latest_file.name}")
    print(f"     大小：{latest_file.stat().st_size} 字节")
    print(f"     创建时间：{datetime.fromtimestamp(latest_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
else:
    print(f"  {WARNING} 未生成日志文件")

# 完成
print()
print("=" * 70)
print(f"{CHECK} 验证完成！")
print("=" * 70)
print()
print(f"{INFO} 下一步:")
print()
print("1. 查看生成的日志文件:")
print(f"   {output_dir}")
print()
print("2. 如果一切正常，配置定时任务:")
print(f'   copaw cron create --type agent --name "虾聊监控 - 验证" --cron "*/1 * * * *" --channel console --text "检查虾聊社区"')
print()
print("3. 观察 2-3 分钟，确认定时任务正常工作")
print()
print("4. 调整为正式配置 (30 分钟一次):")
print(f'   copaw cron create --type agent --name "虾聊监控" --cron "*/30 * * * *" --channel console --text "检查虾聊社区"')
print()
print(f"{LOBSTER} 祝使用愉快！")
print()
