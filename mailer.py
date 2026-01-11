import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console

console = Console()

def save_report_locally(html_content):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    filename = f"reports/stock_report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    return filename

def format_html_section(data, company):
    summary = data.get('answer', 'No summary available.')
    
    # Elegant Minimalist Logic
    accent_color = "#94a3b8"  # Slate (Neutral)
    status_label = "NEUTRAL"
    
    if any(word in summary.lower() for word in ["buy", "bullish", "strong"]):
        accent_color = "#10b981"  # Emerald
        status_label = "BULLISH"
    elif any(word in summary.lower() for word in ["sell", "bearish", "risks"]):
        accent_color = "#ef4444"  # Rose
        status_label = "BEARISH"

    section = f"""
    <div style="margin-bottom: 40px; padding: 0 10px;">
        <div style="margin-bottom: 12px;">
            <span style="font-size: 0.7rem; font-weight: 800; letter-spacing: 0.1em; color: {accent_color}; border: 1.5px solid {accent_color}; padding: 2px 8px; border-radius: 4px; margin-right: 12px; vertical-align: middle;">
                {status_label}
            </span>
            <h2 style="display: inline; margin: 0; font-size: 1.4rem; color: #1e293b; font-weight: 600; vertical-align: middle;">{company}</h2>
        </div>
        
        <div style="color: #475569; font-size: 1rem; line-height: 1.6; margin-bottom: 15px;">
            {summary}
        </div>
        
        <div style="border-top: 1px solid #f1f5f9; padding-top: 15px;">
            <ul style="padding-left: 0; list-style: none; margin: 0;">
    """
    for res in data.get('results', []):
        section += f"""
            <li style="margin-bottom: 8px;">
                <a href="{res['url']}" style="color: #3b82f6; text-decoration: none; font-size: 0.95rem;">
                    → {res['title']}
                </a>
            </li>
        """
    
    section += "</ul></div></div>"
    return section

def send_email(html_body, receiver_list):
    sender = os.getenv("SENDER_EMAIL")
    pwd = os.getenv("SENDER_PASSWORD")
    BOT_NAME = "AlphaPulse" 
    
    msg = MIMEMultipart()
    msg['Subject'] = f"{BOT_NAME} Intelligence | {datetime.now().strftime('%d %b')}"
    msg['From'] = f"{BOT_NAME} <{sender}>"
    
    # Display all recipients in the "To" field
    msg['To'] = ", ".join(receiver_list)

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin: 0; padding: 0; background-color: #ffffff; font-family: -apple-system, system-ui, sans-serif;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: auto; padding: 40px 20px;">
            <tr>
                <td style="padding-bottom: 40px; border-bottom: 2px solid #f8fafc;">
                    <h1 style="margin: 0; font-size: 1.8rem; color: #0f172a; font-weight: 800;">{BOT_NAME} <span style="color: #3b82f6;">Briefing</span></h1>
                    <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.9rem;">{datetime.now().strftime('%A, %d %B %Y')}</p>
                </td>
            </tr>
            <tr>
                <td style="padding-top: 40px;">
                    {html_body}
                </td>
            </tr>
            <tr>
                <td style="padding-top: 40px; border-top: 2px solid #f8fafc; text-align: center;">
                    <p style="font-size: 0.75rem; color: #cbd5e1; letter-spacing: 0.05em; text-transform: uppercase;">
                        Proprietary AI Analysis • For Information Only
                    </p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    msg.attach(MIMEText(full_html, 'html'))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, pwd)
            server.send_message(msg)
        return True, full_html
    except Exception as e:
        console.print(f"[bold red]Email Failed:[/bold red] {e}")
        return False, None