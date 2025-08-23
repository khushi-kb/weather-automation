import os
import requests
import json
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

def fetch_weather(city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def send_email(subject, content):
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    sender_email = os.getenv('SENDER_EMAIL')
    recipient_email = os.getenv('RECIPIENT_EMAIL')

    message = Mail(
        from_email=sender_email,
        to_emails=recipient_email,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    city = "Noida"  # Change this to your desired city
    weather_data = fetch_weather(city)

    if weather_data.get("cod") != 200:
        print(f"Error fetching weather data: {weather_data.get('message')}")
        return

    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    weather_description = weather_data['weather'][0]['description']

    subject = f"Weather Report for {city}"
    content = (f"Current Temperature: {temperature}°C\n"
               f"Humidity: {humidity}%\n"
               f"Weather Description: {weather_description.capitalize()}")

    send_email(subject, content)

if __name__ == "__main__":
    main()
