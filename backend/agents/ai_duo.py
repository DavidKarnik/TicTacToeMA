# backend/agents/ai_duo.py

import re
from backend.agents.openai_agent import call_openai_agent
from backend.utils.logic import get_available_moves, make_move, board_to_str

def safe_extract(text: str, keyword: str, default: str = "") -> str:
    """Bezpečně extrahuje text za klíčovým slovem."""
    parts = text.split(keyword)
    return parts[1].split("\n")[0].strip() if len(parts) > 1 else default

def extract_number(text: str, available_moves: list = None) -> int:
    """Extrahuje číslo z textu s fallbackem na první dostupný tah."""
    m = re.search(r"(\d+)", text)
    if m:
        num = int(m.group(1))
        if 1 <= num <= 9:
            return num
    # Fallback: první dostupný tah (převedený na 1-indexed)
    if available_moves:
        return available_moves[0] + 1
    return 5  # Střed jako poslední záchrana

def generate_ai_duo_move(board: list) -> tuple[list, list]:
    board_str = board_to_str(board)

    # 1) Začátečník navrhne tah
    available_str = ", ".join(str(m + 1) for m in get_available_moves(board))
    b_prompt = f"""# ROLE
Jsi začátečník v piškvorkách. Hraješ za symbol O, soupeř hraje za X.

# CÍL
Vyber tah, kterým se pokusíš vyhrát (3 symboly O v řadě).

# PRAVIDLA
- Hrací pole je 3x3, pozice jsou číslovány 1-9
- Můžeš hrát POUZE na volná pole (označená čísly)
- Pole s X nebo O jsou obsazená - NELZE na ně hrát
- Výhra = 3 stejné symboly v řadě (horizontálně, vertikálně, diagonálně)

# ČÍSLOVÁNÍ POLÍ
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9

# AKTUÁLNÍ STAV HRY
{board_str}

# VOLNÁ POLE
{available_str}

# POŽADOVANÝ VÝSTUP
Odpověz PŘESNĚ v tomto formátu (nic jiného):
Tah: <číslo 1-9>
Důvod: <krátké vysvětlení>

# PŘÍKLAD ODPOVĚDI
Tah: 5
Důvod: Střed je strategicky výhodný.
"""
    available = get_available_moves(board)
    b_reply = call_openai_agent(b_prompt, board)
    b_move = extract_number(b_reply, available)
    b_reason = safe_extract(b_reply, "Důvod:", "neuveden")

    # 2) Expert zhodnotí a navrhne případnou změnu
    e_prompt = f"""# ROLE
Jsi expert na piškvorky. Hodnotíš tah začátečníka a případně navrhuješ lepší.

# TVŮJ SYMBOL
O (soupeř má X)

# STRATEGIE (v pořadí priority)
1. VÝHRA - pokud můžeš vyhrát tímto tahem, udělej to
2. BLOKOVÁNÍ - pokud soupeř může vyhrát příštím tahem, zablokuj ho
3. POZICE - jinak hraj strategicky (střed > rohy > strany)

# PRAVIDLA
- Pole 3x3, pozice 1-9
- Hrát lze POUZE na volná pole (čísla)
- X a O jsou obsazená pole - NELZE na ně hrát

# ČÍSLOVÁNÍ POLÍ
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9

# AKTUÁLNÍ STAV HRY
{board_str}

# VOLNÁ POLE
{available_str}

# VÝHERNÍ ŘADY (3 v řadě = výhra)
Horizontální: 1-2-3, 4-5-6, 7-8-9
Vertikální: 1-4-7, 2-5-8, 3-6-9
Diagonální: 1-5-9, 3-5-7

# PŘÍKLAD VÝHRY O
O | O | 3    → Tah na 3 = výhra (řada 1-2-3)
---------
X | X | 6
---------
7 | 8 | 9

# PŘÍKLAD NUTNÉHO BLOKOVÁNÍ
X | X | 3    → Tah na 3 = blokování (jinak X vyhraje)
---------
O | O | 6
---------
7 | 8 | 9

# NÁVRH ZAČÁTEČNÍKA
Tah: {b_move}
Důvod: {b_reason}

# TVŮJ ÚKOL
Zhodnoť návrh začátečníka. Je tah {b_move} optimální? Pokud ne, navrhni lepší.

# POŽADOVANÝ VÝSTUP
Odpověz PŘESNĚ v tomto formátu:
Hodnocení: <je tah dobrý/špatný a proč>
Tah: <číslo 1-9>
Důvod: <krátké vysvětlení>
"""
    e_reply = call_openai_agent(e_prompt, board)
    e_move = extract_number(e_reply.split("Tah:")[-1], available)
    e_reason = safe_extract(e_reply, "Důvod:", "neuveden")
    e_feedback = safe_extract(e_reply, "Hodnocení:", "bez hodnocení")
    # Ořízni text před "Tah:" pokud existuje
    if "Tah:" in e_feedback:
        e_feedback = e_feedback.split("Tah:")[0].strip()

    # 3) Začátečník se rozhodne – poslechne experta, nebo ne
    d_prompt = f"""# ROLE
Jsi začátečník v piškvorkách. Rozhoduješ se mezi svým původním tahem a radou experta.

# SITUACE
Tvůj původní návrh: Tah {b_move} - {b_reason}
Expertova rada: {e_feedback}
Expert navrhuje: Tah {e_move} - {e_reason}

# TVŮJ ÚKOL
Vyber jeden z tahů:
- Tah {b_move} (tvůj původní)
- Tah {e_move} (expertův návrh)

# VOLNÁ POLE
{available_str}

# POŽADOVANÝ VÝSTUP
Odpověz PŘESNĚ v tomto formátu:
Vybraný tah: <číslo>
Důvod: <krátké vysvětlení proč jsi vybral tento tah>
"""
    d_reply = call_openai_agent(d_prompt, board)
    final_move = extract_number(d_reply, available)
    final_reason = safe_extract(d_reply, "Důvod:", "neuveden")

    # 4) Aplikuj finální tah a vrať nové board + zprávy
    new_board = make_move(board, final_move, "O")
    messages = [
        {"side": "left",  "text": f"Začátečník: Tah {b_move} – {b_reason}"},
        {"side": "right", "text": f"Expert: {e_feedback} Tah {e_move} – {e_reason}"},
        {"side": "left",  "text": f"Začátečník: Rozhodl jsem se pro {final_move} – {final_reason}"}
    ]
    return new_board, messages