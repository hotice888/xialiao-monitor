#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML 日志生成器 v4.0 - 优化布局"""

from pathlib import Path
from datetime import datetime
import json
import re

OUTPUT_DIR = Path.home() / "Desktop" / "xialiao"

def safe_str(s, max_len=200):
    """安全转换字符串"""
    if not s:
        return ''
    s = re.sub(r'<[^>]+>', '', str(s))
    clean = ''.join(c for c in s[:max_len] if ord(c) < 0x10000 or '\u4e00' <= c <= '\u9fff')
    return clean.replace('\n', '<br>').replace('"', '&quot;')

def generate_daily_html(logs, filepath):
    """生成每日 HTML 日志"""
    today = datetime.now().strftime('%Y-%m-%d')
    datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            min-height: 100vh;
            display: flex;
            font-size: 14px;
            line-height: 1.6;
            color: #333;
        }}
        
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
            color: #667eea;
            margin-bottom: 20px;
            font-size: 18px;
            text-align: center;
            padding-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
            font-weight: 600;
        }}
        
        /* 左侧统计卡片 - 紧凑布局 */
        .sidebar-stats {{
            margin-bottom: 20px;
            padding: 12px 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .sidebar-stat-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 6px;
            flex-wrap: nowrap;
        }}
        
        .sidebar-stat-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
            background: rgba(255, 255, 255, 0.15);
            padding: 8px 6px;
            border-radius: 8px;
            transition: all 0.2s ease;
            white-space: nowrap;
            flex: 1;
            justify-content: center;
            position: relative;
            min-width: 45px;
        }}
        
        .sidebar-stat-item:hover {{
            background: rgba(255, 255, 255, 0.25);
            transform: translateY(-2px);
        }}
        
        .sidebar-stat-icon {{
            font-size: 16px;
            line-height: 1;
        }}
        
        .sidebar-stat-number {{
            font-size: 16px;
            font-weight: 700;
            line-height: 1;
        }}
        
        .sidebar-stat-label {{
            font-size: 10px;
            opacity: 0;
            transition: opacity 0.2s ease;
            position: absolute;
            bottom: -20px;
            white-space: nowrap;
            pointer-events: none;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 3px 6px;
            border-radius: 4px;
            z-index: 10;
        }}
        
        .sidebar-stat-item:hover .sidebar-stat-label {{
            opacity: 1;
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
        
        .main-content {{
            flex: 1;
            margin-left: 260px;
            padding: 30px 40px;
            overflow-y: auto;
            height: 100vh;
        }}
        
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        .header {{
            background: rgba(255, 255, 255, 0.98);
            padding: 30px 35px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.3);
            display: flex;
            align-items: center;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 32px;
            margin: 0;
            font-weight: 800;
            display: inline;
            letter-spacing: 1px;
        }}
        
        .header-time {{
            color: #999;
            font-size: 15px;
            font-weight: 500;
            background: #f5f7fa;
            padding: 8px 16px;
            border-radius: 20px;
            white-space: nowrap;
            margin-left: 20px;
        }}
        
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
        
        .section-subtitle {{
            color: #667eea;
            font-size: 16px;
            margin: 25px 0 12px;
            font-weight: 600;
            padding-left: 12px;
            border-left: 4px solid #667eea;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 14px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            table-layout: fixed;
        }}
        
        .data-table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .data-table th {{
            color: white;
            padding: 14px 15px;
            text-align: center;
            font-weight: 600;
            font-size: 13px;
            vertical-align: middle;
            white-space: nowrap;
        }}
        
        .data-table td {{
            padding: 15px 15px;
            border-bottom: 1px solid #f0f0f0;
            vertical-align: middle;
            color: #444;
            line-height: 1.6;
        }}
        
        .data-table td:first-child,
        .data-table td:last-child {{
            text-align: center;
        }}
        
        .data-table tbody tr:hover {{
            background: linear-gradient(135deg, #667eea08 0%, #764ba208 100%);
        }}
        
        .data-table tbody tr:last-child td {{ border-bottom: none; }}
        
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
        .rank-other {{ background: #e0e0e0; color: #666; }}
        
        .title-wrapper {{
            white-space: normal;
            word-wrap: break-word;
            display: block;
            line-height: 1.6;
        }}
        
        .post-title {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        .post-title:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}
        
        .post-content, .comment-content {{
            color: #666;
            width: 100%;
            word-wrap: break-word;
            line-height: 1.5;
            font-size: 13px;
            background: #f8f9fa;
            padding: 8px 10px;
            border-radius: 6px;
            display: block;
        }}
        
        .hot-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 3px 8px;
            background: #fff5f5;
            border-radius: 10px;
            font-size: 11px;
            color: #ff6b6b;
            font-weight: 600;
            white-space: nowrap;
            margin: 2px;
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
        
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: rgba(255, 255, 255, 0.1); }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(102, 126, 234, 0.5);
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>🦞 监控时间线</h2>
        <div class="sidebar-stats">
            <div class="sidebar-stat-row">
                <div class="sidebar-stat-item">
                    <span class="sidebar-stat-icon">📊</span>
                    <span class="sidebar-stat-number">{len(logs)}</span>
                    <span class="sidebar-stat-label">监控</span>
                </div>
                <div class="sidebar-stat-item">
                    <span class="sidebar-stat-icon">💬</span>
                    <span class="sidebar-stat-number">{total_comments}</span>
                    <span class="sidebar-stat-label">评论</span>
                </div>
                <div class="sidebar-stat-item">
                    <span class="sidebar-stat-icon">📝</span>
                    <span class="sidebar-stat-number">{total_posts}</span>
                    <span class="sidebar-stat-label">发帖</span>
                </div>
                <div class="sidebar-stat-item">
                    <span class="sidebar-stat-icon">💌</span>
                    <span class="sidebar-stat-number">{total_replies}</span>
                    <span class="sidebar-stat-label">回复</span>
                </div>
            </div>
        </div>
        <div id="monitor-list">
'''
    
    sorted_logs = sorted(logs, key=lambda x: x.get('time', ''), reverse=True)
    for i, log in enumerate(sorted_logs):
        time_str = log.get('time', 'Unknown')
        stats = log.get('stats', {})
        active_class = 'active' if i == 0 else ''
        
        html += f'''
            <div class="monitor-item {active_class}" onclick="showSection('{log.get('id', 'section-0')}')">
                <div class="monitor-time">{time_str}</div>
                <div class="monitor-stats">
                    💬 {stats.get('comments', 0)} | 📝 {stats.get('posts', 0)} | 💌 {stats.get('replies', 0)}
                </div>
            </div>
'''
    
    html += f'''
        </div>
    </div>
    
    <div class="main-content">
        <div class="container">
            <div class="header">
                <h1>🦞 虾聊社区监控日志</h1>
                <span class="header-time">{datetime_now}</span>
            </div>
'''
    
    for i, log in enumerate(sorted_logs):
        active_class = 'active' if i == 0 else ''
        section_id = log.get('id', f'section-{i}')
        
        html += f'''
            <div class="monitor-section {active_class}" id="{section_id}">
'''
        
        # 评论他人帖子表格
        comments = log.get('comments', [])
        if comments:
            html += '<h3 class="section-subtitle">评论他人帖子</h3>'
            html += '''
                <table class="data-table">
                    <colgroup>
                        <col style="width: 60px;">
                        <col style="width: 25%;">
                        <col style="width: 35%;">
                        <col style="width: 30%;">
                    </colgroup>
                    <thead>
                        <tr>
                            <th>序号</th>
                            <th>主贴标题</th>
                            <th>内容概述</th>
                            <th>评论内容</th>
                        </tr>
                    </thead>
                    <tbody>
'''
            for i, comment in enumerate(comments, 1):
                post_url = comment.get('url', '#')
                html += f'''
                        <tr>
                            <td><span class="rank-badge rank-other">{i}</span></td>
                            <td><div class="title-wrapper"><a href="{post_url}" class="post-title" target="_blank">{safe_str(comment.get('title', ''), 50)}</a></div></td>
                            <td><div class="post-content">{safe_str(comment.get('content', ''), 150)}</div></td>
                            <td><div class="comment-content">{safe_str(comment.get('comment', ''), 100)}</div></td>
                        </tr>
'''
            html += '''
                    </tbody>
                </table>
'''
        
        # 自动发帖表格
        if log.get('posted'):
            html += '<h3 class="section-subtitle">自动发帖</h3>'
            html += '''
                <table class="data-table">
                    <colgroup>
                        <col style="width: 60px;">
                        <col style="width: 35%;">
                        <col style="width: 60%;">
                    </colgroup>
                    <thead>
                        <tr>
                            <th>序号</th>
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
                            <td><span class="rank-badge rank-other">1</span></td>
                            <td><div class="title-wrapper"><a href="{post_url}" class="post-title" target="_blank">{safe_str(post.get('title', ''), 60)}</a></div></td>
                            <td><div class="post-content">{safe_str(post.get('content', ''), 300)}</div></td>
                        </tr>
'''
            html += '''
                    </tbody>
                </table>
'''
        
        # 收到的回复表格
        replies = log.get('replies_received', [])
        if replies:
            html += '<h3 class="section-subtitle">收到的回复</h3>'
            html += '''
                <table class="data-table">
                    <colgroup>
                        <col style="width: 60px;">
                        <col style="width: 25%;">
                        <col style="width: 25%;">
                        <col style="width: 35%;">
                    </colgroup>
                    <thead>
                        <tr>
                            <th>序号</th>
                            <th>我的帖子</th>
                            <th>评论者</th>
                            <th>评论内容</th>
                        </tr>
                    </thead>
                    <tbody>
'''
            for i, reply in enumerate(replies, 1):
                post_title = safe_str(reply.get('post_title', ''), 50)
                html += f'''
                        <tr>
                            <td><span class="rank-badge rank-other">{i}</span></td>
                            <td><div class="title-wrapper"><span class="post-title">{post_title}</span></div></td>
                            <td>{safe_str(reply.get('commenter', ''), 20)}</td>
                            <td><div class="comment-content">{safe_str(reply.get('comment_content', ''), 100)}</div></td>
                        </tr>
'''
            html += '''
                    </tbody>
                </table>
'''
        
        # 热门帖子表格
        hot_posts = log.get('hot_posts', [])
        if hot_posts:
            html += '<h3 class="section-subtitle">热门帖子 TOP 10</h3>'
            html += '''
                <table class="data-table">
                    <colgroup>
                        <col style="width: 60px;">
                        <col style="width: 30%;">
                        <col style="width: 45%;">
                        <col style="width: 140px;">
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
                content = post.get('content', '') or '暂无内容'
                post_url = f'https://xialiaoai.com/p/{post.get("id", "#")}'
                score = post.get('score', post.get('upvotes', 0))
                comments_count = post.get('comments_count', 0)
                html += f'''
                        <tr>
                            <td><span class="rank-badge {rank_class}">{j}</span></td>
                            <td><div class="title-wrapper"><a href="{post_url}" class="post-title" target="_blank">{safe_str(post.get('title', ''), 60)}</a></div></td>
                            <td><div class="post-content">{safe_str(content, 150)}</div></td>
                            <td>
                                <span class="hot-badge">🔥 {score}</span>
                                <span class="hot-badge">💬 {comments_count}</span>
                            </td>
                        </tr>
'''
            html += '''
                    </tbody>
                </table>
'''
        
        html += '''
            </div>
'''
    
    html += '''
        </div>
    </div>
    
    <script>
        function showSection(sectionId) {
            document.querySelectorAll('.monitor-section').forEach(section => {
                section.classList.remove('active');
            });
            document.querySelectorAll('.monitor-item').forEach(item => {
                item.classList.remove('active');
            });
            const target = document.getElementById(sectionId);
            if (target) {
                target.classList.add('active');
            }
            if (event && event.currentTarget) {
                event.currentTarget.classList.add('active');
            }
        }
        
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
