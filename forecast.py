import json
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime


# ==========================================
# CẤU HÌNH VÙNG
# ==========================================

REGION = {
    "name": "Central Vietnam",

    # Góc dưới bên trái
    "lat_min": 14.5,
    "lon_min": 107.5,

    # Góc trên bên phải
    "lat_max": 17.5,
    "lon_max": 109.5,

    # Khoảng cách giữa các điểm
    "grid_step": 0.5
}


# ==========================================
# TẠO GRID
# ==========================================

def create_grid():
    points = []

    lat = REGION["lat_min"]

    while lat <= REGION["lat_max"]:
        lon = REGION["lon_min"]

        while lon <= REGION["lon_max"]:

            points.append({
                "latitude": round(lat, 2),
                "longitude": round(lon, 2)
            })

            lon += REGION["grid_step"]

        lat += REGION["grid_step"]

    return points


# ==========================================
# LẤY WEATHER FORECAST
# ==========================================

def get_weather(latitude, longitude):

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum,"
            "wind_speed_10m_max"
        ),

        "forecast_days": 7,
        "timezone": "Asia/Bangkok"
    }

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        + urlencode(params)
    )

    with urlopen(url, timeout=30) as response:
        return json.load(response)


# ==========================================
# TÍNH TRUNG BÌNH
# ==========================================

def average(values):

    values = [
        value for value in values
        if value is not None
    ]

    if not values:
        return None

    return round(sum(values) / len(values), 2)


# ==========================================
# MAIN
# ==========================================

def main():

    print("========================================")
    print("AI WEATHER FORECAST SYSTEM")
    print("========================================")

    print("Region:", REGION["name"])

    grid = create_grid()

    print("Grid points:", len(grid))
    print()

    # --------------------------------------
    # Lấy forecast cho từng điểm
    # --------------------------------------

    forecasts = []

    for number, point in enumerate(grid, start=1):

        print(
            f"[{number}/{len(grid)}] "
            f"Downloading "
            f"{point['latitude']}, "
            f"{point['longitude']}"
        )

        try:

            data = get_weather(
                point["latitude"],
                point["longitude"]
            )

            forecasts.append({
                "latitude": point["latitude"],
                "longitude": point["longitude"],
                "daily": data["daily"]
            })

        except Exception as error:

            print("ERROR:", error)


    # --------------------------------------
    # Không có dữ liệu
    # --------------------------------------

    if not forecasts:

        print("No weather data received.")

        return


    # ======================================
    # TỔNG HỢP THEO NGÀY
    # ======================================

    dates = forecasts[0]["daily"]["time"]

    region_forecast = []


    for day_index, date in enumerate(dates):

        temperatures_min = []
        temperatures_max = []
        rain_values = []
        wind_values = []


        for forecast in forecasts:

            daily = forecast["daily"]

            temperatures_min.append(
                daily["temperature_2m_min"][day_index]
            )

            temperatures_max.append(
                daily["temperature_2m_max"][day_index]
            )

            rain_values.append(
                daily["precipitation_sum"][day_index]
            )

            wind_values.append(
                daily["wind_speed_10m_max"][day_index]
            )


        result = {

            "date": date,

            "temperature": {
                "min": min(temperatures_min),
                "max": max(temperatures_max),
                "average_min": average(temperatures_min),
                "average_max": average(temperatures_max)
            },

            "rain": {
                "average_mm": average(rain_values),
                "maximum_mm": max(rain_values)
            },

            "wind": {
                "average_kmh": average(wind_values),
                "maximum_kmh": max(wind_values)
            }
        }


        region_forecast.append(result)


    # ======================================
    # TẠO KẾT QUẢ
    # ======================================

    output = {

        "generated_at": datetime.now().isoformat(),

        "region": REGION,

        "grid_points": len(forecasts),

        "forecast": region_forecast
    }


    # ======================================
    # LƯU JSON
    # ======================================

    with open(
        "forecast.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )


    # ======================================
    # HIỂN THỊ
    # ======================================

    print()
    print("========================================")
    print("REGION FORECAST")
    print("========================================")

    for day in region_forecast:

        print()
        print("Date:", day["date"])

        print(
            "Temperature:",
            day["temperature"]["min"],
            "-",
            day["temperature"]["max"],
            "°C"
        )

        print(
            "Average temperature:",
            day["temperature"]["average_min"],
            "-",
            day["temperature"]["average_max"],
            "°C"
        )

        print(
            "Average rain:",
            day["rain"]["average_mm"],
            "mm"
        )

        print(
            "Maximum rain:",
            day["rain"]["maximum_mm"],
            "mm"
        )

        print(
            "Average wind:",
            day["wind"]["average_kmh"],
            "km/h"
        )

        print(
            "Maximum wind:",
            day["wind"]["maximum_kmh"],
            "km/h"
        )


    print()
    print("========================================")
    print("DONE")
    print("Saved: forecast.json")
    print("========================================")


# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    main()