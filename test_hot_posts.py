#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试获取热门帖子"""

import requests
import json
import sys

API_KEY = 'xialiao_019cfced89f47656b5f6cf89d0c4c6ac'

def get_hot_posts(limit=10):
    r = requests.get(
        f'https://xialiaoai.com/api/v1/posts?sort=hot&limit={limit}',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    data = json.loads(r.content.decode('utf-8'))
    posts = data.get('data', {}).get('items', [])
    return posts

if __name__ == '__main__':
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
    
    posts = get_hot_posts(10)
    
    print('=' * 70)
    print('虾聊社区热门帖子 TOP 10')
    print('=' * 70)
    print()
    
    for i, post in enumerate(posts[:10], 1):
        title = post.get('title', '无标题')[:60]
        agent = post.get('agent_name', post.get('author_name', 'Unknown'))[:20]
        score = post.get('score', post.get('upvotes', 0))
        comments = post.get('comments_count', 0)
        content_preview = post.get('content', '')[:80].replace('\n', ' ')
        
        print(f'{i}. [{agent}] {title}')
        print(f'   🔥 热度：{score}  |  💬 评论：{comments}')
        if content_preview:
            print(f'   📝 "{content_preview}..."')
        print()
    
    print('=' * 70)
    print(f'共获取 {len(posts)} 条热门帖子')
