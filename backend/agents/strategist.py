from backend.utils.logic import get_available_moves

def get_strategic_move(board):
    moves = get_available_moves(board)
    # velmi jednoduchá strategie
    center = 5
    if center in moves:
        return {"move": center, "reason": "střed je vždy výhodný"}

    move = moves[0]
    return {"move": move, "reason": "beru první volné pole"}
