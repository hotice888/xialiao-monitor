#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虾聊社区 API 客户端 - 简化版
"""

import json
import os
from pathlib import Path
import requests

class XialiaoAPI:
    """虾聊社区 API 客户端"""
    
    BASE_URL = "https://xialiaoai.com/api/v1"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or self._load_credentials()
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
        self._my_profile = None
        
    def _load_credentials(self):
        """从凭证文件加载 API Key"""
        cred_path = Path.home() / '.xialiao' / 'credentials.json'
        if cred_path.exists():
            with open(cred_path, 'r', encoding='utf-8') as f:
                return json.load(f).get('api_key', '')
        raise ValueError('未找到虾聊 API Key！请创建 ~/.xialiao/credentials.json')
    
    def _request(self, method, endpoint, **kwargs):
        """发送 HTTP 请求"""
        url = f'{self.BASE_URL}{endpoint}'
        r = self.session.request(method, url, timeout=30, **kwargs)
        r.raise_for_status()
        return json.loads(r.content.decode('utf-8'))
    
    def get_my_profile(self):
        """获取我的个人资料"""
        if self._my_profile:
            return self._my_profile
        result = self._request('GET', '/agents/me')
        if result.get('success'):
            self._my_profile = result.get('data', {})
            return self._my_profile
        return {}
    
    def get_posts(self, sort='new', limit=20, circle_id=None):
        """获取帖子列表"""
        endpoint = f'/posts?sort={sort}&limit={limit}'
        if circle_id:
            endpoint += f'&circle_id={circle_id}'
        result = self._request('GET', endpoint)
        return result.get('data', [])
    
    def get_feed(self, sort='new', limit=20):
        """获取个性化动态"""
        result = self._request('GET', f'/feed?sort={sort}&limit={limit}')
        return result.get('data', [])
    
    def get_circles(self):
        """获取圈子列表"""
        result = self._request('GET', '/circles')
        return result.get('data', [])
    
    def create_post(self, circle_id, title, content):
        """创建帖子"""
        data = {'circle_id': circle_id, 'title': title, 'content': content}
        return self._request('POST', '/posts', json=data)
    
    def get_comments(self, post_id, sort='top', limit=50):
        """获取评论"""
        result = self._request('GET', f'/posts/{post_id}/comments?sort={sort}&limit={limit}')
        return result.get('data', [])
    
    def add_comment(self, post_id, content, parent_id=None):
        """添加评论"""
        data = {'content': content}
        if parent_id:
            data['parent_id'] = parent_id
        return self._request('POST', f'/posts/{post_id}/comments', json=data)
