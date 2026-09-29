select
    my_color,
    count(*) as total_games,
    sum(case when result_for_me = 'win' then 1 else 0 end) as wins,
    sum(case when result_for_me = 'loss' then 1 else 0 end) as losses,
    sum(case when result_for_me = 'draw' then 1 else 0 end) as draws,

    round(
        100.0 * sum(case when result_for_me = 'win' then 1 else 0 end) / count(*),
        1
    ) as win_percentage,

    round(avg(my_rating), 1) as average_rating,
    round(avg(opponent_rating), 1) as average_opponent_rating

from {{ ref('stg_lichess_games') }}

group by my_color