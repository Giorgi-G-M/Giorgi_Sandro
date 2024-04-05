import requests
import datetime
import sys
import tabulate

def weather_main():
    while True:
        user = input("Where are you? ")

        if user:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={user}&APPID=02734d5341b5aa5ecb0198a4bc9a722e"
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                weather_info = {
                    "Location": f"{user}",
                    "Sunrise": sun_rise(data),
                    "Humidity": get_info(data)[0],
                    "Weather": get_info(data)[1],
                    "Wind Direction": degrees_to_direction(data),
                    "Weather Condition": weather_checker(data),
                    "Temperature (Fahrenheit)": fahrenheit_converter(data),
                    "Temperature (Celsius)": celsius_converter(data),
                    "Sunset": sun_set(data)
                }

                table_data = [(key, value) for key, value in weather_info.items()]

                print(tabulate.tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid"))
                break
            else:
                print("Invalid location. Please try again.")
        else:
            print("Please provide both city and country.")


#This function gives infromation about humidity and weather's description for example: "cloudy, rain" etc.
def get_info(data):
    humanidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]

    return humanidity, weather

#This function gives information about sunrise
def sun_rise(data):
        sun_rise = data["sys"]["sunrise"]
        date_convertor = datetime.datetime.fromtimestamp(sun_rise)
        return date_convertor

#This function returns information about sunset
def sun_set(data):
    sun_set = data["sys"]["sunset"]
    date_convertor = datetime.datetime.fromtimestamp(sun_set)
    return date_convertor

#This function is checking wind's deg and direction
def degrees_to_direction(data):
    directions = ["North", "North-northeast", "Northeast", "East-northeast", "East",
                  "East-southeast", "Southeast", "South-southeast", "South",
                  "South-southwest", "Southwest", "West-southwest", "West",
                  "West-northwest", "Northwest", "North-northwest"]

    if "wind" in data and "deg" in data["wind"]:
        wind_degrees = data["wind"]["deg"]

        if 350 <= wind_degrees <= 360 or 0 <= wind_degrees <= 10:
            return directions[0]

        index = 360.0 / len(directions)
        for i in range(len(directions)):
            if i * index <= wind_degrees < (i+1) * index:
                return directions[i+1]

#this funciton is checking weather conditions
def weather_checker(data):
    weather = ["clear sky", "few clouds", "scattered clouds", "broken clouds","shower rain",
               "rain", "thunderstorm", "snow", "mist", "light rain", "thunderstorm with heavy rain"]

    current_weather = data["weather"][0]["description"]
    if "rain" in current_weather or "light rain" in current_weather:
        return ("take a ambrella")
    elif "snow" in current_weather:
        return ("you need a ambrella")
    elif "thunderstorm" in current_weather:
        return ("You'll need a ambrela")
    elif "scattered clouds" in current_weather or "broken clouds" in current_weather:
        return ("You might need a ambrela")
    elif "mist" in current_weather:
        return ("You might need a light")
    else:
        return ("it's a nice day out!")

#from kelvin to fahrenheit convertor
def fahrenheit_converter(data):

    current_temp = data["main"]["temp"]
    converter = float(9/5 * (current_temp - 273.15) + 32)
    return round(converter)

#from kelvin to celsius convertor
def celsius_converter(data):
    current_temp = data["main"]["temp"]
    converter = float(current_temp - 273.15)
    return round(converter)


if __name__=="__main__":
    weather_main()
