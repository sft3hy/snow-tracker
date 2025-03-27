import requests
import os
from email_utils import email_sam

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# List of destinations with approximate coordinates (latitude, longitude)
destinations = [
    {"name": "Mountain High", "lat": 34.3009, "lon": -117.5495},
    {"name": "Mt. Baldy", "lat": 34.2366, "lon": -117.6513},
    {"name": "Snow Summit", "lat": 34.2601, "lon": -116.9114},
    {"name": "Bear Mountain", "lat": 34.2453, "lon": -116.9570},
    {"name": "Snow Valley Mountain Resort", "lat": 34.1087, "lon": -117.2747},
]

def fetch_weekly_forecast(lat, lon):
    """
    Fetches the one week forecast using the OpenWeatherMap One Call API.
    Returns the daily forecast list.
    """
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "imperial",
        "appid": API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("daily", [])

def get_weekly_snowfall():
    """
    Iterates over each destination, sums up snowfall for the next 7 days,
    and returns a list of dictionaries for destinations with snowfall.
    """
    results = []
    
    for dest in destinations:
        daily_forecasts = fetch_weekly_forecast(dest["lat"], dest["lon"])
        total_snow_inches = 0.0
        
        # Iterate over up to 7 days of forecast
        for day in daily_forecasts[:7]:
            # The API may include a "snow" field in the daily data if snowfall is forecast
            # The unit should be inches when units=imperial, but if not, you may need to convert.
            snow = day.get("snow", 0)
            total_snow_inches += snow
        
        # If there is any snowfall, add the destination to the result
        if total_snow_inches > 0:
            # Round snowfall to one decimal place
            results.append({
                "location": dest["name"],
                "snowfall_in_inches": round(total_snow_inches, 1)
            })
    
    return results

def email_choice():
    snowfall_destinations = get_weekly_snowfall()
    if snowfall_destinations:
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                h2 { color: #2c3e50; }
                table { width: 100%%; border-collapse: collapse; margin-top: 10px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #3498db; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h2>Upcoming Snowfall Forecast</h2>
            <table>
                <tr>
                    <th>Location</th>
                    <th>Snowfall (inches)</th>
                </tr>
        """
        for item in snowfall_destinations:
            html_content += f"""
                <tr>
                    <td>{item['location']}</td>
                    <td>{item['snowfall_in_inches']} inches</td>
                </tr>
            """
        html_content += """
            </table>
        </body>
        </html>
        """
        return html_content
    else:
        return None

fetch_weekly_forecast(37.647190, -118.967453)

# potential_email = email_choice()
# if potential_email is not None:
#     email_sam(subject="Snow Forecast", body=potential_email, email_recipient="smaueltown@gmail.com")