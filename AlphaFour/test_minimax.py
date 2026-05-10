from play import play_tournament

from players import random_player_fn

from minimax import initialize_my_player_fn


# create minimax player
minimax_player = initialize_my_player_fn(depth=3)


# tournament
play_tournament(
    minimax_player,
    random_player_fn,
    300
)