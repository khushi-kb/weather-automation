import requests
import pandas as pd
import matplotlib.pyplot as plt
import schedule
import time
from datetime import datetime

# --- CONFIG ---
API_KEY = "992aa4054e3423461f5446bd9d5fc4fd"  # replace with your API key
CITY = "Delhi"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# --- FUNCTION TO FETCH WEATHER ---
def get_weather():
    response = requests.get(URL)
    data = response.json()

    if response.status_code != 200:
        print("Error fetching weather:", data.get("message", "Unknown error"))
        return None

    weather_info = {
        "City": CITY,
        "Temperature (°C)": data["main"]["temp"],
        "Feels Like (°C)": data["main"]["feels_like"],
        "Humidity (%)": data["main"]["humidity"],
        "Condition": data["weather"][0]["description"],
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return weather_info

# --- FUNCTION TO GENERATE REPORT ---
def generate_report():
    weather = get_weather()
    if weather:
        df = pd.DataFrame([weather])
        print("\n--- Today's Weather Report ---")
        print(df)

        # Save report to CSV
        df.to_csv("weather_report.csv", mode='a', index=False, header=False)

        # Plot temperature vs feels like
        df_plot = pd.read_csv("weather_report.csv", names=["City", "Temperature (°C)", "Feels Like (°C)", "Humidity (%)", "Condition", "Date"])
        plt.figure(figsize=(6,4))
        plt.plot(df_plot["Date"], df_plot["Temperature (°C)"], label="Temperature")
        plt.plot(df_plot["Date"], df_plot["Feels Like (°C)"], label="Feels Like")
        plt.xticks(rotation=45)
        plt.xlabel("Time")
        plt.ylabel("°C")
        plt.title(f"Weather Trend in {CITY}")
        plt.legend()
        plt.tight_layout()
        plt.savefig("weather_trend.png")
        plt.close()
        print("Report generated: weather_report.csv + weather_trend.png")

# --- SCHEDULER ---
# schedule.every().day.at("09:00").do(generate_report)  # runs daily at 9 AM
schedule.every(1).minutes.do(generate_report)


print("Weather automation started... Press CTRL+C to stop.")
generate_report()

while True:
    schedule.run_pending()
    time.sleep(60)
