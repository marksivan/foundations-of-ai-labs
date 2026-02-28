from ttutil import print_board
from players import random_player_fn
import copy



def check_columns(board, x):
    if board[0] == x and board[3] == x and board[6] == x:
        return True
    if board[1] == x and board[4] == x and board[7] == x:
        return True
    if board[2] == x and board[5] == x and board[8] == x:
        return True
    return False

def check_rows(board, x):
    if board[0] == x and board[1] == x and board[2] == x:
        return True
    if board[3] == x and board[4] == x and board[4] == x:
        return True
    if board[6] == x and board[7] == x and board[8] == x:
        return True
    return False

def check_diagonal(board, x):
    if board[0] == x and board[4] == x and board[8] == x:
        return True
    if board[2] == x and board[4] == x and board[6] == x:
        return True
    return False

   
    


def check_win_conditions(board):
    players = (1,2)
    winners = []

    for player in players:
        if check_columns(board, player) or check_rows(board, player) or check_diagonal(board, player):
            winners.append(player)
    
    if len(winners) == 1:
        return winners[0]
    
    if len(winners) == 2:
       raise Exception(f"there are two winners: {board}")
        
    return 0
   

def play_game(player1_fn, player2_fn):

    board = [0] * 9

    result = [board]


    player1_turn = False

    while check_win_conditions(result[-1]) == 0:
        
        player1_turn = not player1_turn
        position = random_player_fn(result[-1])
        new_board = result[-1].copy()
        if position is not None:
            if player1_turn:
                new_board[position] = 1
            else:
                new_board[position] = 2

            result.append(new_board)

    return result





    


def report_game(game):
    winner = check_win_conditions(game[-1])
    if winner == 0:
        print("\ntie!")
    else:
        print(f"\nplayer {winner} won!")
    for board in game:
        print_board(board)
        print("")
    return winner


def play_tournament(num_rounds, player1_fn, player2_fn):
    record = [0, 0, 0]  # ties, player1 wins, player2 wins
    for _ in range(num_rounds):
        game = play_game(player1_fn, player2_fn)
        winner = check_win_conditions(game[-1])
        record[winner] += 1
        game = play_game(player2_fn, player1_fn)
        winner = check_win_conditions(game[-1])
        if winner == 1:
            winner = 2
        elif winner == 2:
            winner = 1
        record[winner] += 1
    print(f"P1-P2-T: {record[1]}-{record[2]}-{record[0]}")


def compile_playbook():
    raise NotImplementedError("Fill this in!")


## Tests
# print(check_win_conditions([1, 2, 2, 0, 1, 1, 2, 0, 0]))
# print(check_win_conditions([1, 2, 2, 0, 1, 1, 2, 0, 1]))
# print(check_win_conditions([2, 2, 2, 0, 1, 1, 1, 0, 0]))
# print(check_win_conditions([2, 2, 2, 1, 1, 1, 0, 0, 0]))


# print(random_player_fn([0, 0, 0, 0, 0, 0, 0, 0, 0]))
# print(random_player_fn([0, 0, 0, 1, 2, 0, 0, 0, 0]))
# print(random_player_fn([2, 1, 2, 1, 2, 0, 1, 0, 0]))



# results = play_game()

# for item in results:
#     print(item)
game = play_game(random_player_fn, random_player_fn)

print(report_game(game))