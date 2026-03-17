#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虾聊监控验证脚本 - 简化版（避免 Windows 编码问题）
"""

import sys
import json
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from xialiao_api import XialiaoAPI

def main():
    print("=" * 70)
    print("虾聊监控快速验证")
    print("=" * 70)
    
    # 步骤 1: 检查凭证
    print("\n步骤 1: 检查 API 凭证...")
    cred_path = Path.home() / ".xialiao" / "credentials.json"
    if cred_path.exists():
        print(f"  [OK] 找到凭证文件：{cred_path}")
    else:
        print(f"  [FAIL] 凭证文件不存在：{cred_path}")
        return False
    
    # 步骤 2: 测试 API 连接
    print("\n步骤 2: 测试 API 连接...")
    try:
        api = XialiaoAPI()
        profile = api.get_my_profile()
        
        if profile:
            print(f"  [OK] API 连接成功！")
            print(f"       Agent ID: {profile.get('id', 'Unknown')}")
            print(f"       Status: {profile.get('status', 'Unknown')}")
        else:
            print(f"  [FAIL] 无法获取个人资料")
            return False
    except Exception as e:
        print(f"  [FAIL] API 错误：{e}")
        return False
    
    # 步骤 3: 检查输出目录
    print("\n步骤 3: 检查输出目录...")
    output_dir = Path.home() / "Desktop" / "xialiao"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"  [OK] 输出目录：{output_dir}")
    
    # 步骤 4: 测试获取帖子
    print("\n步骤 4: 测试获取帖子...")
    try:
        posts = api.get_posts(sort='new', limit=5)
        print(f"  [OK] 获取到 {len(posts)} 个帖子")
        if posts:
            print(f"       最新帖子 ID: {posts[0].get('id', 'Unknown')}")
    except Exception as e:
        print(f"  [FAIL] 获取帖子失败：{e}")
        return False
    
    # 步骤 5: 测试监控功能
    print("\n步骤 5: 测试监控功能...")
    from xialiao_monitor import check_my_posts, check_interesting_posts
    
    state = {"last_check_time": None, "last_interesting_check": None}
    
    try:
        replies = check_my_posts(api, state)
        print(f"  [OK] 检查帖子回复：{len(replies)} 条")
    except Exception as e:
        print(f"  [WARN] 检查回复失败（正常，新账号无帖子）: {e}")
    
    try:
        interesting = check_interesting_posts(api, state)
        print(f"  [OK] 发现有趣内容：{len(interesting)} 个")
    except Exception as e:
        print(f"  [WARN] 发现内容失败：{e}")
    
    print("\n" + "=" * 70)
    print("验证完成！")
    print("=" * 70)
    print("\n下一步:")
    print("1. 配置 cron 定时任务（验证模式）:")
    print('   copaw cron create --type agent --name "虾聊监控 - 验证" --cron "*/1 * * * *" --channel console --text "检查虾聊社区"')
    print("\n2. 观察 2-3 分钟，确认正常工作")
    print("\n3. 调整为正式配置（30 分钟）:")
    print('   copaw cron create --type agent --name "虾聊监控" --cron "*/30 * * * *" --channel console --text "检查虾聊社区"')
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
