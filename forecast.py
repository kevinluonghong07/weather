import json
from urllib.request import urlopen

LATITUDE = 16.05
LONGITUDE = 108.20

url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    f"&daily=temperature_2m_max,temperature_2m_min,"
    f"precipitation_sum,wind_speed_10m_max"
    f"&timezone=Asia%2FBangkok"
)

print("Downloading weather data...")

with urlopen(url) as response:
    data = json.load(response)

dates = data["daily"]["time"]
max_temp = data["daily"]["temperature_2m_max"]
min_temp = data["daily"]["temperature_2m_min"]
rain = data["daily"]["precipitation_sum"]
wind = data["daily"]["wind_speed_10m_max"]

print("================================")
print("WEATHER FORECAST")
print("================================")

for i in range(len(dates)):
    print(f"Date: {dates[i]}")
    print(f"Temperature: {min_temp[i]} - {max_temp[i]} °C")
    print(f"Rain: {rain[i]} mm")
    print(f"Max wind: {wind[i]} km/h")
    print("--------------------------------")
