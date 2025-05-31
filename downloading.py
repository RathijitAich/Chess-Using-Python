import requests
import json

# List of archive URLs you have
archive_urls = [
    "https://api.chess.com/pub/player/monkey-on-mars/games/2024/10",
    "https://api.chess.com/pub/player/monkey-on-mars/games/2024/11",
    "https://api.chess.com/pub/player/monkey-on-mars/games/2024/12",
    "https://api.chess.com/pub/player/monkey-on-mars/games/2025/01",
    "https://api.chess.com/pub/player/monkey-on-mars/games/2025/02",
    "https://api.chess.com/pub/player/monkey-on-mars/games/2025/03",
    "https://api.chess.com/pub/player/monkey-on-mars/games/2025/04",
    "https://api.chess.com/pub/player/monkey-on-mars/games/2025/05"
]

all_games = []

for url in archive_urls:
    print(f"Fetching: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        games = data.get("games", [])
        all_games.extend(games)
    else:
        print(f"Failed to fetch {url} (status {response.status_code})")
        print(response.text)

# Save as JSON (optional)
with open("monkey_games.json", "w") as f:
    json.dump(all_games, f, indent=2)

print(f"Downloaded {len(all_games)} games.")


with open("monkey_games.pgn", "w", encoding="utf-8") as f:
    for game in all_games:
        if "pgn" in game:
            f.write(game["pgn"] + "\n\n")
print("Games saved to monkey_games.pgn.")