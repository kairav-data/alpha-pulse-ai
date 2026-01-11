import os
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from tavily import TavilyClient
from mailer import send_email, format_html_section, save_report_locally

load_dotenv()
console = Console()

# --- CONFIG ---
COMPANIES = ["Reliance Industries", "HDFC Bank", "TCS", "Adani Enterprises"]
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def run_analysis():
    console.print(f"\n[bold green]🚀 STARTING DAILY ANALYSIS - {datetime.now()}[/bold green]")
    client = TavilyClient(api_key=TAVILY_API_KEY)
    email_content = ""

    for company in COMPANIES:
        try:
            # SHORT QUERY to avoid "too long" error while triggering recommendation logic
            query = f"Recommend Buy/Sell for {company} India stock based on today's catalysts and news."
            
            response = client.search(
                query=query,
                topic="finance",
                search_depth="advanced",
                max_results=5,
                include_answer="advanced" # Essential for Buy/Sell logic
            )
            
            email_content += format_html_section(response, company)
            console.print(f"✅ Analyzed [cyan]{company}[/cyan]")
            
        except Exception as e:
            console.print(f"[bold red]Error with {company}:[/bold red] {e}")

    if email_content:
        success, full_html = send_email(email_content)
        path = save_report_locally(full_html)
        if success:
            console.print(f"[bold green]✉️ Report Sent & Saved to {path}[/bold green]")

# --- SCHEDULER ---
schedule.every().day.at("08:00").do(run_analysis)

console.print("[bold yellow]Bot is alive! Waiting for 08:00 AM...[/bold yellow]")

run_analysis() # Uncomment to test immediately

while True:
    schedule.run_pending()
    time.sleep(30)