我已为你完整更新了README文档，适配隐藏敏感信息后的代码（环境变量配置），同时补充了时区依赖、虚拟环境等实际部署细节，确保文档准确且符合GitHub开源规范：

```markdown
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
- 🎨 自定义邮件样式，包含毛玻璃效果，适配中文显示
- 🕙 自动适配北京时间（UTC+8），避免时区偏差
- 📮 适配 QQ 邮箱 SMTP，可快速替换为其他邮箱
- 🔒 敏感信息通过环境变量配置，安全无泄露
- 🚀 轻量化部署，无多余依赖

### 前置条件
1. 已部署 Memos 并能访问其 SQLite 数据库文件（`memos_prod.db`）
2. 已开启邮箱 SMTP 服务（推荐 QQ 邮箱）
3. Python 3.6+ 环境
4. 安装依赖：
   ```bash
   # 基础依赖
   pip install requests markdown pytz
   # 推荐使用虚拟环境（避免污染系统环境）
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install requests markdown pytz
   ```

### 配置说明
#### 方式1：环境变量配置（推荐，安全无泄露）
```bash
# 临时生效（终端）
export MEMOS_DB_PATH="/你的/memos_prod.db绝对路径"
export SMTP_HOST="smtp.qq.com"
export SMTP_PORT="465"
export SMTP_USER="你的邮箱账号@qq.com"
export SMTP_PASS="你的邮箱SMTP授权码"
export BACKGROUND_COLOR="#f5f7fa"

# 永久生效（Linux/Mac，写入~/.bashrc）
echo "export MEMOS_DB_PATH='/你的/memos_prod.db绝对路径'" >> ~/.bashrc
echo "export SMTP_HOST='smtp.qq.com'" >> ~/.bashrc
echo "export SMTP_PORT='465'" >> ~/.bashrc
echo "export SMTP_USER='你的邮箱账号@qq.com'" >> ~/.bashrc
echo "export SMTP_PASS='你的邮箱SMTP授权码'" >> ~/.bashrc
source ~/.bashrc
```

#### 方式2：直接修改代码（仅本地测试使用）
```python
# 替换代码顶部的默认值
DB_PATH = "/你的/memos_prod.db绝对路径"
SMTP_USER = "你的邮箱账号@qq.com"
SMTP_PASS = "你的邮箱SMTP授权码"
```

#### SMTP 授权码获取方式（QQ 邮箱）
- 登录 QQ 邮箱 → 设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务
- 开启「SMTP 服务」→ 生成授权码（需验证密保）

### 使用方法
#### 1. 在 Memos 中添加提醒
在 Memos 笔记中按以下格式添加提醒（邮箱为接收提醒的邮箱）：
```
【提醒标题】
/remind 2024-01-17 14:30 接收邮箱@qq.com
【提醒内容（支持 Markdown）】
- 待办事项 1
- 待办事项 2
```
示例：
```
周一工作安排
/remind 2024-01-17 09:00 123456@qq.com
### 上午
- 9:30 项目例会
- 10:00 客户沟通

### 下午
- 14:00 代码评审
```

#### 2. 运行脚本
```bash
# 直接运行（虚拟环境中）
python memos_mail_reminder.py

# 添加定时任务（推荐，Linux/Mac）
# 编辑 crontab
crontab -e
# 添加每分钟执行（精准匹配时间）
* * * * * /你的/虚拟环境路径/venv/bin/python3 /你的/脚本路径/memos_mail_reminder.py >> /你的/日志路径/reminder.log 2>&1

# 1Panel 计划任务配置（可视化操作）
# 执行周期：* * * * *
# 脚本内容：
# source /你的/虚拟环境路径/venv/bin/activate && /你的/虚拟环境路径/venv/bin/python3 /你的/脚本路径/memos_mail_reminder.py >> /你的/日志路径/reminder.log 2>&1
```

#### 3. 验证效果
- 脚本会每分钟检查一次数据库
- 当北京时间与 `/remind` 标记的时间完全匹配时，自动发送邮件
- 运行日志会输出检测结果和邮件发送状态

### 常见问题
1. **数据库路径错误**：确保 `MEMOS_DB_PATH` 为绝对路径，且有读取权限
2. **SMTP 授权码错误**：确认使用的是授权码而非登录密码，且已开启SMTP服务
3. **邮件发送失败**：检查 SMTP 端口（QQ 邮箱为 465）、网络连接和防火墙规则
4. **Markdown 渲染异常**：确保已安装 `markdown` 库，版本≥3.0
5. **时区偏差**：确保已安装 `pytz` 库，脚本自动适配北京时间
6. **ModuleNotFoundError**：确保在虚拟环境中运行，且已安装所有依赖

### 自定义扩展
- 调整 `BACKGROUND_COLOR` 修改邮件背景色
- 替换 `SMTP_HOST` 和 `SMTP_PORT` 适配其他邮箱：
  - 163 邮箱：`smtp.163.com`，端口 465
  - Gmail：`smtp.gmail.com`，端口 465
  - 企业微信邮箱：`smtp.exmail.qq.com`，端口 465
- 修改邮件模板中的 CSS 样式，自定义字体、颜色和布局

---

## English
### Features
- 🕒 Detects Memos notes marked with `/remind` and sends timed email reminders
- 📝 Supports Markdown content, automatically converted to beautiful HTML emails
- 🎨 Custom email styles with frosted glass effects, optimized for Chinese display
- 🕙 Automatically adapts to Beijing Time (UTC+8) to avoid time zone deviation
- 📮 Adapted to QQ Mail SMTP, easily replaceable with other email providers
- 🔒 Sensitive information is configured via environment variables for security
- 🚀 Lightweight deployment with no redundant dependencies

### Prerequisites
1. Deployed Memos and can access its SQLite database file (`memos_prod.db`)
2. Enabled SMTP service for your email (QQ Mail recommended)
3. Python 3.6+ environment
4. Install dependencies:
   ```bash
   # Basic dependencies
   pip install requests markdown pytz
   # Recommended: use virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install requests markdown pytz
   ```

### Configuration
#### Method 1: Environment Variables (Recommended, Secure)
```bash
# Temporary effect (terminal)
export MEMOS_DB_PATH="/absolute/path/to/your/memos_prod.db"
export SMTP_HOST="smtp.qq.com"
export SMTP_PORT="465"
export SMTP_USER="your-email@qq.com"
export SMTP_PASS="your-smtp-auth-code"
export BACKGROUND_COLOR="#f5f7fa"

# Permanent effect (Linux/Mac, write to ~/.bashrc)
echo "export MEMOS_DB_PATH='/absolute/path/to/your/memos_prod.db'" >> ~/.bashrc
echo "export SMTP_HOST='smtp.qq.com'" >> ~/.bashrc
echo "export SMTP_PORT='465'" >> ~/.bashrc
echo "export SMTP_USER='your-email@qq.com'" >> ~/.bashrc
echo "export SMTP_PASS='your-smtp-auth-code'" >> ~/.bashrc
source ~/.bashrc
```

#### Method 2: Modify Code Directly (For Local Testing Only)
```python
# Replace default values at the top of the code
DB_PATH = "/absolute/path/to/your/memos_prod.db"
SMTP_USER = "your-email@qq.com"
SMTP_PASS = "your-smtp-auth-code"
```

#### How to get SMTP authorization code (QQ Mail)
- Log in to QQ Mail → Settings → Accounts → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Services
- Enable "SMTP Service" → Generate authorization code (need to verify security)

### Usage
#### 1. Add Reminders in Memos
Add reminders in Memos notes using the following format (email is the recipient's email):
```
[Reminder Title]
/remind 2024-01-17 14:30 recipient@qq.com
[Reminder Content (Markdown supported)]
- Todo item 1
- Todo item 2
```
Example:
```
Monday Work Schedule
/remind 2024-01-17 09:00 123456@qq.com
### Morning
- 9:30 Project meeting
- 10:00 Client communication

### Afternoon
- 14:00 Code review
```

#### 2. Run the Script
```bash
# Run directly (in virtual environment)
python memos_mail_reminder.py

# Add scheduled task (Recommended, Linux/Mac)
# Edit crontab
crontab -e
# Add execution every minute (for precise time matching)
* * * * * /path/to/your/venv/bin/python3 /path/to/your/script/memos_mail_reminder.py >> /path/to/your/log/reminder.log 2>&1

# 1Panel Scheduled Task Configuration (Visual Operation)
# Execution cycle: * * * * *
# Script content:
# source /path/to/your/venv/bin/activate && /path/to/your/venv/bin/python3 /path/to/your/script/memos_mail_reminder.py >> /path/to/your/log/reminder.log 2>&1
```

#### 3. Verify the Result
- The script checks the database every minute
- When Beijing Time exactly matches the time marked with `/remind`, an email is sent automatically
- The running log outputs detection results and email sending status

### Troubleshooting
1. **Database path error**: Ensure `MEMOS_DB_PATH` is an absolute path with read permissions
2. **SMTP authorization code error**: Confirm using authorization code instead of login password, and SMTP service is enabled
3. **Email sending failure**: Check SMTP port (465 for QQ Mail), network connection and firewall rules
4. **Markdown rendering exception**: Ensure `markdown` library is installed (version ≥3.0)
5. **Time zone deviation**: Ensure `pytz` library is installed, the script automatically adapts to Beijing Time
6. **ModuleNotFoundError**: Ensure running in virtual environment and all dependencies are installed

### Customization
- Adjust `BACKGROUND_COLOR` to modify the email background color
- Replace `SMTP_HOST` and `SMTP_PORT` to adapt to other email providers:
  - 163 Mail: `smtp.163.com`, port 465
  - Gmail: `smtp.gmail.com`, port 465
  - WeChat Work Mail: `smtp.exmail.qq.com`, port 465
- Modify CSS styles in the email template to customize fonts, colors and layouts

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  
本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 💡 Contributing
Contributions, issues and feature requests are welcome!  
欢迎提交贡献、反馈问题和提出功能需求！

## ⭐ Star History
[![Star History Chart](https://api.star-history.com/svg?repos=dadashuai7608/memos-mail-reminder&type=Date)](https://star-history.com/#dadashuai7608/memos-mail-reminder&Date)  
*Replace `dadashuai7608` with your actual GitHub username*
```
