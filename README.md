# 机器人工程师学习路径 - GitHub Pages 部署指南

## 📦 已完成的准备工作

项目目录：`/Users/deane/Documents/workspace-other/robot-engineer-learning-path/`

已包含文件：
- `index.html` - 完整的学习路径书籍（暗色主题，响应式设计）
- `deploy.py` - 自动部署脚本

## 🚀 部署步骤

### 方式一：使用自动部署脚本（推荐）

在你的**本地终端**（Terminal.app 或 iTerm）中执行：

```bash
# 1. 进入项目目录
cd /Users/deane/Documents/workspace-other/robot-engineer-learning-path

# 2. 运行部署脚本
python3 deploy.py
```

脚本会提示你输入：
1. GitHub PAT（需要有 `repo` 权限）
2. GitHub 用户名

脚本会自动：
- 创建仓库（如已存在则跳过）
- 推送代码到 main 分支
- 启用 GitHub Pages

### 方式二：手动部署

如果自动脚本遇到问题，可以手动操作：

```bash
# 1. 进入项目目录
cd /Users/deane/Documents/workspace-other/robot-engineer-learning-path

# 2. 在 GitHub 网页上创建新仓库
#    仓库名：robot-engineer-learning-path
#    设为 Public
#    不要勾选 "Add a README file"

# 3. 添加 remote 并推送
git remote add origin https://github.com/<你的用户名>/robot-engineer-learning-path.git
git branch -M main
git push -u origin main

# 4. 在 GitHub 仓库 Settings > Pages 中启用
#    Source 选择 "Deploy from a branch"
#    Branch 选择 "main" / "(root)"
```

## 🔑 获取 GitHub PAT

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 token（仅显示一次）

## 📖 访问你的网站

部署成功后，访问地址：
```
https://<你的用户名>.github.io/robot-engineer-learning-path/
```

## 📝 书籍内容概览

- 01 软硬件基础（软件基础 + 硬件基础）
- 02 单片机核心（ARM Cortex-M + 通信协议 + 嵌入式系统）
- 03 机器人动力与底盘系统（传感器 + SLAM + 导航控制）
- 04 上位机开发（Python & Java + 通信中间件）
- 05 语音对话系统（ASR/TTS + NLP + 对话管理）
- 06 ROS2 核心（仿真 + 感知 + 控制 + 算法）
- 07 多机器人整机实战（单机产品化 + 多机协同）
- 08 端侧模型部署（模型压缩 + 边缘推理 + 具身智能）
- 09 云端模型部署（大模型微调 + 模型服务化 + Agent 架构）

每个模块包含详细的知识点网格、学习建议和实战项目推荐。

## ⚠️ 注意事项

- GitHub Pages 生效通常需要 1-2 分钟
- 如果访问 404，请等待后重试或检查 Settings > Pages 配置
- 如需自定义域名，在仓库 Settings > Pages > Custom domain 中配置
