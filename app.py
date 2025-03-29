from flask import Flask, render_template, jsonify
import requests

# 🔧 KONFIGURACJA STEAM API
STEAM_API_KEY = "52B5AE794910514B707E5525617BD71D"
STEAM_ID = "76561198928855404"
R6_APP_ID = 359550

app = Flask(__name__)

def get_playtime():
    """Pobiera czas gry w Rainbow Six Siege z Steam API."""
    url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={STEAM_API_KEY}&steamid={STEAM_ID}"
    response = requests.get(url).json()

    total_playtime = 0
    two_week_playtime = 0

    # Pobierz całkowity czas gry
    for game in response.get("response", {}).get("games", []):
        if game["appid"] == R6_APP_ID:
            total_playtime = game.get("playtime_forever", 0)  # Minuty
            break

    # Pobierz czas gry z ostatnich 2 tygodni
    url_recent = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={STEAM_API_KEY}&steamid={STEAM_ID}"
    response_recent = requests.get(url_recent).json()

    for game in response_recent.get("response", {}).get("games", []):
        if game["appid"] == R6_APP_ID:
            two_week_playtime = game.get("playtime_2weeks", 0)  # Minuty
            break

    return two_week_playtime, total_playtime

def format_playtime(minutes):
    """Konwertuje minuty na różne jednostki czasu."""
    seconds = minutes * 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7  # Poprawiona dokładna wartość
    months = days / 30  # Przybliżenie do 30-dniowego miesiąca

    return {
        "minutes": minutes,
        "hours": round(hours, 2),
        "days": round(days, 2),
        "weeks": round(weeks, 2),
        "months": round(months, 2),
        "seconds": seconds,
    }

@app.route("/")
def index():
    """Generuje stronę HTML ze statystykami."""
    two_week_playtime, total_playtime = get_playtime()
    
    data_two_weeks = format_playtime(two_week_playtime)
    data_total = format_playtime(total_playtime)

    return render_template("stats.html", two_weeks=data_two_weeks, total=data_total)

@app.route("/refresh")
def refresh():
    """Odświeża dane."""
    return jsonify({"message": "Dane zostały odświeżone!"})

if __name__ == "__main__":
    app.run(debug=True)
