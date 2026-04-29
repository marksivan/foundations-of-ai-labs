import random

RED_X = "❌"
RED_O = "⭕"
EMPTY_SQUARE = "⬜"


def stringify_board(board):
    def checker(board_value):
        if board_value == 0:
            return EMPTY_SQUARE
        elif board_value == 1:
            return RED_X
        elif board_value == 2:
            return RED_O
        else:
            raise Exception(f"Invalid board value: {board_value}")

    assert len(board) == 9, f"Board is not a list of length 9: {board}"
    rows = []
    rows.append("".join([checker(value) for value in board[:3]]))
    rows.append("".join([checker(value) for value in board[3:6]]))
    rows.append("".join([checker(value) for value in board[6:]]))
    return "\n".join(rows)


def print_board(board):
    print(stringify_board(board))


def check_win_conditions(board):
    winners = set()
    for row in range(3):
        if (
            board[row * 3 + 0] > 0
            and board[row * 3 + 0] == board[row * 3 + 1] == board[row * 3 + 2]
        ):
            winners.add(board[row * 3 + 0])
    for col in range(3):
        if board[col] > 0 and board[col] == board[col + 3] == board[col + 6]:
            winners.add(board[col])
    if board[0] > 0 and board[0] == board[4] == board[8]:  # first diagonal
        winners.add(board[0])
    if board[2] > 0 and board[2] == board[4] == board[6]:  # second diagonal
        winners.add(board[2])
    if len(winners) == 1:
        return list(winners)[0]
    elif len(winners) == 0:
        return 0
    else:
        raise Exception(f"there are two winners: {board}")


def play_game(player1_fn, player2_fn):
    boards = []
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    boards.append([x for x in board])
    current_player = 1
    while check_win_conditions(board) == 0 and 0 in board:
        player_fn = player1_fn if current_player == 1 else player2_fn
        board[player_fn(board)] = current_player
        current_player = 2 if current_player == 1 else 1
        boards.append([x for x in board])
    return boards


def report_game(boards):
    winner = check_win_conditions(boards[-1])
    if winner == 0:
        print("\ntie!")
    else:
        print(f"\nplayer {winner} won!")
    for board in boards:
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
    return (record[1], record[2], record[0])


def compile_playbook():
    def minimax(board, whose_turn, who_am_i, notepad):
        winner = check_win_conditions(board)
        best_moves = []
        if winner == who_am_i:
            minimax_value = 1
        elif winner > 0:
            minimax_value = -1
        elif 0 not in board:  # i.e. the board is full
            minimax_value = 0
        else:
            other_player = 1 if whose_turn == 2 else 2
            minimax_value = float("-inf") if who_am_i == whose_turn else float("inf")
            for move in range(9):
                if board[move] == 0:
                    board[move] = whose_turn
                    next_value = minimax(board, other_player, who_am_i, notepad)
                    if next_value == minimax_value:
                        best_moves.append(move)
                    if who_am_i == whose_turn:  # max layer
                        if next_value > minimax_value:
                            minimax_value = next_value
                            best_moves = [move]
                    else:  # min layer
                        if next_value < minimax_value:
                            minimax_value = next_value
                            best_moves = [move]
                    board[move] = 0  # rewind the board
        notepad[tuple(board)] = best_moves
        return minimax_value

    playbook = dict()
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    minimax(board, whose_turn=1, who_am_i=1, notepad=playbook)
    return playbook


def compile_simple_playbook_for_testing():
    return {
        (1, 2, 0, 0, 0, 1, 2, 0, 0): [4, 8],
        (0, 0, 2, 1, 2, 1, 1, 1, 2): [0],
    }


def random_player_fn(board):
    legal_moves = [i for i, val in enumerate(board) if val == 0]
    if len(legal_moves) == 0:
        return None
    else:
        return random.choice(legal_moves)


def create_optimal_player_fn():
    def player_fn(board):
        best_moves = playbook[tuple(board)]
        if len(best_moves) > 0:
            return random.choice(best_moves)
        else:
            return None

    playbook = compile_playbook()
    return player_fn


optimal_player_fn = create_optimal_player_fn()
