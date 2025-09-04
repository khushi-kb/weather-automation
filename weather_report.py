import os
import requests
import certifi
from datetime import datetime
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

if not all([OPENWEATHERMAP_API_KEY, SENDGRID_API_KEY, SENDER_EMAIL, RECIPIENT_EMAIL]):
    raise EnvironmentError(
        "One or more required environment variables are missing: "
        "OPENWEATHERMAP_API_KEY, SENDGRID_API_KEY, SENDER_EMAIL, RECIPIENT_EMAIL"
    )

CITY = "Noida"
OWM_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"  # Celsius

def unix_to_localtime(unix_timestamp, tz_offset_sec):
    dt = datetime.utcfromtimestamp(unix_timestamp + tz_offset_sec)
    return dt.strftime("%H:%M:%S")

def get_weather(city):
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": UNITS,
    }
    response = requests.get(OWM_URL, params=params, verify=False)
    response.raise_for_status() 
    return response.json()

def format_weather_report(data):
    main = data.get("main", {})
    wind = data.get("wind", {})
    sys = data.get("sys", {})
    clouds = data.get("clouds", {})
    weather_list = data.get("weather", [])
    visibility = data.get("visibility")
    rain = data.get("rain", {})
    snow = data.get("snow", {})
    timezone_offset = data.get("timezone", 0)

    weather_desc = weather_list[0]["description"].capitalize() if weather_list else "N/A"

    rain_vol = rain.get("1h") or rain.get("3h")
    snow_vol = snow.get("1h") or snow.get("3h")
    wind_gust = wind.get("gust")

    report = f"""\
🌡 Temperature:
  - Current: {main.get("temp", "N/A")} °C
  - Min: {main.get("temp_min", "N/A")} °C
  - Max: {main.get("temp_max", "N/A")} °C
  - Feels Like: {main.get("feels_like", "N/A")} °C

💧 Humidity & Pressure:
  - Humidity: {main.get("humidity", "N/A")}%
  - Pressure: {main.get("pressure", "N/A")} hPa

🌬 Wind:
  - Speed: {wind.get("speed", "N/A")} m/s
  - Direction: {wind.get("deg", "N/A")}°
  - Gust: {wind_gust if wind_gust is not None else "N/A"} m/s

🌫 Visibility & Clouds:
  - Visibility: {visibility if visibility is not None else "N/A"} meters
  - Cloudiness: {clouds.get("all", "N/A")}%

🌅 Sunrise & Sunset (local time):
  - Sunrise: {unix_to_localtime(sys.get("sunrise", 0), timezone_offset)}
  - Sunset: {unix_to_localtime(sys.get("sunset", 0), timezone_offset)}

☔ Precipitation:
  - Rain volume (last 1h or 3h): {rain_vol if rain_vol is not None else "0"} mm
  - Snow volume (last 1h or 3h): {snow_vol if snow_vol is not None else "0"} mm

📝 Weather Description:
  - {weather_desc}
"""
    return report

def send_email(subject, body, sender, recipients, api_key):
    message = Mail(
        from_email=sender,
        to_emails=[email.strip() for email in recipients.split(",")],
        subject=subject,
        plain_text_content=body,
    )
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            print("Email sent successfully.")
        else:
            print(f"Failed to send email. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    print(f"Fetching weather data for {CITY}...")
    weather_data = get_weather(CITY)
    report = format_weather_report(weather_data)
    subject = f"Weather Report for {CITY} - {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    print("Sending email...")
    send_email(subject, report, SENDER_EMAIL, RECIPIENT_EMAIL, SENDGRID_API_KEY)

if __name__ == "__main__":
    main()