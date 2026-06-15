# PR 🚀

自动化 GitHub Workflows 集合，让你的项目开发效率翻倍！

## ⚡ 包含的 Workflow

### 1. 🤖 AI Code Review (`pr-review.yml`)

每次有人提 PR 时自动触发，对代码进行全面审查：

| 检查项 | 说明 |
|--------|------|
| 🔴 **严重问题** | 密钥泄漏、合并冲突、SQL 注入风险 |
| 🟡 **警告** | 调试语句遗留、TODO/FIXME 标记、空文件 |
| 💡 **建议** | 大文件拆分建议、代码优化方向 |

**自动决策：**
- ✅ 无问题 → 自动 Approve
- 🟡 仅有警告 → Comment
- 🔴 有严重问题 → Request Changes

### 2. 📊 Daily Project Briefing (`daily-briefing.yml`)

每天北京时间早 8:05 自动生成项目日报并发布到 Issue：

- 📝 过去 24 小时的所有提交
- 🎯 活跃的 Issue 动态
- 🔀 打开的 Pull Request
- 🌿 最近更新的分支

## 🚀 使用方式

提个 PR 试试效果！Workflow 会自动运行 👀
