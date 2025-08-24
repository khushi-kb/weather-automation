# Daily Weather Email Automation

This Python project fetches the current weather for a specified city using the OpenWeatherMap API and sends an email report using SendGrid. The process is fully automated with GitHub Actions to run daily.

---

## Features

- Retrieves live weather data including temperature, humidity, and weather description
- Sends email reports to multiple recipients
- Automates daily emails via a scheduled GitHub Actions workflow

---

## Prerequisites

- Python 3.x installed on your system
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))
- SendGrid account with API key ([Sign up here](https://sendgrid.com/))
- Verified sender email in SendGrid
- Recipient email addresses

---

## Installation

1. **Clone the repository:**

   git clone https://github.com/khushi-kb/weather-automation.git
   cd weather-automation

2. Install Python dependencies:

pip install -r requirements.txt

3. .env file

OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDER_EMAIL=your_verified_sender_email
RECIPIENT_EMAIL=your_recipient_email
