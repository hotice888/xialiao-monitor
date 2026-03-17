# 发布虾聊监控技能到 GitHub

## 📋 发布步骤

### 步骤 1: 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名：`xialiao-monitor`
3. 描述：虾聊社区自动监控技能
4. 可见性：Public（公开）
5. **不要**初始化 README、.gitignore 或 license（我们已经有了）
6. 点击 "Create repository"

### 步骤 2: 获取仓库 URL

创建后，GitHub 会显示仓库 URL：
```
https://github.com/hotice888/xialiao-monitor.git
```

### 步骤 3: 添加远程仓库

```bash
cd C:\Users\Administrator\.copaw\active_skills\xialiao-monitor

# 添加远程仓库（替换为你的实际 URL）
git remote add origin https://github.com/hotice888/xialiao-monitor.git

# 或如果已存在
git remote set-url origin https://github.com/hotice888/xialiao-monitor.git
```

### 步骤 4: 推送到 GitHub

```bash
# 重命名分支为 main
git branch -M main

# 推送
git push -u origin main
```

**首次推送需要认证**:
- 输入 GitHub 用户名
- 输入 Personal Access Token（不是密码）

### 步骤 5: 验证推送

访问 https://github.com/hotice888/xialiao-monitor
确认文件已上传。

---

## 🔑 获取 Personal Access Token

如果还没有 Token：

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写说明（如：xialiao-monitor deploy）
4. 选择过期时间（建议 90 天）
5. 选择权限：
   - ✅ `repo` (Full control of private repositories)
6. 点击 "Generate token"
7. **复制并保存 Token**（只显示一次！）

---

## 🚀 快速推送脚本

运行 `push-to-github.bat`：

```bash
cd C:\Users\Administrator\.copaw\active_skills\xialiao-monitor
push-to-github.bat
```

脚本会：
1. 初始化 Git（如果未初始化）
2. 添加所有文件
3. 提交更改
4. 添加远程仓库
5. 推送到 GitHub

按提示输入 GitHub 凭证即可。

---

## ✅ 发布后检查

### 1. 检查仓库

访问 https://github.com/hotice888/xialiao-monitor

确认文件：
- ✅ README.md
- ✅ SKILL.md
- ✅ skill.json
- ✅ xialiao_api.py
- ✅ xialiao_monitor.py
- ✅ .gitignore

### 2. 测试 ClawHub 安装

```bash
# 先卸载（如果已安装）
clawdhub uninstall xialiao-monitor

# 重新安装
clawdhub install hotice888/xialiao-monitor
```

### 3. 更新 ClawHub 索引

如果是第一次发布，可能需要等待 ClawHub 索引更新（通常几分钟到几小时）。

---

## 🐛 故障排查

### 问题：权限错误

**错误**: `remote: Permission denied`

**解决**:
- 检查仓库 URL 是否正确
- 确认使用的是 Personal Access Token 而非密码
- 确认 Token 有 `repo` 权限

### 问题：仓库不存在

**错误**: `Repository not found`

**解决**:
- 确认已在 GitHub 创建仓库
- 检查仓库名拼写
- 确认仓库可见性（Public）

### 问题：认证失败

**错误**: `Authentication failed`

**解决**:
- 重新生成 Personal Access Token
- 清除 Git 凭证缓存：
  ```bash
  git credential-manager erase
  ```
- 重新推送

---

## 📝 发布清单

发布前检查：

- [ ] 已在 GitHub 创建仓库
- [ ] 已获取 Personal Access Token
- [ ] 本地 Git 已初始化
- [ ] 所有文件已提交
- [ ] 远程仓库 URL 已配置
- [ ] 已运行推送命令

发布后检查：

- [ ] 仓库页面显示所有文件
- [ ] README.md 正确显示
- [ ] 可以克隆仓库
- [ ] ClawHub 可以安装

---

## 🎉 发布成功！

发布成功后：

1. 更新 SKILL.md 中的仓库链接（如果不同）
2. 在虾聊社区发帖宣布
3. 分享给其他用户
4. 收集反馈并持续改进

---

**仓库**: https://github.com/hotice888/xialiao-monitor  
**版本**: 1.0.0  
**发布日期**: 2026-03-17
