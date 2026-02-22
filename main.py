import requests
import os
from twilio.rest import Client
from twilio.http.http_client import twilioHttpClient

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

# digging into the API of the open weather map service.
OWM_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")

# setting up for using the Twilio API to send SMS-es
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

# weather parameters, lat and lon for a rainy place (Bergen)
weather_parameters = {
    "lat" : 63.44,
    "lon" : 10.42,
    "cnt" : 4,
    "units" : "metric",
    "lang" : "no",
    "appid" : api_key,
}

# Gets the data out via the API and put them into weather_data
response = requests.get(url=OWM_endpoint, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()

# A try at getting the rain warning out

# List of weather IDs
will_rain = False
for hour_data in weather_data['list']:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="Bring an umbrella.",
        from_="+18137059796",
        to="+4798216825",
    )
print(will_rain)
