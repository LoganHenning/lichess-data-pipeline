import pandas as pd

from src.pandas_etl import validate_games


def make_valid_game(game_id="game1"):
    return {
        "game_id": game_id,
        "date": "2026.09.18",
        "white_player": "MrBlunderhill",
        "black_player": "Opponent",
        "white_rating": 2100,
        "black_rating": 2050,
        "result": "1-0",
        "my_color": "white",
        "my_rating": 2100,
        "opponent_rating": 2050,
        "result_for_me": "win"
    }


def test_valid_game_is_accepted():
    games = pd.DataFrame([
        make_valid_game()
    ])

    clean, rejected, report = validate_games(games)

    assert len(clean) == 1
    assert len(rejected) == 0
    assert report["valid_rows"] == 1
    assert report["rejected_rows"] == 0


def test_blank_required_value_is_rejected():
    game = make_valid_game()
    game["white_player"] = None

    games = pd.DataFrame([game])

    clean, rejected, report = validate_games(games)

    assert len(clean) == 0
    assert len(rejected) == 1
    assert report["blank_value_count"] == 1
    assert (
        rejected.iloc[0]["rejection_reason"]
        == "blank_required_value"
    )


def test_invalid_result_is_rejected():
    game = make_valid_game()
    game["result"] = "BAD"

    games = pd.DataFrame([game])

    clean, rejected, report = validate_games(games)

    assert len(clean) == 0
    assert len(rejected) == 1
    assert report["invalid_result_count"] == 1
    assert (
        rejected.iloc[0]["rejection_reason"]
        == "invalid_result"
    )


def test_invalid_color_is_rejected():
    game = make_valid_game()
    game["my_color"] = "green"

    games = pd.DataFrame([game])

    clean, rejected, report = validate_games(games)

    assert len(clean) == 0
    assert len(rejected) == 1
    assert report["invalid_color_count"] == 1
    assert (
        rejected.iloc[0]["rejection_reason"]
        == "invalid_color"
    )


def test_duplicate_game_id_is_rejected():
    games = pd.DataFrame([
        make_valid_game("game1"),
        make_valid_game("game1")
    ])

    clean, rejected, report = validate_games(games)

    assert len(clean) == 1
    assert len(rejected) == 1
    assert report["duplicate_count"] == 1
    assert (
        rejected.iloc[0]["rejection_reason"]
        == "duplicate_game_id"
    )


def test_invalid_player_result_is_rejected():
    game = make_valid_game()
    game["result_for_me"] = "BAD"

    games = pd.DataFrame([game])

    clean, rejected, report = validate_games(games)

    assert len(clean) == 0
    assert len(rejected) == 1
    assert report["invalid_player_result_count"] == 1
    assert (
        rejected.iloc[0]["rejection_reason"]
        == "invalid_player_result"
    )