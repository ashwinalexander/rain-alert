import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv


OPEN_WEATHER_MAP_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
LAT_COORD = 47.03
LON_COORD = -10.2

load_dotenv()

# use env variables for these
API_KEY = os.getenv('API_KEY')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')
TWILIO_TO = os.getenv('TWILIO_TO')

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

def send_message(rain_sms):
    message = client.messages \
        .create(
        body=rain_sms,
        from_=TWILIO_FROM,
        to=TWILIO_TO
    )

    print(message.status)


def check_if_prec(weather_json):
    '''check if there is precipitation at the location'''
    print(weather_json)
    for condition in weather_json['weather']:
        if condition['id'] < 700:
            return True


parameters = {
    "lat": LAT_COORD,
    "lon": LON_COORD,
    "appid": API_KEY,
    "units": 'metric',
}

# Get current weather data
response = requests.get(OPEN_WEATHER_MAP_ENDPOINT,params=parameters)
# response.raise_for_status()
weather_data = response.json()


if(check_if_prec(weather_data)):
    send_message("Bring an umbrella")

else:
    send_message("it's probably not raining right now")





# look through response, get main id from weather, and description and then if code < 700 - bring an umbrella



