# ❄️ Daily Snowfall Tracker  

This project fetches snowfall forecasts for ski and snowboard destinations near Irvine, California. It runs daily using **GitHub Actions** and sends an HTML-formatted snowfall report via email when snow is expected.  

## 🏔️ Tracked Destinations  
- **Mountain High** (Wrightwood, CA)  
- **Mt. Baldy** (Mt. Baldy, CA)  
- **Snow Summit** (Big Bear Lake, CA)  
- **Bear Mountain** (Big Bear Lake, CA)  
- **Snow Valley Mountain Resort** (Running Springs, CA)  

## 🚀 Features  
✅ **Daily Forecast Checks** – Runs every day at 9 AM Pacific Time  
✅ **OpenWeatherMap API Integration** – Retrieves snowfall data for the next 7 days  
✅ **Formatted Email Reports** – Sends a styled HTML table if snowfall is expected  
✅ **Secure API Key Handling** – Uses **GitHub Secrets** for API credentials  

## 📜 Setup Instructions  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/YOUR_USERNAME/snowfall-tracker.git
cd snowfall-tracker
```

### 2️⃣ Add Your OpenWeatherMap API Key  
Sign up for an API key at [OpenWeatherMap](https://openweathermap.org/api) and add it to GitHub Secrets:  
- Navigate to **Settings → Secrets and variables → Actions**  
- Click **New repository secret**  
- Name it **OPENWEATHER_API_KEY** and paste your API key  

### 3️⃣ Configure GitHub Actions  
The workflow file (`.github/workflows/daily_snowfall.yml`) is already set up to:  
- Run the script daily at 9 AM Pacific Time  
- Fetch snowfall forecasts  
- Send formatted email reports  

### 4️⃣ Run the Script Locally (Optional)  
To test the script manually:  
```bash
pip install requests
python snowfall_checker.py
```

## 📧 Email Notifications  
The script generates an **HTML email report** if snowfall is detected. To send emails, you can integrate an **SMTP service** (e.g., Gmail, SendGrid) by modifying `snowfall_checker.py` to send the output from `email_choice()`.

## 🤖 GitHub Actions Workflow  
The GitHub Actions workflow (`.github/workflows/daily_snowfall.yml`) schedules the job:  
```yaml
on:
  schedule:
    - cron: '0 16 * * *'  # Runs at 9 AM PT (16:00 UTC)
```
Modify the cron expression if you want a different schedule.

## 📌 Future Improvements  
- ⏳ Add a snowfall threshold (e.g., notify only if snowfall > 2 inches)  
- 📍 Expand to more ski resorts  
- 📤 Automate email notifications  

