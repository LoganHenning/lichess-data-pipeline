import requests
import time


# Tell Lichess that we want PGN data and identify our application
headers = {
    "Accept": "application/x-chess-pgn",
    "User-Agent": "lichess-data-pipeline/1.0 (https://github.com/LoganHenning/lichess-data-pipeline)"
}


# Lichess game to download
game_id = "9xBktSBL"


# Allow the request to be attempted up to 3 times
max_attempts = 3
attempt = 1


while attempt <= max_attempts:

    try:
        # Request the game from the Lichess API
        response = requests.get(
            f"https://lichess.org/game/export/{game_id}",
            headers=headers,
            timeout=10
        )

        # Raise an error for unsuccessful HTTP status codes
        response.raise_for_status()

    except requests.exceptions.HTTPError as error:

        # Retry temporary HTTP problems:
        # 429 = rate limited
        # 500-599 = Lichess/server-side error
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
                attempt = attempt + 1

        else:
            print("Request failed:", error)
            break

    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError
    ) as error:

        # Retry temporary connection problems
        if attempt < max_attempts:
            print(
                "Temporary connection problem. "
                "Waiting 5 seconds before retrying..."
            )

            time.sleep(5)
            attempt = attempt + 1

        else:
            print("Request failed after maximum attempts:", error)
            break



    except requests.exceptions.RequestException as error:

        # Catch any other requests-related problem
        print("Request failed:", error)
        break


    else:
        # Only save the file if the API request succeeded
        with open("data/raw_game.pgn", "w", encoding="utf-8") as file:
            file.write(response.text)

        print("Saved game to data/raw_game.pgn")
        break

