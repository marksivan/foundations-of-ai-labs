from ttutil import print_board
from players import random_player_fn, create_optimal_player_fn



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
    if board[3] == x and board[4] == x and board[5] == x:
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

    while check_win_conditions(result[-1]) == 0 and 0 in result[-1]:
        
        player1_turn = not player1_turn
        new_board = result[-1].copy()

        if player1_turn:
            position = player1_fn(new_board)
        else:
            position = player2_fn(new_board)


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


def get_player_turn(board):
    if board.count(1) == board.count(2):
        return 1
    return 2

def compile_playbook():
    result = dict()
    memo = dict()

    def minimax(board):
        board_tuple = tuple(board)

        if board_tuple in memo:
            return memo[board_tuple]
        winner = check_win_conditions(board)

        #Terminal states
        if winner == 1:
            return 1
        if winner ==2:
            return -1
        # if 0 not in board:
        #     return 0

        if winner == 0:
            return 0
        
        player = get_player_turn(board)

        move_values = {}

        best_value = None

        for i in range(9):
            if board[i] == 0:
                board[i] = player
                value = minimax(board)
                board[i] = 0 #undo move

                move_values[i] = value

                if best_value is None:
                    best_value = value
                else:
                    if player == 1:
                        best_value = max(best_value, value)
                    else:
                        best_value = min(best_value, value)
        
        best_moves = [move for move,val in move_values.items() if val == best_value]
 
        result[board_tuple] = best_moves
        memo[board_tuple] = best_value

        return best_value

    minimax([0] * 9)

    return result









## Tests
# print(check_win_conditions([1, 2, 2, 0, 1, 1, 2, 0, 0]))
# print(check_win_conditions([1, 2, 2, 0, 1, 1, 2, 0, 1]))
# print(check_win_conditions([2, 2, 2, 0, 1, 1, 1, 0, 0]))
# print(check_win_conditions([2, 2, 2, 1, 1, 1, 0, 0, 0]))
# print(check_win_conditions([2, 2, 1, 0, 1, 0, 1, 0, 0]))



# print(random_player_fn([0, 0, 0, 0, 0, 0, 0, 0, 0]))
# print(random_player_fn([0, 0, 0, 1, 2, 0, 0, 0, 0]))
# print(random_player_fn([2, 1, 2, 1, 2, 0, 1, 0, 0]))



# results = play_game()

# for item in results:
#     print(item)
# game = play_game(random_player_fn, random_player_fn)

# print(report_game(game))

# playbook = compile_playbook()
# print(playbook[(1, 1, 0, 0, 2, 0, 0, 0, 0)])
# print(playbook[(1, 1, 0, 2, 1, 0, 2, 2, 0)])
# print(playbook[(0, 0, 0, 0, 1, 0, 0, 0, 0)])