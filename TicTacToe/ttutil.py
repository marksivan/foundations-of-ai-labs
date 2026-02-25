def stringify_board(board):
    def checker(board_value):
        if board_value == 0:
            return "⬜"
        elif board_value == 1:
            return "❌"
        elif board_value == 2:
            return "⭕"
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
