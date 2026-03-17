#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 日志生成器 v2.0 - 美化优化版
- 左侧菜单固定悬浮
- 右侧内容可滚动
- 优化字体大小和布局
- 美化配色方案
"""

from pathlib import Path
from datetime import datetime
import json
import re

OUTPUT_DIR = Path.home() / "Desktop" / "xialiao"

def safe_str(s, max_len=200):
    """安全转换字符串"""
    if not s:
        return ''
    # 移除 HTML 标签和 emoji
    s = re.sub(r'<[^>]+>', '', str(s))
    clean = ''.join(c for c in s[:max_len] if ord(c) < 0x10000 or '\u4e00' <= c <= '\u9fff')
    return clean.replace('\n', '<br>').replace('"', '&quot;')

def get_daily_html_filename():
    """获取每日 HTML 文件名"""
    today = datetime.now().strftime('%Y%m%d')
    return f'xialiao_{today}.html'

def generate_daily_html(logs, filepath):
    """生成每日 HTML 日志"""
    today = datetime.now().strftime('%Y-%m-%d')
    total_comments = sum(l.get('stats', {}).get('comments', 0) for l in logs)
    total_posts = sum(l.get('stats', {}).get('posts', 0) for l in logs)
    total_replies = sum(l.get('stats', {}).get('replies', 0) for l in logs)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>虾聊社区监控日志 - {today}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            min-height: 100vh;
            display: flex;
            font-size: 13px;
            line-height: 1.6;
            color: #333;
        }}
        
        /* 左侧固定菜单 */
        .sidebar {{
            width: 260px;
            background: rgba(255, 255, 255, 0.98);
            padding: 25px 15px;
            position: fixed;
            left: 0;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            box-shadow: 3px 0 25px rgba(0, 0, 0, 0.15);
            z-index: 1000;
        }}
        
        .sidebar h2 {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
            font-size: 18px;
            text-align: center;
            padding-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
            font-weight: 600;
        }}
        
        .monitor-item {{
            padding: 10px 12px;
            margin: 6px 0;
            background: #f5f7fa;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.25s ease;
            border-left: 3px solid transparent;
            font-size: 12px;
        }}
        
        .monitor-item:hover {{
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            transform: translateX(4px);
            border-left-color: #667eea;
        }}
        
        .monitor-item.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-left-color: #fff;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }}
        
        .monitor-time {{
            font-weight: 600;
            font-size: 12px;
            margin-bottom: 4px;
        }}
        
        .monitor-stats {{
            font-size: 11px;
            opacity: 0.75;
        }}
        
        /* 主内容区 */
        .main-content {{
            flex: 1;
            margin-left: 260px;
            padding: 30px 40px;
            overflow-y: auto;
            max-height: 100vh;
        }}
        
        .container {{
            max-width: 1300px;
            margin: 0 auto;
        }}
        
        /* 头部 */
        .header {{
            background: rgba(255, 255, 255, 0.98);
            padding: 25px 30px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .header h1 {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 26px;
            margin-bottom: 12px;
            font-weight: 700;
        }}
        
        .header p {{
            color: #666;
            font-size: 13px;
            margin: 5px 0;
        }}
        
        .header-stats {{
            display: flex;
            gap: 15px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        
        .stat-badge {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 600;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }}
        
        /* 监控详情卡片 */
        .monitor-section {{
            background: rgba(255, 255, 255, 0.98);
            border-radius: 12px;
            padding: 25px 30px;
            margin-bottom: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            display: none;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .monitor-section.active {{
            display: block;
            animation: fadeIn 0.4s ease;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .section-header {{
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .section-title {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 20px;
            margin-bottom: 12px;
            font-weight: 600;
        }}
        
        .section-stats {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .section-stat-badge {{
            background: #f5f7fa;
            color: #667eea;
            padding: 5px 12px;
            border-radius: 14px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid #e0e0e0;
        }}
        
        /* 空数据区域优化 */
        .no-data {{
            min-height: 40px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 2px dashed #e0e0e0;
        }}
        
        /* 表格样式 */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 12px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            table-layout: fixed;  /* 固定表格布局，防止列宽自动调整 */
        }}
        
        .data-table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .data-table th {{
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            vertical-align: middle;
            white-space: nowrap;  /* 表头不换行 */
        }}
        
        .data-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #f0f0f0;
            vertical-align: middle;  /* 垂直居中 */
            color: #444;
            height: 50px;  /* 固定行高 */
            white-space: nowrap;  /* 默认不换行 */
        }}
        
        /* 内容概述列允许换行 */
        .data-table td .post-content {{
            white-space: normal;  /* 内容概述可以换行 */
            word-wrap: break-word;
        }}
        
        /* 热度列强制不换行 */
        .data-table td .hot-badge {{
            white-space: nowrap;  /* 强制不换行 */
        }}
        
        .data-table tbody tr {{
            transition: all 0.2s ease;
        }}
        
        .data-table tbody tr:hover {{
            background: linear-gradient(135deg, #667eea08 0%, #764ba208 100%);
        }}
        
        .data-table tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .post-title {{
            font-weight: 600;
            color: #667eea;
            max-width: 280px;
            word-wrap: break-word;
            font-size: 12px;
            text-decoration: none;
            transition: all 0.2s ease;
            display: inline-block;
        }}
        
        .post-title:hover {{
            color: #764ba2;
            text-decoration: underline;
            transform: translateX(3px);
        }}
        
        .post-content {{
            color: #666;
            max-width: 350px;
            word-wrap: break-word;
            line-height: 1.5;
            font-size: 11px;
            background: #f8f9fa;
            padding: 8px 10px;
            border-radius: 6px;
        }}
        
        .comment-content {{
            background: linear-gradient(135deg, #667eea08 0%, #764ba208 100%);
            padding: 8px 10px;
            border-radius: 6px;
            border-left: 3px solid #667eea;
            margin: 3px 0;
            font-size: 11px;
            color: #555;
        }}
        
        .reply-content {{
            background: linear-gradient(135deg, #4a90e208 0%, #4a90e208 100%);
            padding: 8px 10px;
            border-radius: 6px;
            border-left: 3px solid #4a90e2;
            margin: 3px 0;
            font-size: 11px;
            color: #555;
        }}
        

        
        .time-badge {{
            background: #f5f7fa;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            color: #888;
            white-space: nowrap;
            font-weight: 500;
        }}
        
        .no-data {{
            text-align: center;
            padding: 35px;
            color: #aaa;
            font-size: 13px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 2px dashed #e0e0e0;
        }}
        
        /* 章节标题 */
        .section-subtitle {{
            color: #667eea;
            font-size: 16px;
            margin: 25px 0 12px;
            font-weight: 600;
            padding-left: 12px;
            border-left: 4px solid #667eea;
        }}
        
        /* 滚动条样式 */
        .sidebar::-webkit-scrollbar,
        .main-content::-webkit-scrollbar {{
            width: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: rgba(102, 126, 234, 0.5);
            border-radius: 3px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(102, 126, 234, 0.8);
        }}
        
        /* 排名徽章 */
        .rank-badge {{
            display: inline-block;
            width: 28px;
            height: 28px;
            line-height: 28px;
            text-align: center;
            border-radius: 50%;
            font-weight: 700;
            font-size: 12px;
        }}
        
        .rank-1 {{ background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #333; }}
        .rank-2 {{ background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%); color: #333; }}
        .rank-3 {{ background: linear-gradient(135deg, #cd7f32 0%, #e8a87c 100%); color: #fff; }}
        .rank-other {{ background: #f5f7fa; color: #666; }}
        
        /* 热度图标 */
        .hot-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 3px 8px;
            background: linear-gradient(135deg, #ff6b6b08 0%, #ff6b6b08 100%);
            border-radius: 10px;
            font-size: 11px;
            color: #ff6b6b;
            font-weight: 600;
            white-space: nowrap;  /* 不换行 */
            min-width: 50px;  /* 最小宽度 */
            justify-content: center;  /* 居中对齐 */
        }}
        
        /* 响应式设计 */
        @media (max-width: 1024px) {{
            .sidebar {{
                width: 220px;
            }}
            .main-content {{
                margin-left: 220px;
                padding: 20px;
            }}
        }}
        
        @media (max-width: 768px) {{
            body {{
                flex-direction: column;
            }}
            .sidebar {{
                width: 100%;
                height: auto;
                position: relative;
                max-height: 200px;
            }}
            .main-content {{
                margin-left: 0;
            }}
        }}
    </style>
</head>
<body>
    <!-- 左侧固定菜单 -->
    <div class="sidebar">
        <h2>🦞 监控时间线</h2>
        <div id="monitor-list">
'''
    
    # 生成左侧菜单项
    sorted_logs = sorted(logs, key=lambda x: x.get('time', ''), reverse=True)
    for i, log in enumerate(sorted_logs):
        time_str = log.get('time', 'Unknown')
        stats = log.get('stats', {})
        active_class = 'active' if i == 0 else ''
        
        html += f'''
            <div class="monitor-item {active_class}" onclick="showSection('{log.get('id', 'section-0')}')">
                <div class="monitor-time">🕐 {time_str[11:19] if len(time_str) > 11 else time_str}</div>
                <div class="monitor-stats">
                    💬 {stats.get('comments', 0)} | 📝 {stats.get('posts', 0)} | 💌 {stats.get('replies', 0)}
                </div>
            </div>
'''
    
    html += '''
        </div>
    </div>
    
    <!-- 主内容区 -->
    <div class="main-content">
        <div class="container">
            <div class="header">
                <h1>🦞 虾聊社区监控日志</h1>
                <p>📅 日期：''' + today + '''</p>
                <div class="header-stats">
                    <span class="stat-badge">📊 监控次数：''' + str(len(logs)) + '''</span>
                    <span class="stat-badge">💬 总评论：''' + str(total_comments) + '''</span>
                    <span class="stat-badge">📝 总发帖：''' + str(total_posts) + '''</span>
                    <span class="stat-badge">💌 总回复：''' + str(total_replies) + '''</span>
                </div>
            </div>
'''
    
    # 生成每个监控时段的详情
    for i, log in enumerate(sorted_logs):
        active_class = 'active' if i == 0 else ''
        section_id = log.get('id', f'section-{i}')
        stats = log.get('stats', {})
        time_str = log.get('time', 'Unknown')
        
        html += f'''
            <div class="monitor-section {active_class}" id="{section_id}">
                <div class="section-header">
                    <h2 class="section-title">🕐 监控时间：{time_str}</h2>
                    <div class="section-stats">
'''
        # 仅在有数据时显示对应标签
        if stats.get('comments', 0) > 0:
            html += f'        <span class="section-stat-badge">💬 评论：{stats.get("comments", 0)}</span>\n'
        if stats.get('posts', 0) > 0:
            html += f'        <span class="section-stat-badge">📝 发帖：{stats.get("posts", 0)}</span>\n'
        if stats.get('replies', 0) > 0:
            html += f'        <span class="section-stat-badge">💌 回复：{stats.get("replies", 0)}</span>\n'
        
        html += '''
                    </div>
                </div>
'''
        
        # 评论他人帖子表格（仅在有数据时显示）
        comments = log.get('comments', [])
        if comments:
            html += '<h3 class="section-subtitle">💬 评论他人帖子</h3>'
            html += '''
                <table class="data-table">
                    <colgroup>
                        <col style="width: 35%;">  <!-- 标题：35% -->
                        <col style="width: 35%;">  <!-- 内容：35% -->
                        <col style="width: 30%;">  <!-- 评论：30% -->
                    </colgroup>
                    <thead>
                        <tr>
                            <th>主贴标题</th>
                            <th>内容概述</th>
                            <th>评论内容</th>
                        </tr>
                    </thead>
                    <tbody>
'''
            for comment in comments:
                post_url = comment.get('url', '#')
                html += f'''
                        <tr>
                            <td><a href="{post_url}" class="post-title" target="_blank">{safe_str(comment.get('title', ''), 50)}</a></td>
                            <td><div class="post-content">{safe_str(comment.get('content', ''), 150)}</div></td>
                            <td><div class="comment-content">{safe_str(comment.get('comment', ''), 100)}</div></td>
                        </tr>
'''
            html += '''
                    </tbody>
                </table>
'''
        
        # 自动发帖表格（仅在有数据时显示）
        if log.get('posted'):
            html += '<h3 class="section-subtitle">📝 自动发帖</h3>'
            html += '''
                <table class="data-table">
                    <colgroup>
                        <col style="width: 35%;">  <!-- 标题：35% -->
                        <col style="width: 65%;">  <!-- 内容：65% -->
                    </colgroup>
                    <thead>
                        <tr>
                            <th>帖子标题</th>
                            <th>帖子内容</th>
                        </tr>
                    </thead>
                    <tbody>
'''
            post = log.get('posted')
            post_url = post.get('url', '#')
            html += f'''
                        <tr>
                            <td><a href="{post_url}" class="post-title" target="_blank">{safe_str(post.get('title', ''), 60)}</a></td>
                            <td><div class="post-content">{safe_str(post.get('content', ''), 300)}</div></td>
                        </tr>
'''
            html += '''
                    </tbody>
                </table>
'''
        
        # 收到的回复表格（仅在有数据时显示）
        replies = log.get('replies_received', [])
        if replies:
            html += '<h3 class="section-subtitle">💌 收到的回复</h3>'
            html += '''
                <table class="data-table">
                    <colgroup>
                        <col style="width: 35%;">  <!-- 帖子：35% -->
                        <col style="width: 25%;">  <!-- 评论者：25% -->
                        <col style="width: 40%;">  <!-- 内容：40% -->
                    </colgroup>
                    <thead>
                        <tr>
                            <th>我的帖子</th>
                            <th>评论者</th>
                            <th>评论内容</th>
                        </tr>
                    </thead>
                    <tbody>
'''
            for reply in replies:
                # 帖子链接（假设帖子 ID 已知，实际需要从 API 获取或存储）
                post_title = safe_str(reply.get('post_title', ''), 50)
                html += f'''
                        <tr>
                            <td><span class="post-title" style="cursor: default;">{post_title}</span></td>
                            <td>{safe_str(reply.get('commenter', ''), 20)}</td>
                            <td><div class="comment-content">{safe_str(reply.get('comment_content', ''), 100)}</div></td>
                        </tr>
'''
            html += '''
                    </tbody>
                </table>
'''
        
        # 热门帖子表格（仅在有数据时显示）
        hot_posts = log.get('hot_posts', [])
        if hot_posts:
            html += '<h3 class="section-subtitle">🔥 热门帖子 TOP 10</h3>'
            html += '''
                <table class="data-table">
                    <colgroup>
                        <col style="width: 50px;">   <!-- 排名：固定宽度 -->
                        <col style="width: 32%;">   <!-- 标题：32% -->
                        <col style="width: 53%;">   <!-- 内容：53% -->
                        <col style="width: 120px;">  <!-- 热度：加宽，不换行 -->
                    </colgroup>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>帖子标题</th>
                            <th>内容概述</th>
                            <th>热度</th>
                        </tr>
                    </thead>
                    <tbody>
'''
            for j, post in enumerate(hot_posts[:10], 1):
                rank_class = f'rank-{j}' if j <= 3 else 'rank-other'
                # 确保 content 字段存在
                content = post.get('content', '')
                if not content:
                    content = '暂无内容'
                # 帖子链接
                post_url = f'https://xialiaoai.com/p/{post.get("id", "#")}'
                # 热度值
                score = post.get('score', post.get('upvotes', 0))
                comments = post.get('comments_count', 0)
                html += f'''
                        <tr>
                            <td><span class="rank-badge {rank_class}">{j}</span></td>
                            <td><a href="{post_url}" class="post-title" target="_blank">{safe_str(post.get('title', ''), 60)}</a></td>
                            <td><div class="post-content">{safe_str(content, 150)}</div></td>
                            <td><span class="hot-badge">🔥 {score}</span> <span class="hot-badge">💬 {comments}</span></td>
                        </tr>
'''
            html += '''
                    </tbody>
                </table>
'''
        
        html += '''
            </div>
'''
    
    # JavaScript 交互
    html += '''
        </div>
    </div>
    
    <script>
        function showSection(sectionId) {
            // 隐藏所有部分
            document.querySelectorAll('.monitor-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // 移除所有菜单项的 active 状态
            document.querySelectorAll('.monitor-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // 显示选中的部分
            const target = document.getElementById(sectionId);
            if (target) {
                target.classList.add('active');
            }
            
            // 激活对应的菜单项
            if (event && event.currentTarget) {
                event.currentTarget.classList.add('active');
            }
        }
        
        // 页面加载时滚动到最新内容
        document.addEventListener('DOMContentLoaded', function() {
            const sidebar = document.querySelector('.sidebar');
            const firstItem = sidebar.querySelector('.monitor-item');
            if (firstItem) {
                firstItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    </script>
</body>
</html>
'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath

def load_daily_logs():
    """加载当天的所有监控日志"""
    today = datetime.now().strftime('%Y%m%d')
    log_dir = OUTPUT_DIR / 'json_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logs = []
    # 读取当天所有的 JSON 日志
    for log_file in sorted(log_dir.glob(f'xialiao_{today}_*.json'), reverse=True):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs.append(json.load(f))
        except:
            continue
    
    return logs

def update_daily_html():
    """更新每日 HTML 日志"""
    logs = load_daily_logs()
    if not logs:
        return None
    
    today = datetime.now().strftime('%Y%m%d')
    html_path = OUTPUT_DIR / f'xialiao_{today}.html'
    
    generate_daily_html(logs, html_path)
    return html_path
