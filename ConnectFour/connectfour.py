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



def check_row(board, element,start, end):

    streak = 0
    for i in range(start,end):
        if board[i] == element:
            streak += 1
        else:
            streak = 0
        if streak == 4:
            return True
    return False

def check_all_rows(board, element):

    row6 = check_row(board, element,35,42)
    row5 = check_row(board, element,28,35)
    row4 = check_row(board, element,21,28)
    row3 = check_row(board, element,14,21)
    row2 = check_row(board, element,7,14)
    row1 = check_row(board, element,0,7)

    return row6 or row5 or row4 or row3 or row2 or row1


def check_column(board, element, start,end):
    streak = 0
    for i in range(start, end+1, 7):
        if board[i] == element:
            streak += 1
        else:
            streak = 0
        if streak == 4:
            return True
    return False

def check_all_columns(board,element):

    col1 = check_column(board, element,0,35)
    col2 = check_column(board, element,1,36)
    col3 = check_column(board, element,2,37)
    col4 = check_column(board, element,3,38)
    col5 = check_column(board, element,4,39)
    col6 = check_column(board, element,5,40)
    col7 = check_column(board, element,6,41)

    return col1 or col2 or col3 or col4 or col5 or col6 or col7










        
def check_win_conditions(board):
    raise NotImplementedError("fill this in!")


def play_move(board, player, column):
    raise NotImplementedError("fill this in!")
