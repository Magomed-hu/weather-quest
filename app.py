from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "502c4314e0a97f147ababe7f7a47d69b"
history = []  # история запросов

def get_background(weather_main):
    return {
        "Clear": "sun",
        "Rain": "rain",
        "Snow": "snow",
        "Clouds": "clouds"
    }.get(weather_main, "default")

def get_message(weather_main):
    return {
        "Clear": "☀️ Отличный день для прогулки!",
        "Rain": "🌧 Не забудь зонт!",
        "Snow": "❄️ Теплее одевайся!",
        "Clouds": "☁️ Пасмурно, но нормально"
    }.get(weather_main, "🌍 Погода есть погода")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.json.get("city", "").strip()
    if not city:
        return jsonify({"error": "Введите название города"})

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric&lang=ru"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "weather" not in data:
        return jsonify({"error": "Город не найден"})

    weather_main = data["weather"][0]["main"]

    result = {
        "city": data["name"],
        "temp": round(data["main"]["temp"]),
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "background": get_background(weather_main),
        "message": get_message(weather_main)
    }

    history.insert(0, result["city"])
    history[:] = history[:5]  # сохраняем только последние 5 городов
    result["history"] = history

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
