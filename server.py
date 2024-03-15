from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

def get_direction(deg):
    if 0 <= deg <= 12 or 348 <= deg <= 360:
        return 'N'
    elif 13 <= deg <= 33:
        return 'NNE'
    elif 34 <= deg <= 56:
        return 'NE'
    elif 57 <= deg <= 77:
        return 'ENE'
    elif 78 <= deg <= 92:
        return 'E'
    elif 93 <= deg <= 112:
        return 'ESE'
    elif 113 <= deg <= 137:
        return 'SE'
    elif 138 <= deg <= 157:
        return 'SSE'
    elif 158 <= deg <= 182:
        return 'S'
    elif 183 <= deg <= 202:
        return 'SSW'
    elif 203 <= deg <= 227:
        return 'SW'
    elif 228 <= deg <= 247:
        return 'WSW'
    elif 248 <= deg <= 272:
        return 'W'
    elif 273 <= deg <= 292:
        return 'WNW'
    elif 293 <= deg <= 317:
        return 'NW'
    elif 318 <= deg <= 337:
        return 'NNW'
    else:
        return 'Invalid degree'


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    if not city or not city.strip():
        # If city is empty or only contains spaces
        city = "Vaasa"

    weather_data = get_current_weather(city)

    if weather_data.get('cod') != 200:
        # Handle the case where the city is not found
        return render_template('city-not-found.html')

    # Convert wind direction from string to integer before passing to get_direction
    deg = int(weather_data['wind']['deg'])  # Make sure 'deg' exists and is valid
    direction = get_direction(deg)  # Use the converted deg to get direction

    return render_template(
        "weather.html",
        title=weather_data['name'],
        status=weather_data['weather'][0]['description'].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        wind=f"{weather_data['wind']['speed']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        direction=direction
    )
        


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
