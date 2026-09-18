import json
import pandas as pd


# Load the raw chess data
games = pd.read_csv("data/games.csv")
total_rows = len(games)


# Validate required columns
required_columns = [
    "game_id",
    "date",
    "white_player",
    "black_player",
    "white_rating",
    "black_rating",
    "result",
    "my_color",
    "my_rating",
    "opponent_rating",
    "result_for_me"
]

missing_columns = []

for column in required_columns:
    if column not in games.columns:
        missing_columns.append(column)

print("Missing columns:", missing_columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")


# Track rejection reasons for each row
rejection_reasons = pd.Series(
    "",
    index=games.index,
    dtype="object"
)


# Find rows with blank required values
blank_mask = games[required_columns].isna().any(axis=1)

blank_value_count = (
    games[required_columns]
    .isna()
    .sum()
    .sum()
)

print("Blank value count:", blank_value_count)

rejection_reasons.loc[blank_mask] += "blank_required_value;"


# Validate categorical values
valid_results = ["1-0", "0-1", "1/2-1/2"]
valid_colors = ["white", "black"]
valid_player_results = ["win", "loss", "draw"]


# Only perform these checks on rows that are not already blank
nonblank_mask = ~blank_mask

invalid_result_mask = (
    nonblank_mask
    & ~games["result"].isin(valid_results)
)

invalid_color_mask = (
    nonblank_mask
    & ~games["my_color"].isin(valid_colors)
)

invalid_player_result_mask = (
    nonblank_mask
    & ~games["result_for_me"].isin(valid_player_results)
)


invalid_result_count = invalid_result_mask.sum()
invalid_color_count = invalid_color_mask.sum()
invalid_player_result_count = invalid_player_result_mask.sum()

print("Invalid result count:", invalid_result_count)
print("Invalid color count:", invalid_color_count)
print("Invalid player result count:", invalid_player_result_count)


rejection_reasons.loc[
    invalid_result_mask
] += "invalid_result;"

rejection_reasons.loc[
    invalid_color_mask
] += "invalid_color;"

rejection_reasons.loc[
    invalid_player_result_mask
] += "invalid_player_result;"


# Find duplicate game IDs among otherwise valid rows
candidate_mask = rejection_reasons == ""

candidate_games = games[candidate_mask]

duplicate_mask = candidate_games.duplicated(
    subset=["game_id"],
    keep="first"
)

duplicate_indices = candidate_games[
    duplicate_mask
].index

duplicate_count = len(duplicate_indices)

print("Duplicate game ID count:", duplicate_count)

rejection_reasons.loc[
    duplicate_indices
] += "duplicate_game_id;"


# Separate clean and rejected records
rejected_mask = rejection_reasons != ""

rejected_games = games[rejected_mask].copy()

rejected_games["rejection_reason"] = (
    rejection_reasons[rejected_mask]
    .str.rstrip(";")
)

games = games[~rejected_mask].copy()

valid_row_count = len(games)
rejected_row_count = len(rejected_games)

print("Rejected rows:", rejected_row_count)
print("Rows after validation:", valid_row_count)


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

games = games.merge(
    result_scores,
    on="result",
    how="left"
)


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

color_summary[
    ["games_as_white", "games_as_black"]
] = (
    color_summary[
        ["games_as_white", "games_as_black"]
    ].astype(int)
)

print(color_summary)


# Build the validation report
validation_report = {
    "total_rows": total_rows,
    "valid_rows": valid_row_count,
    "rejected_rows": rejected_row_count,
    "missing_columns": missing_columns,
    "duplicate_count": int(duplicate_count),
    "blank_value_count": int(blank_value_count),
    "invalid_result_count": int(invalid_result_count),
    "invalid_color_count": int(invalid_color_count),
    "invalid_player_result_count": int(
        invalid_player_result_count
    )
}


# Write output files
games.to_csv(
    "data/clean_games.csv",
    index=False
)

rejected_games.to_csv(
    "data/rejected_games.csv",
    index=False
)

outcome_summary.to_csv(
    "data/outcome_summary.csv",
    index=False
)

color_summary.to_csv(
    "data/color_summary.csv",
    index=False
)

with open(
    "data/validation_report.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        validation_report,
        file,
        indent=4
    )