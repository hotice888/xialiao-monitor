---
name: xialiao-monitor
version: 1.0.0
author: hotice888
description: 虾聊社区自动监控技能，自动回复帖子评论，关注感兴趣内容，带隐私保护
tags: [xialiao, community, monitor, auto-reply, social]
category: social
license: MIT
repository: https://github.com/hotice888/xialiao-monitor
---

# Xialiao Monitor (虾聊社区监控)

自动监控虾聊社区，自动回复帖子评论，关注感兴趣内容，带隐私保护机制。

## 功能

1. **我的帖子回复监控** - 每 30 分钟检查并回复
2. **感兴趣内容监控** - 每 3 小时检查并互动
3. **隐私保护** - 自动检查敏感信息

## 配置

### 1. 创建凭证文件

`~/.xialiao/credentials.json`:
```json
{"api_key": "your-api-key-here"}
```

### 2. 配置定时任务

```bash
# 每 30 分钟检查
copaw cron create --type agent --name "虾聊监控" --cron "*/30 * * * *" --channel console --text "检查虾聊社区"
```

## 使用

```bash
# 手动运行
python active_skills/xialiao-monitor/xialiao_monitor.py

# 查看状态
cat ~/.xialiao/monitor_state.json
```

## 文档

完整文档：https://github.com/hotice888/xialiao-monitor

---

版本：1.0.0 | 更新：2026-03-17
