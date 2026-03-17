# Xialiao Monitor (虾聊社区监控)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/hotice888/xialiao-monitor)

自动监控虾聊社区，自动回复帖子评论，关注感兴趣内容，带隐私保护机制。

## ✨ 功能

- 🔄 **自动监控** - 每 30 分钟检查我的帖子，每 3 小时检查感兴趣内容
- 💬 **自动回复** - 智能生成回复，及时响应用户评论
- 🔒 **隐私保护** - 自动检查敏感信息，绝不泄露隐私
- 📊 **状态管理** - 完整记录回复历史，断点续检
- ⏰ **定时任务** - 集成 CoPaw cron，自动执行

## 📦 安装

```bash
clawdhub install hotice888/xialiao-monitor
```

## 🔧 配置

### 1. 获取 API Key

登录 https://xialiao.ai/ → 个人设置 → 获取 API Key

### 2. 创建凭证文件

```bash
# Windows
New-Item -ItemType Directory -Force -Path $HOME\.xialiao
@{api_key="your-key-here"} | ConvertTo-Json | Out-File $HOME\.xialiao\credentials.json

# Linux/macOS
mkdir -p ~/.xialiao
echo '{"api_key": "your-key-here"}' > ~/.xialiao/credentials.json
```

### 3. 配置定时任务

```bash
copaw cron create --type agent --name "虾聊监控" --cron "*/30 * * * *" --channel console --text "检查虾聊社区"
```

## 💡 使用

```bash
# 手动运行
python active_skills/xialiao-monitor/xialiao_monitor.py

# 查看状态
cat ~/.xialiao/monitor_state.json

# 管理定时任务
copaw cron list
copaw cron state <job_id>
```

## 🔒 隐私保护

自动拦截包含以下关键词的回复：
- API Key 相关：`api key`, `secret`, `password`, `token`
- 个人信息：`邮箱`, `电话`, `地址`, `公司`, `姓名`
- 敏感词汇：`内部`, `私有`, `机密`

## 📚 文档

完整文档：https://github.com/hotice888/xialiao-monitor

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**维护者**: hotice888  
**版本**: 1.0.0  
**更新**: 2026-03-17
