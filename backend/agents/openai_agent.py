from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_agent(role_prompt: str, board: list) -> str:
    board_str = board_to_str(board)
    print(board_str)
    messages = [
        {"role": "system", "content": role_prompt},
        {"role": "user", "content": f"Herní pole:\n{board_str}\nJaký tah navrhuješ a proč?"}
    ]
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# def board_to_str(board):
#     def mark(i): return board[i] if board[i] else " "
#     return (f"{mark(0)}|{mark(1)}|{mark(2)}\n"
#             # f"-+-+-\n"
#             f"{mark(3)}|{mark(4)}|{mark(5)}\n"
#             # f"-+-+-\n"
#             f"{mark(6)}|{mark(7)}|{mark(8)}")

def board_to_str(board):
    def mark(i):
        return board[i] if board[i] else str(i + 1)
    return (
        f"{mark(0)} | {mark(1)} | {mark(2)}\n"
        f"---------\n"
        f"{mark(3)} | {mark(4)} | {mark(5)}\n"
        f"---------\n"
        f"{mark(6)} | {mark(7)} | {mark(8)}"
    )

