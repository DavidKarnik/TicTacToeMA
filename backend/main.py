from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agents.strategist import get_strategic_move
from backend.agents.beginner import get_beginner_move
from backend.agents.advisor import get_advisor_messages
from backend.utils.logic import make_move, check_win, get_available_moves

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BoardRequest(BaseModel):
    board: list

@app.post("/ai-chat/")
def ai_chat(request: BoardRequest):
    board = request.board

    # zkontroluj, jestli hra už neskončila
    winner = check_win(board)
    if winner:
        return {
            "board": board,
            "advisor_messages": [{"side": "left", "text": f"Hra skončila, vítěz: {winner}"}],
            "ai_duo_messages": [{"side": "left", "text": "Hra skončila"}]
        }

    # začátečník navrhne tah
    beginner_move = get_beginner_move(board)

    # stratég odpoví a vybere tah
    strategic_result = get_strategic_move(board)
    strategic_move = strategic_result["move"]
    reason = strategic_result["reason"]

    # aplikuj tah
    board = make_move(board, strategic_move, "O")

    # vytvoř konverzaci AI duo
    ai_duo_messages = [
        {"side": "left", "text": f"Začátečník: Co takhle tah na {beginner_move}?" },
        {"side": "right", "text": f"Stratég: Ne, radši {strategic_move}, protože {reason}." },
        {"side": "left", "text": f"Začátečník: Aha, chápu!" }
    ]

    # poradce pro hráče (pro X)
    advisor_messages = get_advisor_messages(board)

    return {
        "board": board,
        "advisor_messages": advisor_messages,
        "ai_duo_messages": ai_duo_messages
    }
