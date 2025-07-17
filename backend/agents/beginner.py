import random
from backend.utils.logic import get_available_moves

def get_beginner_move(board):
    moves = get_available_moves(board)
    return random.choice(moves)
