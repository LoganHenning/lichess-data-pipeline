import json
import pandas as pd


# Load the raw chess data
games = pd.read_csv("data/games.csv")
total_rows = len(games)


# Validate required columns
required_columns = ["game_id", "white_player", "black_player", "result"]

missing_columns = []

for column in required_columns:
    if column not in games.columns:
        missing_columns.append(column)

print("Missing columns:", missing_columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")


# Count and remove rows with blank required values
blank_value_count = games[required_columns].isna().sum().sum()
print("Blank value count:", blank_value_count)

games = games.dropna(subset=required_columns).copy()
print("Rows after blank filtering:", len(games))


# Count and remove duplicate game IDs
duplicate_count = games.duplicated(subset=["game_id"]).sum()
print("Duplicate game ID count:", duplicate_count)

games = games.drop_duplicates(subset=["game_id"]).copy()
valid_row_count = len(games)

print("Rows after deduplication:", valid_row_count)


# Derive readable outcomes
games["outcome"] = games["result"].map({
    "1-0": "White Win",
    "0-1": "Black Win",
    "1/2-1/2": "Draw"
})


# Merge result scores into the games
result_scores = pd.DataFrame({
    "result": ["1-0", "0-1", "1/2-1/2"],
    "white_score": [1.0, 0.0, 0.5]
})

games = games.merge(result_scores, on="result", how="left")


# Create the White-win output
white_wins = games[games["result"] == "1-0"].copy()


# Create the outcome summary
outcome_summary = (
    games.groupby("outcome")
    .size()
    .reset_index(name="game_count")
)

print(outcome_summary)


# Count games played as each color
white_summary = (
    games.groupby("white_player")
    .size()
    .reset_index(name="games_as_white")
    .rename(columns={"white_player": "player"})
)

black_summary = (
    games.groupby("black_player")
    .size()
    .reset_index(name="games_as_black")
    .rename(columns={"black_player": "player"})
)


# Merge the White and Black summaries
color_summary = white_summary.merge(
    black_summary,
    on="player",
    how="outer"
).fillna(0)

color_summary[["games_as_white", "games_as_black"]] = (
    color_summary[["games_as_white", "games_as_black"]].astype(int)
)

print(color_summary)


# Build the validation report
validation_report = {
    "total_rows": total_rows,
    "valid_rows": valid_row_count,
    "missing_columns": missing_columns,
    "duplicate_count": int(duplicate_count),
    "blank_value_count": int(blank_value_count)
}


# Write output files
games.to_csv("data/clean_games.csv", index=False)
white_wins.to_csv("data/white_wins.csv", index=False)
outcome_summary.to_csv("data/outcome_summary.csv", index=False)
color_summary.to_csv("data/color_summary.csv", index=False)

with open("data/validation_report.json", "w") as file:
    json.dump(validation_report, file, indent=4)