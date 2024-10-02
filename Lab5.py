import requests
import streamlit as st
from openai import OpenAI

st.title("Weather Recommendation Bot")

def fetch_weather(city, api_key):
    if "," in city:
        city = city.split(",")[0].strip()

    base_url = "https://api.openweathermap.org/data/2.5/"
    endpoint = f"weather?q={city}&appid={api_key}"
    complete_url = base_url + endpoint

    response = requests.get(complete_url)
    weather_info = response.json()

    if response.status_code != 200:
        st.error("Unable to retrieve weather data. Check the city name.")
        return None

    temperature = weather_info['main']['temp'] - 273.15
    feels_like_temp = weather_info['main']['feels_like'] - 273.15
    min_temp = weather_info['main']['temp_min'] - 273.15
    max_temp = weather_info['main']['temp_max'] - 273.15
    humidity_level = weather_info['main']['humidity']

    return {
        "city": city,
        "temperature": round(temperature, 2),
        "feels_like": round(feels_like_temp, 2),
        "min_temp": round(min_temp, 2),
        "max_temp": round(max_temp, 2),
        "humidity": round(humidity_level, 2)
    }

def initialize_openai():
    return OpenAI(api_key=st.secrets["open_api_key"])

def get_response(prompt, weather_info):
    client = initialize_openai()

    context = [
        {"role": "system", "content": f"The current weather in {weather_info['city']} is:\n"
                                      f"Temperature: {weather_info['temperature']}°C\n"
                                      f"Feels like: {weather_info['feels_like']}°C\n"
                                      f"Minimum: {weather_info['min_temp']}°C\n"
                                      f"Maximum: {weather_info['max_temp']}°C\n"
                                      f"Humidity: {weather_info['humidity']}%"},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=context
    )

    return response.choices[0].message.content

city_input = st.text_input("Enter a city (e.g., Paris, France):", "Paris, France")

if city_input:
    weather_info = fetch_weather(city_input, st.secrets["weather_key"])

    if weather_info:
        st.write("### Current Weather:")
        st.write(weather_info)

        user_query = st.text_area("Ask about the weather:", "What should I wear today?")

        if user_query:
            with st.spinner("Generating response..."):
                chatbot_output = get_response(user_query, weather_info)
                st.write("### Suggested Response:")
                st.write(chatbot_output)
