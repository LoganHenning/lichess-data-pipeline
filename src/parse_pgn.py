import csv
import chess.pgn


rows = []
username = "MrBlunderhill"


with open("data/raw_games.pgn", "r", encoding="utf-8") as file:

    while True:
        game = chess.pgn.read_game(file)

        if game is None:
            break

        headers = game.headers

        white_player = headers.get("White")
        black_player = headers.get("Black")
        white_rating = int(headers.get("WhiteElo"))
        black_rating = int(headers.get("BlackElo"))
        result = headers.get("Result")

        # Determine which color I played and calculate
        # statistics relative to my account
        if username.lower() == white_player.lower():
            my_color = "white"
            my_rating = white_rating
            opponent_rating = black_rating

            if result == "1-0":
                result_for_me = "win"
            elif result == "0-1":
                result_for_me = "loss"
            else:
                result_for_me = "draw"

        elif username.lower() == black_player.lower():
            my_color = "black"
            my_rating = black_rating
            opponent_rating = white_rating

            if result == "0-1":
                result_for_me = "win"
            elif result == "1-0":
                result_for_me = "loss"
            else:
                result_for_me = "draw"

        else:
            raise ValueError("Username not found in game.")

        rating_difference = my_rating - opponent_rating

        # Count individual turns, then convert to full chess moves
        ply_count = 0

        for move in game.mainline_moves():
            ply_count += 1

        move_count = (ply_count + 1) // 2

        # Create one structured row for the game
        row = {
            "game_id": headers.get("GameId"),
            "date": headers.get("Date"),
            "white_player": white_player,
            "black_player": black_player,
            "white_rating": white_rating,
            "black_rating": black_rating,
            "result": result,
            "eco": headers.get("ECO"),
            "opening": headers.get("Opening"),
            "time_control": headers.get("TimeControl"),
            "move_count": move_count,
            "my_color": my_color,
            "my_rating": my_rating,
            "opponent_rating": opponent_rating,
            "rating_difference": rating_difference,
            "result_for_me": result_for_me
        }

        rows.append(row)


if rows:
    with open("data/games.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)


print(f"Parsed {len(rows)} games to data/games.csv")