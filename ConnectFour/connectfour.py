from collections import defaultdict

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




def check_diagonal(board, element, diagonal):
    for index in diagonal:
        if board[index] != element:
            return False
    return True

def generate_diagonals():
    positive_diagonals = []
    negative_diagonals = []

    positive_diagonal_starts = (3, 4, 5 ,6, 10, 11, 12, 13, 17, 18, 19, 20)
    negative_diagonal_starts = (0, 1, 2, 3,7,8,9,10,14,15,16,17)

    
    postive_step = 6
    for index in positive_diagonal_starts:
        diagonal = []
        for i in range(index, index + 4 * postive_step , postive_step):
            diagonal.append(i)
        positive_diagonals.append(diagonal)
    

    negative_step = 8
    for index in negative_diagonal_starts:
        diagonal = []
        for i in range(index, index + 4 * negative_step , negative_step):
            diagonal.append(i)
        negative_diagonals.append(diagonal)
    
    return positive_diagonals + negative_diagonals
    

def check_all_diagonals(board, element): 
    diagonals = generate_diagonals()

    for diagonal in diagonals:
        if check_diagonal(board, element, diagonal):
            return True
    return False
        
def check_win_conditions(board):
    players = (1,2)

    winners = []

    for player in players:
        if check_all_columns(board, player) or check_all_rows(board, player) or check_all_diagonals(board, player):
            winners.append(player)
    
    if len(winners) == 0:
        return 0
    
    if len(winners) == 2:
        raise Exception("There are two winners: Impossible board")
    
    return winners[0]

def column_indices_map():
    mapp = defaultdict(list)
    for i in range(0,7):
        for j in range(i + 35, i - 1, -7):
            mapp[i].append(j)
        mapp[i].append(-1)
    return mapp


def play_move(board, player, column):
    
    column_positions_map = column_indices_map()

    column_indices = column_positions_map[column]

    for position in column_indices:
        if position == -1:
            break
        if board[position] == 0:
            board[position] = player
            return board
        
    raise Exception(f"column {column} is full")
    


