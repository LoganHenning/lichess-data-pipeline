games = ["win", "draw", "draw", "loss", "loss", "win"]

wins = 0
losses = 0
draws = 0

for game in games:
    if game == "win":
        wins = wins + 1
    elif game == "loss":
        losses = losses + 1
    elif game == "draw":
        draws = draws + 1

total_games = len(games)

total_points = wins + (draws * 0.5)
score_percentage = (total_points / total_games) * 100

print("Wins:", wins)
print("Losses:", losses)
print("Draws:", draws)
print("Total games:", total_games)
print("Score percentage:", score_percentage)