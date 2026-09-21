TRUNCATE TABLE CHESS_ANALYTICS.RAW.LICHESS_GAMES_LOAD;

COPY INTO CHESS_ANALYTICS.RAW.LICHESS_GAMES_LOAD
FROM @CHESS_ANALYTICS.RAW.LICHESS_STAGE/clean_games.csv
FILE_FORMAT = (
    FORMAT_NAME = CHESS_ANALYTICS.RAW.LICHESS_CSV_FORMAT
)
FORCE = TRUE;

MERGE INTO CHESS_ANALYTICS.RAW.LICHESS_GAMES AS target
USING CHESS_ANALYTICS.RAW.LICHESS_GAMES_LOAD AS source
    ON target.game_id = source.game_id

WHEN NOT MATCHED THEN
    INSERT (
        game_id,
        game_date,
        white_player,
        black_player,
        white_rating,
        black_rating,
        result,
        eco,
        opening,
        time_control,
        move_count,
        my_color,
        my_rating,
        opponent_rating,
        rating_difference,
        result_for_me,
        outcome,
        white_score
    )
    VALUES (
        source.game_id,
        source.game_date,
        source.white_player,
        source.black_player,
        source.white_rating,
        source.black_rating,
        source.result,
        source.eco,
        source.opening,
        source.time_control,
        source.move_count,
        source.my_color,
        source.my_rating,
        source.opponent_rating,
        source.rating_difference,
        source.result_for_me,
        source.outcome,
        source.white_score
    );

SELECT COUNT(*) AS total_games
FROM CHESS_ANALYTICS.RAW.LICHESS_GAMES;