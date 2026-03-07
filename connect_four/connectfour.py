def stringify_board(board):
    """Returns a nice string representation of a Connect Four board."""

    def checker(board_value):
        if board_value == 0:
            return "⚪"
        elif board_value == 1:
            return "🔴"
        elif board_value == 2:
            return "🟡"
        else:
            raise Exception(f"Invalid connect-four board value: {board_value}")

    mapped = [checker(val) for val in board]
    structured = ["".join(mapped[i : i + 7]) for i in range(0, 42, 7)]
    return "\n".join(structured)


def print_board(board):
    """Prints a nice string representation of a Connect Four board."""
    print(stringify_board(board))


def check_win_conditions(board):
    raise NotImplementedError("fill this in!")


def play_move(board, player, column):
    raise NotImplementedError("fill this in!")
