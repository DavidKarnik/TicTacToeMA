# backend/agents/ai_duo.py

import re
from backend.agents.openai_agent import call_openai_agent
from backend.utils.logic import get_available_moves, make_move, board_to_str

def extract_number(text: str) -> int:
    m = re.search(r"(\d+)", text)
    return int(m.group(1)) if m else None

def generate_ai_duo_move(board: list) -> tuple[list, list]:
    board_str = board_to_str(board)

    # 1) Začátečník navrhne tah
    b_prompt = f"""
    Jsi začátečník v piškvorkách (O). Pole je:
    {board_str}

    Navrhni tah (číslo 1–9) a stručně vysvětli.
    Odpověz ve formátu:
    Tah: <číslo>
    Důvod: <text>
    """
    b_reply = call_openai_agent(b_prompt, board)
    b_move = extract_number(b_reply)
    b_reason = b_reply.split("Důvod:")[-1].strip()

    # 2) Expert zhodnotí a navrhne případnou změnu
    e_prompt = f"""
    Jsi expert na piškvorky. Pole je:
    {board_str}

    Začátečník navrhl tah {b_move} – {b_reason}. Zhodnoť:
    - Je tento tah dobrý?
    - Pokud ne, navrhni lepší.
    Odpověz ve formátu:
    Hodnocení: <text>
    Tah: <číslo>
    Důvod: <text>
    """
    e_reply = call_openai_agent(e_prompt, board)
    e_move = extract_number(e_reply.split("Tah:")[-1])
    e_reason = e_reply.split("Důvod:")[-1].strip()
    e_feedback = e_reply.split("Hodnocení:")[1].split("Tah:")[0].strip()

    # 3) Začátečník se rozhodne – posluší experta, nebo zůstane
    d_prompt = f"""
    Původní tah: {b_move} – {b_reason}
    Expert řekl: {e_feedback}, navrhl {e_move} – {e_reason}
    Rozhodni, jestli:
    1. Zůstaneš u {b_move}
    2. Použiješ {e_move}
    Odpověz ve formátu:
    Vybraný tah: <číslo>
    Důvod: <text>
    """
    d_reply = call_openai_agent(d_prompt, board)
    final_move = extract_number(d_reply)
    final_reason = d_reply.split("Důvod:")[-1].strip()

    # 4) Aplikuj finální tah a vrať nové board + zprávy
    new_board = make_move(board, final_move, "O")
    messages = [
        {"side": "left",  "text": f"Začátečník: Tah {b_move} – {b_reason}"},
        {"side": "right", "text": f"Expert: {e_feedback} Tah {e_move} – {e_reason}"},
        {"side": "left",  "text": f"Začátečník: Rozhodl jsem se pro {final_move} – {final_reason}"}
    ]
    return new_board, messages