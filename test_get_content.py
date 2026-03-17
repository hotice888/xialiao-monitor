#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试获取帖子和评论的完整内容"""

from xialiao_api import XialiaoAPI
import json
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

api = XialiaoAPI()

print('=' * 80)
print('测试：获取帖子完整内容和评论')
print('=' * 80)

# 获取热门帖子
posts_data = api._request('GET', '/posts?sort=hot&limit=3')
posts = posts_data.get('data', {}).get('items', [])

print(f'\n获取到 {len(posts)} 个帖子\n')

for i, post in enumerate(posts[:3], 1):
    print('-' * 80)
    print(f'【帖子 {i}】')
    print(f'ID: {post.get("id")}')
    print(f'标题：{post.get("title", "无标题")}')
    print(f'作者：{post.get("agent_name", post.get("author_name", "Unknown"))}')
    print(f'热度：{post.get("score", post.get("upvotes", 0))}')
    print(f'评论数：{post.get("comments_count", 0)}')
    print(f'\n内容:\n{post.get("content", "无内容")[:500]}')
    
    # 获取该帖子的评论
    post_id = post.get('id')
    if post_id:
        print(f'\n--- 评论列表 ---')
        comments_data = api._request('GET', f'/posts/{post_id}/comments?sort=new&limit=5')
        comments = comments_data.get('data', {}).get('items', [])
        
        if comments:
            for j, comment in enumerate(comments[:5], 1):
                print(f'\n  评论 {j}:')
                print(f'    作者：{comment.get("agent_name", comment.get("author_name", "Unknown"))}')
                print(f'    内容：{comment.get("content", "")[:100]}')
                print(f'    时间：{comment.get("created_at", "Unknown")}')
                print(f'    点赞：{comment.get("upvotes", 0)}')
        else:
            print('  暂无评论')
    print()

print('=' * 80)
print('测试完成！')
print('=' * 80)
