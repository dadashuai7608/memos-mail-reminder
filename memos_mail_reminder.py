import sqlite3
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
import os
import re
import markdown  
import pytz

DB_PATH = os.getenv("MEMOS_DB_PATH", "/opt/1panel/apps/memos/memos/memos/memos_prod.db") # 替换为你的memos_prod.db文件路径
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.qq.com")                                        # 邮件SMTP服务器（QQ邮箱无需修改，其他邮箱需调整）
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))                                             # SMTP端口
SMTP_USER = os.getenv("SMTP_USER", "your-email@qq.com")                                  # 发送邮件的邮箱账号
SMTP_PASS = os.getenv("SMTP_PASS", "your-smtp-auth-code")                                # 邮箱SMTP授权码
BACKGROUND_IMAGE = os.getenv("BACKGROUND_IMAGE", "")                                     # 邮件背景图
BACKGROUND_COLOR = os.getenv("BACKGROUND_COLOR", "#f5f7fa")                              # 背景图加载失败时的纯色背景


def markdown_to_html(md_content):
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.sane_lists',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ]
    html = markdown.markdown(md_content, extensions=extensions)
    md_css = """
    <style>
        .md-content h1 { font-size: 22px; color: #409EFF; margin: 10px 0; }
        .md-content h2 { font-size: 20px; color: #67C23A; margin: 8px 0; }
        .md-content h3 { font-size: 18px; color: #E6A23C; margin: 6px 0; }
        .md-content p { margin: 6px 0; line-height: 1.6; }
        .md-content ul, .md-content ol { margin: 6px 0 6px 20px; padding: 0; }
        .md-content li { margin: 3px 0; }
        .md-content blockquote { border-left: 4px solid #409EFF; padding: 6px 12px; margin: 8px 0; background: #f5f7fa; }
        .md-content code { background: #f2f2f2; padding: 2px 4px; border-radius: 4px; font-size: 14px; }
        .md-content pre { background: #f8f8f8; padding: 8px; border-radius: 6px; overflow-x: auto; margin: 8px 0; }
        .md-content table { border-collapse: collapse; width: 100%; margin: 8px 0; }
        .md-content th, .md-content td { border: 1px solid #e4e7ed; padding: 6px 10px; text-align: left; }
        .md-content th { background: #f5f7fa; }
    </style>
    """
    return f"<div class='md-content'>{md_css}{html}</div>"

def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_pattern, email) is not None

def send_beautiful_email(title, content, remind_time, to_email):
    try:
        clean_content = re.sub(r'/remind\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+[^\s]+', '', content).strip()
        md_html = markdown_to_html(clean_content)
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>备忘录提醒</title>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: {BACKGROUND_COLOR};
                    font-family: "Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei", Arial, sans-serif;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 10px;
                    border-radius: 15px;
                    backdrop-filter: blur(8px);
                    -webkit-backdrop-filter: blur(8px);
                    background-color: rgba(255, 255, 255, 0.85);
                    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
                }}
                .email-header {{
                    background: linear-gradient(120deg, #409EFF, #67C23A);
                    color: white;
                    padding: 18px;
                    border-radius: 10px 10px 0 0;
                    text-align: center;
                }}
                .email-body {{
                    padding: 22px;
                    border-radius: 0 0 10px 10px;
                }}
                .content-title {{
                    font-size: 19px;
                    color: #303133;
                    margin-bottom: 18px;
                    font-weight: bold;
                    border-left: 4px solid #409EFF;
                    padding-left: 10px;
                }}
                .remind-time {{
                    font-size: 14px;
                    color: #909399;
                    text-align: right;
                    padding-top: 8px;
                    margin-bottom: 15px;
                    border-bottom: 1px dashed #e4e7ed;
                    padding-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h2>📢 备忘录提醒</h2>
                </div>
                <div class="email-body">
                    <div class="content-title">{title}</div>
                    {md_html}
                    <div class="remind-time">提醒时间：{remind_time}（北京时间）</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = MIMEText(html_template, "html", "utf-8")
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = f"📌 备忘录提醒：{title}"
        
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"✅ 邮件发送成功：{title} | 收件人：{to_email}")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败（收件人：{to_email}）：{str(e)}")
        return False

def check_reminders():
    try:
        if not os.path.exists(DB_PATH):
            print(f"❌ 数据库不存在：{DB_PATH}")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM memo;")
        contents = [c[0] for c in cursor.fetchall() if c[0]]
        conn.close()

        if not contents:
            print("⚠️  未读取到任何备忘录")
            return

        print(f"📄 成功读取到 {len(contents)} 条备忘录")
        beijing_tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M")
        
        for content in contents:
            if "/remind " in content:
                remind_parts = content.split("/remind ")[1].split()
                if len(remind_parts) < 3:
                    print(f"⚠️  提醒格式错误（内容前50字）：{content[:50]}... | 正确格式：/remind 年-月-日 时:分 邮箱")
                    continue
                remind_time = f"{remind_parts[0]} {remind_parts[1]}"
                target_email = remind_parts[2]
                if not is_valid_email(target_email):
                    print(f"⚠️  邮箱格式错误（内容前50字）：{content[:50]}... | 错误邮箱：{target_email}")
                    continue
                print(f"🔍 检测到提醒：{content[:50]}... | 提醒时间：{remind_time} | 收件人：{target_email} | 当前北京时间：{now}")
                
                if remind_time == now:
                    title = content.split("/remind")[0].strip() or "无标题提醒"
                    send_beautiful_email(title, content, remind_time, target_email)

    except Exception as e:
        print(f"❌ 检查提醒失败：{str(e)}")

if __name__ == "__main__":
    print(f"[{datetime.now(pytz.timezone('Asia/Shanghai'))}] 开始检查Memos提醒（北京时间）...")
    check_reminders()
