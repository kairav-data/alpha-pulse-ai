import os
import time
import schedule
from dotenv import load_dotenv
from tavily import TavilyClient
from mailer import send_email, format_html_section, console

load_dotenv()

COMPANIES = ["Reliance Industries", "HDFC Bank", "TCS", "Adani Enterprises"]

def run_job():
    console.print(f"[bold green]Check Started: {time.ctime()}[/bold green]")
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    # 1. Parse multiple emails from .env
    raw_emails = os.getenv("RECEIVER_EMAIL", "")
    receiver_list = [email.strip() for email in raw_emails.split(",") if email.strip()]
    
    if not receiver_list:
        console.print("[red]No receiver emails found in .env![/red]")
        return

    report_content = ""
    for company in COMPANIES:
        try:
            # Short query to stay under 400 chars
            query = f"Stock analysis {company} India buy sell catalysts news"
            res = client.search(query=query, topic="finance", search_depth="advanced", include_answer="advanced")
            report_content += format_html_section(res, company)
            console.print(f"✅ Processed {company}")
        except Exception as e:
            console.print(f"❌ {company} failed: {e}")

    if report_content:
        if send_email(report_content, receiver_list):
            console.print(f"[bold cyan]Email delivered to {len(receiver_list)} recipients![/bold cyan]")


schedule_time = os.getenv("SCHEDULE_TIME")
# Schedule for 08:00 AM daily
schedule.every().day.at(schedule_time).do(run_job)

console.print("[yellow]AlphaPulse Bot is Active. Waiting for 08:00...[/yellow]")

while True:
    schedule.run_pending()
    time.sleep(60)