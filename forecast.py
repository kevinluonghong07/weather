from datetime import datetime, timezone

print("================================")
print("AI WEATHER FORECAST")
print("================================")

now = datetime.now(timezone.utc)

print("Forecast run time:", now.strftime("%Y-%m-%d %H:%M UTC"))
print("Weather forecast system started!")
print("================================")
