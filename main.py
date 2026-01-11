import os
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient
# Importing your existing mailer functions
from mailer import send_email, format_html_section, save_report_locally, console

# Load environment variables (Local development uses .env, GitHub uses Secrets)
load_dotenv()

# Configuration
COMPANIES = ["Reliance Industries", "HDFC Bank", "TCS", "Adani Enterprises"]

def run_analysis():
    """
    Main execution logic for the daily stock report.
    This function runs once per trigger.
    """
    console.print(f"\n[bold green]🚀 AlphaPulse Analysis Started - {datetime.now().strftime('%Y-%m-%d %H:%M')}[/bold green]")
    
    # Initialize Tavily Client
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        console.print("[bold red]Error: TAVILY_API_KEY not found![/bold red]")
        return
        
    client = TavilyClient(api_key=api_key)
    
    # Parse recipient list from environment
    raw_emails = os.getenv("RECEIVER_EMAIL", "")
    receiver_list = [e.strip() for e in raw_emails.split(",") if e.strip()]
    
    if not receiver_list:
        console.print("[bold red]Error: No recipients found in RECEIVER_EMAIL![/bold red]")
        return

    html_payload = ""
    
    # Process each company
    for company in COMPANIES:
        try:
            console.print(f"🔍 Analyzing {company}...")
            query = f"Stock analysis and BUY/SELL recommendation for {company} India today."
            
            # Fetch AI research data
            res = client.search(
                query=query, 
                topic="finance", 
                search_depth="advanced", 
                include_answer="advanced"
            )
            
            # Format this section using your mailer's HTML template
            html_payload += format_html_section(res, company)
            console.print(f"✅ Successfully processed {company}")
            
        except Exception as e:
            console.print(f"[bold red]❌ Failed to analyze {company}:[/bold red] {e}")

    # Finalizing and Sending
    if html_payload:
        success, final_html = send_email(html_payload, receiver_list)
        if success:
            # Save a local copy (Note: GitHub Actions artifacts can store this)
            save_report_locally(final_html)
            console.print(f"[bold cyan]✨ Briefing delivered to {len(receiver_list)} recipients![/bold cyan]")
        else:
            console.print("[bold red]⚠️ Report generated but email failed to send.[/bold red]")
    else:
        console.print("[bold yellow]⚠️ No content generated. Email skipped.[/bold yellow]")

if __name__ == "__main__":
    # GitHub Actions calls the script directly
    run_analysis()