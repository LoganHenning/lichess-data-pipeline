select
    game_id,
    to_date(game_date, 'YYYY.MM.DD') as game_date,
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

from {{ source('raw', 'lichess_games') }}