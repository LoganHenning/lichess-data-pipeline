import json
import pandas as pd


REQUIRED_COLUMNS = [
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

VALID_RESULTS = ["1-0", "0-1", "1/2-1/2"]
VALID_COLORS = ["white", "black"]
VALID_PLAYER_RESULTS = ["win", "loss", "draw"]


def validate_games(games):
    games = games.copy()
    total_rows = len(games)

    # Check that all required columns exist
    missing_columns = []

    for column in REQUIRED_COLUMNS:
        if column not in games.columns:
            missing_columns.append(column)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Track why each row is rejected
    rejection_reasons = pd.Series(
        "",
        index=games.index,
        dtype="object"
    )

    # Find blank required values
    blank_mask = games[REQUIRED_COLUMNS].isna().any(axis=1)

    blank_value_count = (
        games[REQUIRED_COLUMNS]
        .isna()
        .sum()
        .sum()
    )

    rejection_reasons.loc[
        blank_mask
    ] += "blank_required_value;"

    # Only validate categories on nonblank rows
    nonblank_mask = ~blank_mask

    invalid_result_mask = (
        nonblank_mask
        & ~games["result"].isin(VALID_RESULTS)
    )

    invalid_color_mask = (
        nonblank_mask
        & ~games["my_color"].isin(VALID_COLORS)
    )

    invalid_player_result_mask = (
        nonblank_mask
        & ~games["result_for_me"].isin(
            VALID_PLAYER_RESULTS
        )
    )

    invalid_result_count = int(
        invalid_result_mask.sum()
    )

    invalid_color_count = int(
        invalid_color_mask.sum()
    )

    invalid_player_result_count = int(
        invalid_player_result_mask.sum()
    )

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

    candidate_games = games[
        candidate_mask
    ]

    duplicate_mask = candidate_games.duplicated(
        subset=["game_id"],
        keep="first"
    )

    duplicate_indices = candidate_games[
        duplicate_mask
    ].index

    duplicate_count = len(duplicate_indices)

    rejection_reasons.loc[
        duplicate_indices
    ] += "duplicate_game_id;"

    # Split clean and rejected records
    rejected_mask = rejection_reasons != ""

    rejected_games = games[
        rejected_mask
    ].copy()

    rejected_games["rejection_reason"] = (
        rejection_reasons[
            rejected_mask
        ].str.rstrip(";")
    )

    clean_games = games[
        ~rejected_mask
    ].copy()

    valid_row_count = len(clean_games)
    rejected_row_count = len(rejected_games)

    validation_report = {
        "total_rows": total_rows,
        "valid_rows": valid_row_count,
        "rejected_rows": rejected_row_count,
        "missing_columns": missing_columns,
        "duplicate_count": int(duplicate_count),
        "blank_value_count": int(blank_value_count),
        "invalid_result_count": invalid_result_count,
        "invalid_color_count": invalid_color_count,
        "invalid_player_result_count": (
            invalid_player_result_count
        )
    }

    return (
        clean_games,
        rejected_games,
        validation_report
    )


def main():
    # Load structured chess data
    games = pd.read_csv("data/games.csv")

    clean_games, rejected_games, validation_report = (
        validate_games(games)
    )

    print(
        "Missing columns:",
        validation_report["missing_columns"]
    )

    print(
        "Blank value count:",
        validation_report["blank_value_count"]
    )

    print(
        "Invalid result count:",
        validation_report["invalid_result_count"]
    )

    print(
        "Invalid color count:",
        validation_report["invalid_color_count"]
    )

    print(
        "Invalid player result count:",
        validation_report[
            "invalid_player_result_count"
        ]
    )

    print(
        "Duplicate game ID count:",
        validation_report["duplicate_count"]
    )

    print(
        "Rejected rows:",
        validation_report["rejected_rows"]
    )

    print(
        "Rows after validation:",
        validation_report["valid_rows"]
    )

    # Derive readable outcomes
    clean_games["outcome"] = clean_games["result"].map({
        "1-0": "White Win",
        "0-1": "Black Win",
        "1/2-1/2": "Draw"
    })

    # Add numeric score for White
    result_scores = pd.DataFrame({
        "result": [
            "1-0",
            "0-1",
            "1/2-1/2"
        ],
        "white_score": [
            1.0,
            0.0,
            0.5
        ]
    })

    clean_games = clean_games.merge(
        result_scores,
        on="result",
        how="left"
    )

    # Create outcome summary
    outcome_summary = (
        clean_games.groupby("outcome")
        .size()
        .reset_index(name="game_count")
    )

    print(outcome_summary)

    # Count games played as White
    white_summary = (
        clean_games.groupby("white_player")
        .size()
        .reset_index(name="games_as_white")
        .rename(
            columns={"white_player": "player"}
        )
    )

    # Count games played as Black
    black_summary = (
        clean_games.groupby("black_player")
        .size()
        .reset_index(name="games_as_black")
        .rename(
            columns={"black_player": "player"}
        )
    )

    # Merge color summaries
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

    # Write output files
    clean_games.to_csv(
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


if __name__ == "__main__":
    main()