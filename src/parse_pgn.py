import csv
import chess.pgn


with open("data/raw_game.pgn", "r", encoding="utf-8") as file:
    game = chess.pgn.read_game(file)


headers = game.headers


# Count individual moves, then convert to full chess moves
ply_count = 0

for move in game.mainline_moves():
    ply_count += 1

move_count = (ply_count + 1) // 2


# Create one structured row from the PGN
row = {
    "game_id": headers.get("GameId"),
    "date": headers.get("Date"),
    "white_player": headers.get("White"),
    "black_player": headers.get("Black"),
    "white_rating": headers.get("WhiteElo"),
    "black_rating": headers.get("BlackElo"),
    "result": headers.get("Result"),
    "eco": headers.get("ECO"),
    "opening": headers.get("Opening"),
    "time_control": headers.get("TimeControl"),
    "move_count": move_count
}


# Write the structured game to CSV
with open("data/games.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=row.keys())

    writer.writeheader()
    writer.writerow(row)


print("Parsed game saved to data/games.csv")
print(row)