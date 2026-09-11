import json
from urllib.request import urlopen
from datetime import datetime


# =========================
# VÙNG DỰ BÁO
# =========================

REGION = {
    "name": "Central Vietnam",
    "latitude": 16.05,
    "longitude": 108.20
}


# =========================
# LẤY DỰ BÁO
# =========================

url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=" + str(REGION["latitude"]) +
    "&longitude=" + str(REGION["longitude"]) +
    "&daily=temperature_2m_max,temperature_2m_min,"
    "precipitation_sum,wind_speed_10m_max"
    "&timezone=Asia%2FBangkok"
)

print("Downloading weather data...")

with urlopen(url) as response:
    data = json.load(response)


# =========================
# HIỂN THỊ
# =========================

dates = data["daily"]["time"]
max_temp = data["daily"]["temperature_2m_max"]
min_temp = data["daily"]["temperature_2m_min"]
rain = data["daily"]["precipitation_sum"]
wind = data["daily"]["wind_speed_10m_max"]

print()
print("================================")
print("WEATHER FORECAST")
print("================================")
print("Region:", REGION["name"])
print()

for i in range(len(dates)):
    print("Date:", dates[i])
    print("Temperature:", min_temp[i], "-", max_temp[i], "°C")
    print("Rain:", rain[i], "mm")
    print("Max wind:", wind[i], "km/h")
    print("--------------------------------")
