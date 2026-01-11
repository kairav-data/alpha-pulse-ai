# 📈 AlphaPulse AI: Daily Market Intelligence

AlphaPulse is an automated financial research agent designed to bridge the gap between raw market news and actionable trading insights. Every morning, it scans the Indian stock market (NSE/BSE), analyzes catalysts using AI, and delivers a sleek, minimalistic report to your inbox.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![AI](https://img.shields.io/badge/Powered%20by-Gemini%20%26%20Tavily-orange)

## ✨ Key Features
- **🤖 Automated Sentiment Analysis:** Generates Bullish/Bearish recommendations based on real-time news catalysts.
- **📧 Minimalist Email Reports:** Sends elegant, dark-mode compatible HTML newsletters at 08:00 AM daily.
- **📂 Local Archiving:** Automatically saves a timestamped HTML copy of every report in the `/reports` directory.
- **🧹 Auto-Cleanup:** Built-in housekeeping to remove reports older than 30 days to save space.
- **⚡ High-Signal Data:** Uses Tavily Finance API to filter out "noise" and focus on institutional-grade financial news.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Search Engine:** [Tavily AI](https://tavily.com/) (Financial Topic Search)
- **Scheduling:** `schedule` library
- **UI/Logging:** `rich` library for beautiful terminal output
- **Email:** `smtplib` (SMTP_SSL)

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/alpha-pulse-ai.git](https://github.com/your-username/alpha-pulse-ai.git)
cd alpha-pulse-ai
