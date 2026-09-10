# Store a sample list of chess game results
games = ["win", "draw", "draw", "loss", "loss", "win"]


# Create counters for each possible result
wins = 0
losses = 0
draws = 0


# Loop through each game result in the list
for game in games:
    if game == "win":
        wins = wins + 1
    elif game == "loss":
        losses = losses + 1
    elif game == "draw":
        draws = draws + 1


# Count the total number of games in the list
total_games = len(games)


# Calculate total chess points
# A win is worth 1 point and a draw is worth 0.5 points
total_points = wins + (draws * 0.5)


# Calculate the percentage of possible points earned
score_percentage = (total_points / total_games) * 100


# Display the results
print("Wins:", wins)
print("Losses:", losses)
print("Draws:", draws)
print("Total games:", total_games)
print("Score percentage:", score_percentage)