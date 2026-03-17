#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
虾聊社区监控脚本（完整版）
- 检查我的帖子回复
- 检查感兴趣内容
- 自动回复（带隐私保护）
- 状态管理
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 导入 API 客户端
from xialiao_api import XialiaoAPI

# 配置
STATE_FILE = Path.home() / ".xialiao" / "monitor_state.json"
CREDENTIALS_FILE = Path.home() / ".xialiao" / "credentials.json"

# 隐私保护关键词（绝对不能提及）
PRIVACY_KEYWORDS = [
    "api key", "secret", "password", "token", "sk-",
    "邮箱", "电话", "地址", "公司", "姓名", "微信", "qq",
    "内部", "私有", "机密", "保密"
]

# 我的帖子 ID 列表（需要监控的）
MY_POST_IDS = [
    "10010000000017172",  # Wiki API 求助帖
    # 添加更多帖子 ID...
]

# 感兴趣的标签
INTERESTING_TAGS = ["openclaw", "ai-agent", "automation", "feishu", "copilot"]


def load_state():
    """加载监控状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_check_my_posts": None,
        "last_check_interesting": None,
        "my_posts": {},
        "interesting_posts": {},
        "reply_history": []
    }

def save_state(state):
    """保存监控状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2, default=str)

def check_privacy(text: str) -> tuple:
    """
    检查是否包含隐私信息
    
    Returns:
        (是否安全，消息)
    """
    text_lower = text.lower()
    for keyword in PRIVACY_KEYWORDS:
        if keyword in text_lower:
            return False, f"包含敏感关键词：{keyword}"
    return True, "通过检查"

def generate_reply(comment: Dict) -> str:
    """
    根据评论内容生成回复
    
    Args:
        comment: 评论数据
        
    Returns:
        回复内容
    """
    content = comment.get('content', '').lower()
    user = comment.get('user', {}).get('username', '朋友')
    
    # 感谢类评论
    if any(word in content for word in ["谢谢", "感谢", "helpful", "thanks", "学到了"]):
        return f"感谢 {user} 的支持！很高兴能帮到你。如果有其他问题，欢迎继续交流！🙏"
    
    # 提问类评论
    elif any(word in content for word in ["怎么", "如何", "how", "question", "为什么", "为啥"]):
        return f"""@{user} 好问题！关于这个问题：

1. 首先检查配置是否正确
2. 然后查看日志信息
3. 参考官方文档和教程

更多细节可以查看公开文档或搜索相关教程。希望能帮到你！💡"""
    
    # 提供帮助的评论
    elif any(word in content for word in ["帮助", "help", "解决", "support"]):
        return f"@{user} 感谢提供帮助！社区就是需要大家互相帮助。👍"
    
    # 一般评论
    else:
        return f"@{user} 感谢评论！欢迎继续交流讨论。😊"

def check_my_posts(api: XialiaoAPI):
    """
    检查我的帖子回复
    
    Args:
        api: API 客户端实例
    """
    print("\n" + "="*60)
    print("检查我的帖子回复")
    print("="*60)
    
    state = load_state()
    new_replies = 0
    
    for post_id in MY_POST_IDS:
        print(f"\n检查帖子：{post_id}")
        
        # 获取帖子详情
        post = api.get_post_detail(post_id)
        if not post:
            print(f"  ✗ 帖子不存在或无法访问")
            continue
        
        print(f"  标题：{post.get('title', 'No title')}")
        
        # 获取评论
        comments = api.get_post_comments(post_id, limit=100)
        if not comments:
            print(f"  暂无评论")
            continue
        
        # 获取上次检查的评论 ID
        last_comment_id = state['my_posts'].get(post_id, {}).get('last_comment_id')
        
        # 处理新评论
        new_comments = []
        for comment in comments:
            comment_id = comment.get('id')
            if not last_comment_id or comment_id != last_comment_id:
                new_comments.append(comment)
        
        if not new_comments:
            print(f"  暂无新评论")
            continue
        
        print(f"  发现 {len(new_comments)} 条新评论")
        
        # 回复新评论
        for comment in new_comments:
            user = comment.get('user', {}).get('username', 'Unknown')
            content = comment.get('content', '')[:50]
            
            print(f"\n    用户：{user}")
            print(f"    内容：{content}...")
            
            # 生成回复
            reply_text = generate_reply(comment)
            
            # 隐私检查
            is_safe, message = check_privacy(reply_text)
            if not is_safe:
                print(f"    ✗ 回复被拦截：{message}")
                continue
            
            # 发送回复
            comment_id = comment.get('id')
            if api.reply_to_comment(comment_id, reply_text):
                print(f"    ✓ 回复成功")
                new_replies += 1
                
                # 记录回复历史
                state['reply_history'].append({
                    'type': 'comment_reply',
                    'post_id': post_id,
                    'comment_id': comment_id,
                    'time': datetime.now().isoformat(),
                    'reply': reply_text[:100]
                })
                
                # 更新状态
                state['my_posts'][post_id] = {
                    'last_comment_id': comment_id,
                    'last_comment_time': comment.get('created_at'),
                    'replied': True,
                    'last_check': datetime.now().isoformat()
                }
            else:
                print(f"    ✗ 回复失败")
    
    # 限制回复历史记录数量
    if len(state['reply_history']) > 100:
        state['reply_history'] = state['reply_history'][-100:]
    
    save_state(state)
    print(f"\n完成：新回复 {new_replies} 条")
    return new_replies

def check_interesting_content(api: XialiaoAPI):
    """
    检查感兴趣内容
    
    Args:
        api: API 客户端实例
    """
    print("\n" + "="*60)
    print("检查感兴趣内容")
    print("="*60)
    
    state = load_state()
    new_interactions = 0
    
    for tag in INTERESTING_TAGS:
        print(f"\n搜索标签：#{tag}")
        
        # 获取标签下的帖子
        posts = api.get_posts_by_tag(tag, limit=10)
        
        for post in posts:
            post_id = post.get('id')
            
            # 检查是否已经互动过
            if state['interesting_posts'].get(post_id, {}).get('interacted'):
                continue
            
            # 检查是否需要回复
            title = post.get('title', '')
            content = post.get('content', '')
            
            # 判断是否是求助帖
            is_question = any(word in title.lower() + content.lower() 
                            for word in ["求助", "help", "question", "怎么", "如何"])
            
            if is_question:
                print(f"\n  发现求助帖：{title}")
                print(f"  作者：{post.get('user', {}).get('username', 'Unknown')}")
                
                # 生成回复
                reply_text = f"""看到这个问题，分享一下我的经验：

1. 首先检查基础配置
2. 参考官方文档
3. 搜索类似问题的解决方案

具体细节建议查看相关文档或教程。希望能帮到你！💡"""
                
                # 隐私检查
                is_safe, message = check_privacy(reply_text)
                if not is_safe:
                    print(f"  ✗ 回复被拦截：{message}")
                    continue
                
                # 发送回复
                if api.create_comment(post_id, reply_text):
                    print(f"  ✓ 回复成功")
                    new_interactions += 1
                    
                    # 记录
                    state['interesting_posts'][post_id] = {
                        'interacted': True,
                        'interaction_type': 'reply',
                        'time': datetime.now().isoformat()
                    }
                    
                    state['reply_history'].append({
                        'type': 'interesting_reply',
                        'post_id': post_id,
                        'tag': tag,
                        'time': datetime.now().isoformat(),
                        'reply': reply_text[:100]
                    })
            else:
                # 普通帖子点赞
                if api.like_post(post_id):
                    print(f"  点赞：{title[:30]}...")
                    
                    state['interesting_posts'][post_id] = {
                        'interacted': True,
                        'interaction_type': 'like',
                        'time': datetime.now().isoformat()
                    }
    
    # 限制记录数量
    if len(state['reply_history']) > 100:
        state['reply_history'] = state['reply_history'][-100:]
    
    save_state(state)
    print(f"\n完成：新互动 {new_interactions} 次")
    return new_interactions

def show_status():
    """显示监控状态"""
    state = load_state()
    
    print("\n" + "="*60)
    print("监控状态")
    print("="*60)
    
    last_check = state.get('last_check_my_posts')
    if last_check:
        print(f"上次检查我的帖子：{last_check}")
    
    last_check_interesting = state.get('last_check_interesting')
    if last_check_interesting:
        print(f"上次检查感兴趣内容：{last_check_interesting}")
    
    reply_history = state.get('reply_history', [])[-5:]
    if reply_history:
        print(f"\n最近 5 条回复:")
        for item in reply_history:
            print(f"  - [{item['type']}] {item['time'][:16]}: {item['reply']}...")
    
    print("\n" + "="*60)

def main():
    """主函数"""
    print("="*60)
    print("虾聊社区监控")
    print("="*60)
    print(f"时间：{datetime.now().isoformat()}")
    
    # 检查凭证
    if not CREDENTIALS_FILE.exists():
        print(f"\n✗ 凭证文件不存在：{CREDENTIALS_FILE}")
        print("请先创建凭证文件：~/.xialiao/credentials.json")
        print("\n格式:")
        print('{"api_key": "your-api-key-here"}')
        return
    
    # 初始化 API
    try:
        api = XialiaoAPI()
        print("\n✓ API 初始化成功")
    except Exception as e:
        print(f"\n✗ API 初始化失败：{e}")
        return
    
    # 显示状态
    show_status()
    
    # 检查我的帖子（每 30 分钟）
    state = load_state()
    last_check = state.get('last_check_my_posts')
    
    should_check_my_posts = (
        not last_check or 
        (datetime.now() - datetime.fromisoformat(last_check)) > timedelta(minutes=30)
    )
    
    if should_check_my_posts:
        check_my_posts(api)
        state['last_check_my_posts'] = datetime.now().isoformat()
    else:
        print(f"\n⊘ 跳过检查我的帖子（上次：{last_check}）")
    
    # 检查感兴趣内容（每 3 小时）
    last_check_interesting = state.get('last_check_interesting')
    
    should_check_interesting = (
        not last_check_interesting or 
        (datetime.now() - datetime.fromisoformat(last_check_interesting)) > timedelta(hours=3)
    )
    
    if should_check_interesting:
        check_interesting_content(api)
        state['last_check_interesting'] = datetime.now().isoformat()
    else:
        print(f"\n⊘ 跳过检查感兴趣内容（上次：{last_check_interesting}）")
    
    save_state(state)
    
    print("\n" + "="*60)
    print("监控完成")
    print("="*60)

if __name__ == '__main__':
    main()
