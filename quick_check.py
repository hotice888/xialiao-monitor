#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速查看虾聊社区动态 - Windows 兼容版"""

import requests
import json
import sys

API_KEY = 'xialiao_019cfced89f47656b5f6cf89d0c4c6ac'

def safe_str(s, max_len=50):
    """安全转换字符串，移除 emoji"""
    if not s:
        return ''
    # 移除 emoji (基本多文种平面外的字符)
    clean = ''.join(c for c in str(s)[:max_len] if ord(c) < 0x10000)
    return clean

def get_posts(limit=10):
    """获取最新帖子"""
    r = requests.get(
        f'https://xialiaoai.com/api/v1/posts?sort=new&limit={limit}',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    data = json.loads(r.content.decode('utf-8'))
    posts_data = data.get('data', {})
    if isinstance(posts_data, dict):
        return posts_data.get('items', [])
    return posts_data

def get_circles():
    """获取圈子列表"""
    r = requests.get(
        'https://xialiaoai.com/api/v1/circles',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    data = json.loads(r.content.decode('utf-8'))
    circles_data = data.get('data', {})
    if isinstance(circles_data, dict):
        return circles_data.get('items', [])
    return circles_data

if __name__ == '__main__':
    # 设置 stdout 为 UTF-8
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
    
    print('=' * 70)
    print('虾聊社区动态')
    print('=' * 70)
    print()
    
    # 获取帖子
    posts = get_posts(10)
    print(f'最新帖子 (共 {len(posts)} 个):')
    print('-' * 70)
    
    for i, post in enumerate(posts[:10], 1):
        title = safe_str(post.get('title', '无标题'))
        agent_name = safe_str(post.get('agent_name', post.get('author_name', 'Unknown')))
        content_preview = safe_str(post.get('content', '')[:30].replace('\n', ' '))
        print(f'{i}. [{agent_name}] {title}')
        if content_preview:
            print(f'   "{content_preview}..."')
    print()
    
    # 获取圈子
    circles = get_circles()
    print(f'热门圈子 (共 {len(circles)} 个):')
    print('-' * 70)
    
    for i, circle in enumerate(circles[:10], 1):
        name = safe_str(circle.get('name', 'Unknown'))
        members = circle.get('member_count', circle.get('members_count', 0))
        print(f'{i}. {name} ({members} 成员)')
    
    print()
    print('=' * 70)
