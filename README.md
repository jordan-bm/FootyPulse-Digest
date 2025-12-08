# FootyPulse Digest  
Automated Player Performance Digest (API-Football | Python | HTML | Jinja2 | Email Automation)

FootyPulse Digest is an automated analytics pipeline that processes historical football data to produce a weekly email digest. The system extracts fixtures, player statistics, lineups, computes advanced performance metrics, and compiles a polished HTML digest delivered via email.

This project utilizes full-stack data engineering: API ingestion, caching, analytics, templated rendering, and automated email delivery.

---

## Overview

FootyPulse Digest analyzes a selected league and season, applying custom scoring metrics to identify the top trending players. The digest includes:

- Top 10 trending players  
- Analytical metrics including form, usage, efficiency, and trend score  
- Automatically generated performance notes  
- Player spotlight cards with photos and team badges  
- A summary table for quick review  
- Automated email delivery  

---

## Features

### 1. Historical Data Pipeline (API-Football)
- Pulls fixtures, lineups, and player season statistics from API-Football  
- Caching system minimizes API usage: after the first run, the pipeline operates on cached data  
- Handles missing or inconsistent data   

### 2. Advanced Player Analytics
Each player receives a set of quantitative / qualitative metrics:

- Form normalization  
- Usage/consistency scoring  
- Goals-per-appearance efficiency  
- Trend score (0–10)  
- Automatically generated notes describing performance  

### 3. Templated Digest Rendering (Jinja2)
- Clean and responsive HTML email template  
- Summary table for quick comparison  
- Spotlight cards including metrics, team logos, and performance notes  

### 4. Email Automation
- Renders HTML digest  
- Sends via SMTP  
- No local files created - only upon request

---

## Analytical Methods

### Trend Score Components  
The model computes several features:

| Metric | Description |
|--------|-------------|
| Form | Normalized match rating (0–10) |
| Usage | Appearance frequency (reliability indicator) |
| Goals per Appearance | Efficiency metric |
| Consistency Score | Derived from usage normalization |
| Note | Generated from performance patterns |

### Trend Score Formula  

trend_score =
0.5 * form_normalized +
0.3 * goals_per_appearance_normalized +
0.2 * usage_normalized

Scaled to a 0–10 range.

---

## Setup Instructions

### 1. Clone Repository

git clone https://github.com/<jordan-bm>/FootyPulse-Digest.git
cd FootyPulse-Digest

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Configure Environment Variables

Create a `.env` file using the structure below (utilize .env.example):

API_FOOTBALL_KEY=your_api_key_here
API_FOOTBALL_HOST=v3.football.api-sports.io
SENDGRID_API_KEY=your_sendgrid_api_key
FOOTYPULSE_SENDER_EMAIL=your_verified_sender_email
FOOTYPULSE_RECEIVER_EMAIL=recipient@example.com

Notes:
- `API_FOOTBALL_KEY` is your API-Football key.
- `API_FOOTBALL_HOST` is required when using the RapidAPI/SendGrid header structure.
- `SENDGRID_API_KEY` is used by the email sending module.
- `FOOTYPULSE_SENDER_EMAIL` must be a verified sender in your SendGrid project.
- `FOOTYPULSE_RECEIVER_EMAIL` determines where the digest is delivered.

### 4. Run the Digest

python scripts/run_digest.py

The first run initializes the cache.
Subsequent runs require no additional API calls.

## Caching Strategy

To stay within API-Football free tier limits:

- Fixtures are cached once per league-season  
- Lineups are cached per fixture  
- Player statistics are cached per player-season  

After the first run, the digest executes entirely from cached data, allowing rapid iteration.

---

## Skills Demonstrated

- Python data engineering  
- REST API integration  
- Rate limit handling and response caching  
- Feature engineering and analytics design  
- Jinja2 templated HTML generation  
- SMTP email automation  
- Clean multi-module project structure  
- Documentation and production-quality packaging  

---

## Future Enhancements 

- Multi-league digest mode  
- Embedded charts for sparklines or rating trends  
- Local static dataset export  
- Player comparison tools  
- (If subscribed to paid API) - Live season statistics

Author

Jordan Burmylo-Magrann
GitHub: https://github.com/jordan-bm
