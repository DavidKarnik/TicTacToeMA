from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents.advisor import get_advisor_messages
from backend.agents.ai_duo import generate_ai_duo_move
from backend.utils.logic import check_win

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class BoardRequest(BaseModel):
    board: list

@app.post("/ai-chat/")
def ai_chat(request: BoardRequest):
    board = request.board
    winner = check_win(board)
    if winner:
        return {"board": board,
                "advisor_messages": [{"side":"left","text":f"Hra skončila: {winner}"}],
                "ai_duo_messages":[{"side":"left","text":"Hra skončila"}]}

    # **AI Duo** místo dosavadního beginner+strategist
    new_board, ai_duo_messages = generate_ai_duo_move(board)

    # po tahu 2AI protivníka
    winner = check_win(new_board)
    if winner:
        return {"board": new_board,
                "advisor_messages": [{"side":"left","text":f"Hra skončila: {winner}"}],
                "ai_duo_messages":[{"side":"left","text":"Hra skončila"}]}

    # poradce pro hráče (X)
    advisor_messages = get_advisor_messages(new_board)

    return {
        "board": new_board,
        "advisor_messages": advisor_messages,
        "ai_duo_messages": ai_duo_messages
    }
