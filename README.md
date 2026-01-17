# Memos Mail Reminder
A lightweight tool to send timed email reminders from Memos notes.  
一款轻量级工具，用于从 Memos 备忘录中发送定时邮件提醒。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Language / 语言
- [简体中文](#简体中文)
- [English](#english)

---

## 简体中文
### 功能特点
- 🕒 检测 Memos 中标记 `/remind` 的笔记，定时发送邮件提醒
- 📝 支持 Markdown 格式内容，自动转为美观的 HTML 邮件
- 🎨 自定义邮件样式，包含背景图和毛玻璃效果
- 📮 适配 QQ 邮箱 SMTP，可快速替换为其他邮箱
- 🚀 轻量化部署，无多余依赖

### 前置条件
1. 已部署 Memos 并能访问其 SQLite 数据库文件（`memos_prod.db`）
2. 已开启邮箱 SMTP 服务（推荐 QQ 邮箱）
3. Python 3.6+ 环境
4. 安装依赖：
   ```bash
   pip install requests markdown
   ```

### 配置说明
1. 下载代码后，修改核心配置项：
   ```python
   # 替换为你的 Memos 数据库路径
   DB_PATH = "xxxx/xxxx/xxxx/xxxx/memos_prod.db"
   
   # 邮件配置（QQ 邮箱示例）
   SMTP_USER = "xxxx@qq.com"  # 你的邮箱账号
   SMTP_PASS = "xxxxxxxxx"    # 邮箱 SMTP 授权码（非登录密码）
   ```
2. SMTP 授权码获取方式（QQ 邮箱）：
   - 登录 QQ 邮箱 → 设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务
   - 开启「SMTP 服务」→ 生成授权码

### 使用方法
#### 1. 在 Memos 中添加提醒
在 Memos 笔记中按以下格式添加提醒：
```
【提醒标题】
/remind 2024-01-17 14:30
【提醒内容（支持 Markdown）】
- 待办事项 1
- 待办事项 2
```
示例：
```
周一工作安排
/remind 2024-01-17 09:00
### 上午
- 9:30 项目例会
- 10:00 客户沟通

### 下午
- 14:00 代码评审
```

#### 2. 运行脚本
```bash
# 直接运行
python memos_mail_reminder.py

# 添加定时任务（推荐）
# 编辑 crontab
crontab -e
# 添加每分钟执行（精准匹配时间）
* * * * * /usr/bin/python3 /path/to/memos_mail_reminder.py >> /path/to/reminder.log 2>&1
```

#### 3. 验证效果
- 脚本会每分钟检查一次数据库
- 当系统时间与 `/remind` 标记的时间完全匹配时，自动发送邮件
- 运行日志会输出检测结果和邮件发送状态

### 常见问题
1. **数据库路径错误**：确保 `DB_PATH` 为绝对路径，且有读取权限
2. **SMTP 授权码错误**：确认使用的是授权码而非登录密码
3. **邮件发送失败**：检查 SMTP 端口（QQ 邮箱为 465）和网络连接
4. **Markdown 渲染异常**：确保已安装 `markdown` 库

### 自定义扩展
- 修改 `BACKGROUND_IMAGE` 更换邮件背景图
- 调整 `BACKGROUND_COLOR` 修改背景色
- 替换 `SMTP_HOST` 和 `SMTP_PORT` 适配其他邮箱：
  - 163 邮箱：`smtp.163.com`，端口 465
  - Gmail：`smtp.gmail.com`，端口 465

---

## English
### Features
- 🕒 Detects Memos notes marked with `/remind` and sends timed email reminders
- 📝 Supports Markdown content, automatically converted to beautiful HTML emails
- 🎨 Custom email styles with background image and frosted glass effects
- 📮 Adapted to QQ Mail SMTP, easily replaceable with other email providers
- 🚀 Lightweight deployment with no redundant dependencies

### Prerequisites
1. Deployed Memos and can access its SQLite database file (`memos_prod.db`)
2. Enabled SMTP service for your email (QQ Mail recommended)
3. Python 3.6+ environment
4. Install dependencies:
   ```bash
   pip install requests markdown
   ```

### Configuration
1. After downloading the code, modify the core configuration items:
   ```python
   # Replace with your Memos database path
   DB_PATH = "xxxx/xxxx/xxxx/xxxx/memos_prod.db"
   
   # Email configuration (QQ Mail example)
   SMTP_USER = "xxxx@qq.com"  # Your email address
   SMTP_PASS = "xxxxxxxxx"    # Email SMTP authorization code (not login password)
   ```
2. How to get SMTP authorization code (QQ Mail):
   - Log in to QQ Mail → Settings → Accounts → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Services
   - Enable "SMTP Service" → Generate authorization code

### Usage
#### 1. Add Reminders in Memos
Add reminders in Memos notes using the following format:
```
[Reminder Title]
/remind 2024-01-17 14:30
[Reminder Content (Markdown supported)]
- Todo item 1
- Todo item 2
```
Example:
```
Monday Work Schedule
/remind 2024-01-17 09:00
### Morning
- 9:30 Project meeting
- 10:00 Client communication

### Afternoon
- 14:00 Code review
```

#### 2. Run the Script
```bash
# Run directly
python memos_mail_reminder.py

# Add scheduled task (recommended)
# Edit crontab
crontab -e
# Add execution every minute (for precise time matching)
* * * * * /usr/bin/python3 /path/to/memos_mail_reminder.py >> /path/to/reminder.log 2>&1
```

#### 3. Verify the Result
- The script checks the database every minute
- When the system time exactly matches the time marked with `/remind`, an email is sent automatically
- The running log outputs detection results and email sending status

### Troubleshooting
1. **Database path error**: Ensure `DB_PATH` is an absolute path with read permissions
2. **SMTP authorization code error**: Confirm using authorization code instead of login password
3. **Email sending failure**: Check SMTP port (465 for QQ Mail) and network connection
4. **Markdown rendering exception**: Ensure the `markdown` library is installed

### Customization
- Modify `BACKGROUND_IMAGE` to change the email background image
- Adjust `BACKGROUND_COLOR` to modify the background color
- Replace `SMTP_HOST` and `SMTP_PORT` to adapt to other email providers:
  - 163 Mail: `smtp.163.com`, port 465
  - Gmail: `smtp.gmail.com`, port 465

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  
本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 💡 Contributing
Contributions, issues and feature requests are welcome!  
欢迎提交贡献、反馈问题和提出功能需求！

## ⭐ Star History
[![Star History Chart](https://api.star-history.com/svg?repos=your-username/memos-mail-reminder&type=Date)](https://star-history.com/#your-username/memos-mail-reminder&Date)  
*Replace `dadashuai7608` with your GitHub username*  
