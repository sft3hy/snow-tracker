import requests
import os
from email_utils import email_sam

import requests

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
    Fetches the one-week forecast using the National Weather Service (NWS) API.
    Returns the daily forecast list with snowfall data if available.
    """
    # Get the NWS gridpoint for the given latitude and longitude
    url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(url)
    response.raise_for_status()
    grid_data = response.json()
    
    # Extract grid ID and forecast URL
    forecast_url = grid_data["properties"]["forecastGridData"]
    
    # Fetch detailed forecast data
    response = requests.get(forecast_url)
    response.raise_for_status()
    forecast_data = response.json()

    # Extract snowfall forecast (in millimeters)
    snowfall_forecast = forecast_data["properties"]["snowfallAmount"]["values"]

    # Convert millimeters to inches (1 mm = 0.0393701 inches)
    daily_snowfall = [(entry["validTime"], entry["value"] * 0.0393701) for entry in snowfall_forecast]

    return daily_snowfall

def get_weekly_snowfall():
    """
    Iterates over each destination, sums up snowfall for the next 7 days,
    and returns a list of dictionaries for destinations with snowfall.
    """
    results = []
    
    for dest in destinations:
        try:
            daily_forecasts = fetch_weekly_forecast(dest["lat"], dest["lon"])
            total_snow_inches = sum(snow for _, snow in daily_forecasts if snow > 0)

            # If there is any snowfall, add the destination to the result
            if total_snow_inches > 0:
                results.append({
                    "location": dest["name"],
                    "snowfall_in_inches": round(total_snow_inches, 1)
                })
        except Exception as e:
            print(f"Error fetching forecast for {dest['name']}: {e}")

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

potential_email = email_choice()
if potential_email is not None:
    email_sam(subject="Snow Forecast", body=potential_email, email_recipient="smaueltown@gmail.com")
else:
    print("no snowfall in any locations in the next 7 days")