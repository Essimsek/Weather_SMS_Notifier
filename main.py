import json
import requests
import datetime
from twilio.rest import Client

# Twilio account
TWILIO_ACCOUNT_SID = "Your Twilio Account SID"
TWILIO_AUTH_TOKEN = "Your Twilio Auth Token"

SECONDS_PER_HOUR = 3600
TIME_LIMIT_HOURS = 12  # Limit is 4 days (api can afford just 4 days)
MY_LAT = 41.138981 # Change these with your actual lat and long
MY_LONG = -20.086720
API_KEY = "Your API Key"

params = {
	"lat": MY_LAT,
	"lon": MY_LONG,
	"appid": API_KEY,
	"exclude": "current,minutely,daily"
}

def send_sms(message):
	client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

	# Replace the 'from_' number with your Twilio phone number
	# Replace the 'to' number with your own phone number
	client.messages.create(from_="Your Twilio number",
						   to="Your Number",
						   body=message)


try:
	request = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
	request.raise_for_status()
	data = request.json()

	rainy_days = []
	current_time = datetime.datetime.now().timestamp()
	time_limit = current_time + (TIME_LIMIT_HOURS * SECONDS_PER_HOUR)  # 12 hours from current_time in seconds
	rainy_in_12_hours = False

	for forecast in data["list"]:
		forecast_time = forecast["dt"]
		if forecast_time <= time_limit:
			weather_condition_id = forecast["weather"][0]["id"]
			if 500 <= weather_condition_id <= 531:  # Check if the weather is rainy
				rainy_days.append(forecast)
				rainy_in_12_hours = True

	if rainy_in_12_hours:
		print("Rain is expected in the next 12 hours. Send SMS.")

		send_sms("Tomorrow weather is rainy so do not forget to take your ☂️ with you!!!")
		# Json data
		with open("weather_data.json", "w") as json_file:
			json.dump(rainy_days, json_file, indent=4)
		print("JSON data has been written to 'weather_data.json'")

	else:
		print("No rain is expected in the next 12 hours. Do not send SMS.")

except requests.RequestException as err:
	print(f"Error: {err}")
