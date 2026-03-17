#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
虾聊社区 API 客户端
实现完整的 API 调用功能
"""

import json
import os
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class XialiaoAPI:
    """虾聊社区 API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 API 客户端
        
        Args:
            api_key: API Key，如果不传则从配置文件读取
        """
        self.base_url = "https://xialiao.ai/api/v1"
        self.api_key = api_key or self._load_api_key()
        
        if not self.api_key:
            raise ValueError("API Key 未配置，请设置 XIALIAO_API_KEY 环境变量或创建凭证文件")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "CoPaw-XialiaoMonitor/1.0"
        })
    
    def _load_api_key(self) -> Optional[str]:
        """从配置文件加载 API Key"""
        credentials_file = Path.home() / ".xialiao" / "credentials.json"
        
        if credentials_file.exists():
            with open(credentials_file, 'r', encoding='utf-8') as f:
                creds = json.load(f)
                return creds.get('api_key')
        
        # 尝试从环境变量读取
        return os.getenv('XIALIAO_API_KEY')
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        发送 API 请求
        
        Args:
            method: HTTP 方法 (GET, POST, etc.)
            endpoint: API 端点
            data: 请求数据
            
        Returns:
            API 响应数据
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(method, url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 请求失败：{e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"响应内容：{e.response.text}")
            return {}
    
    def get_my_profile(self) -> Dict:
        """获取我的个人资料"""
        return self._request('GET', 'user/profile')
    
    def get_my_posts(self, page: int = 1, limit: int = 20) -> List[Dict]:
        """
        获取我的帖子列表
        
        Args:
            page: 页码
            limit: 每页数量
            
        Returns:
            帖子列表
        """
        params = {'page': page, 'limit': limit}
        result = self._request('GET', 'user/posts', data=params)
        return result.get('data', {}).get('posts', [])
    
    def get_post_detail(self, post_id: str) -> Dict:
        """
        获取帖子详情
        
        Args:
            post_id: 帖子 ID
            
        Returns:
            帖子详情
        """
        return self._request('GET', f'posts/{post_id}')
    
    def get_post_comments(self, post_id: str, page: int = 1, limit: int = 50) -> List[Dict]:
        """
        获取帖子评论
        
        Args:
            post_id: 帖子 ID
            page: 页码
            limit: 每页数量
            
        Returns:
            评论列表
        """
        params = {'page': page, 'limit': limit}
        result = self._request('GET', f'posts/{post_id}/comments', data=params)
        return result.get('data', {}).get('comments', [])
    
    def reply_to_comment(self, comment_id: str, content: str) -> bool:
        """
        回复评论
        
        Args:
            comment_id: 评论 ID
            content: 回复内容
            
        Returns:
            是否成功
        """
        data = {
            'content': content,
            'parent_comment_id': comment_id
        }
        result = self._request('POST', 'comments', data=data)
        return result.get('success', False)
    
    def create_comment(self, post_id: str, content: str) -> bool:
        """
        创建评论（回复帖子）
        
        Args:
            post_id: 帖子 ID
            content: 评论内容
            
        Returns:
            是否成功
        """
        data = {
            'post_id': post_id,
            'content': content
        }
        result = self._request('POST', 'comments', data=data)
        return result.get('success', False)
    
    def search_posts(self, query: str, tags: Optional[List[str]] = None, 
                     page: int = 1, limit: int = 20) -> List[Dict]:
        """
        搜索帖子
        
        Args:
            query: 搜索关键词
            tags: 标签列表
            page: 页码
            limit: 每页数量
            
        Returns:
            帖子列表
        """
        data = {
            'query': query,
            'page': page,
            'limit': limit
        }
        if tags:
            data['tags'] = tags
        
        result = self._request('POST', 'posts/search', data=data)
        return result.get('data', {}).get('posts', [])
    
    def get_posts_by_tag(self, tag: str, page: int = 1, limit: int = 20) -> List[Dict]:
        """
        获取特定标签的帖子
        
        Args:
            tag: 标签名
            page: 页码
            limit: 每页数量
            
        Returns:
            帖子列表
        """
        params = {'page': page, 'limit': limit}
        result = self._request('GET', f'tags/{tag}/posts', data=params)
        return result.get('data', {}).get('posts', [])
    
    def like_post(self, post_id: str) -> bool:
        """点赞帖子"""
        result = self._request('POST', f'posts/{post_id}/like')
        return result.get('success', False)
    
    def unlike_post(self, post_id: str) -> bool:
        """取消点赞帖子"""
        result = self._request('POST', f'posts/{post_id}/unlike')
        return result.get('success', False)


# 测试函数
def test_api():
    """测试 API 连接"""
    print("="*60)
    print("虾聊 API 测试")
    print("="*60)
    
    try:
        api = XialiaoAPI()
        print("[OK] API 客户端初始化成功")
        
        # 测试获取个人资料
        print("\n测试获取个人资料...")
        profile = api.get_my_profile()
        if profile:
            print(f"[OK] 获取成功：{profile.get('username', 'Unknown')}")
        else:
            print("[FAIL] 获取失败")
        
        # 测试获取我的帖子
        print("\n测试获取我的帖子...")
        posts = api.get_my_posts(limit=5)
        if posts:
            print(f"[OK] 获取成功，共 {len(posts)} 个帖子")
            for post in posts[:3]:
                print(f"  - {post.get('title', 'No title')} ({post.get('id')})")
        else:
            print("[FAIL] 暂无帖子或获取失败")
        
        print("\n" + "="*60)
        print("API 测试完成")
        print("="*60)
        
    except Exception as e:
        print(f"[FAIL] 测试失败：{e}")
        print("\n请检查:")
        print("1. API Key 是否正确配置")
        print("2. 网络连接是否正常")
        print("3. 凭证文件是否存在：~/.xialiao/credentials.json")
        print("\n创建凭证文件:")
        print('  mkdir ~/.xialiao')
        print('  echo {"api_key": "your-key-here"} > ~/.xialiao/credentials.json')


if __name__ == '__main__':
    test_api()
