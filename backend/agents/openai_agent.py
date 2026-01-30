from openai import OpenAI
import os
from dotenv import load_dotenv
from backend.utils.logic import board_to_str

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_agent(role_prompt: str, board: list) -> str:
    board_str = board_to_str(board)
    messages = [
        {"role": "system", "content": role_prompt},
        {"role": "user", "content": f"Aktuální herní pole:\n{board_str}\nJaký tah navrhuješ a proč?"}
    ]
    try:
        response = client.chat.completions.create(
            # model="gpt-4.1-mini",  # Halucinuje stav herního pole
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Chyba API: {str(e)}"