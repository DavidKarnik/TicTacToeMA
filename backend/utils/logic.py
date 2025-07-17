def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell is None]

def make_move(board, index, symbol):
    new_board = board.copy()
    new_board[index] = symbol
    return new_board

def check_win(board):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6],
    ]
    for a,b,c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell is not None for cell in board):
        return "remíza"
    return None
