import requests
import time


headers = {
    "Accept": "application/x-chess-pgn",
    "User-Agent": (
        "lichess-data-pipeline/1.0 "
        "(https://github.com/LoganHenning/lichess-data-pipeline)"
    )
}


username = "MrBlunderhill"
max_games = 10

params = {
    "max": max_games,
    "moves": "true",
    "opening": "true"
}


max_attempts = 3
attempt = 1


while attempt <= max_attempts:

    try:
        response = requests.get(
            f"https://lichess.org/api/games/user/{username}",
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

    except requests.exceptions.HTTPError as error:

        if (
            response.status_code == 429
            or 500 <= response.status_code < 600
        ) and attempt < max_attempts:

            if response.status_code == 429:
                wait_seconds = 60
            else:
                wait_seconds = 5

            print(
                f"Temporary HTTP error {response.status_code}. "
                f"Waiting {wait_seconds} seconds before retrying..."
            )

            time.sleep(wait_seconds)
            attempt += 1

        else:
            print("Request failed:", error)
            break

    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError
    ) as error:

        if attempt < max_attempts:
            print(
                "Temporary connection problem. "
                "Waiting 5 seconds before retrying..."
            )

            time.sleep(5)
            attempt += 1

        else:
            print("Request failed after maximum attempts:", error)
            break

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)
        break

    else:
        with open("data/raw_games.pgn", "w", encoding="utf-8") as file:
            file.write(response.text)

        print(
            f"Saved up to {max_games} games "
            "to data/raw_games.pgn"
        )
        break