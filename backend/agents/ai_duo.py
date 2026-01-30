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
    Jsi začátečník v piškvorkách. Hraješ za symbol O. Tvůj protivník má symbol X.

    Navrhni tah (číslo 1 až 9 dle hracího pole, tam kde nejsou obsazena pole znaky) a velmi stručně vysvětli. Můžeš hrát všechny pole, kde jsou čísla. Tam kde jsou znaky, už někdo zahrál.
    Ty hraješ jako symbol (o) a soupeř jako symbol (x). Snaž se vyhrát - mít 3 spojené symboly o vedle sebe. Diagonálně, vertikálně, nebo horizontálně. Pole je 3x3, takže pozice 1 až 9.
    
    Čisté pole je:
    1 | 2 | 3
    ---------
    4 | 5 | 6
    ---------
    7 | 8 | 9
    Aktuální rozehrané pole je:
    {board_str}

    Odpověz ve formátu:
    Tah: <číslo>
    Důvod: <text>
    """
    b_reply = call_openai_agent(b_prompt, board)
    b_move = extract_number(b_reply)
    b_reason = b_reply.split("Důvod:")[-1].strip()

    # 2) Expert zhodnotí a navrhne případnou změnu
    e_prompt = f"""
    Jsi expert na piškvorky, co má za úkol poradit začátečníkovi jeho další tah (O). Hrajete za symbol O a váš protivník má symbol X. Můžeš hrát všechny pole, kde jsou čísla. Tam kde jsou znaky, už někdo zahrál.
    Musíš se snažit vyhrát, ne jen blokovat soupeřovu výhru. Pokud můžeš vyhrát, tak proveď tah na výhru a ne na blokování soupeře. Výhra je priorita a hra končí, když jeden z hráčů vyhraje.
    Pokud ale soupeři chybí udělat jen jeden tah a ty svým aktuálním tahen nemůžeš hru vyhrát a ukončit, tak zablokuj protihráče (x)
    Pole má rozměr 3x3. Od 1. do 9. pole. Tam, kde je symbol, už nelze umístit tah - to pole je zabrané. Nemůžeš udělat tah na políčko, kde už symbol je (vždy se řiď aktuálním rozehraným polem hry) Pole je:
    Aktuální rozehrané pole je:
    {board_str}

    Čisté pole (pro orientaci) je:
    1 | 2 | 3
    ---------
    4 | 5 | 6
    ---------
    7 | 8 | 9

    Tady je příklad výtězné situace pro tebe (o):
    X | X | O
    ---------
    X | O | 6
    ---------
    O | 8 | 9
    - v tomto případě hráč (x) obsadil pozice 1,2,4
    - hráč (o) obsadil pole 3,5,7

    Další příklad výhry:
    O | O | O
    ---------
    X | X | 6
    ---------
    7 | X | 9
    Tady je připad další hry, kdy jsi na řadě ty (o) a můžeš vyhrát tahem na pozici 9:
    O | X | X
    ---------
    X | O | 6
    ---------
    7 | X | 9
    
    Tady je příklad tvé prohry, protivník (x) vyhrál. Zde (x) vyhrál spojením pozic 1,2,3. To nechceš:
    X | X | X
    ---------
    O | O | 6
    ---------
    7 | 8 | 9
    - zde soupeř (x) obsadil pole 1,2,3
    - ty, hráč jsi (o) obsadil pole 4,5

    Další příklad prohry:
    X | O | X
    ---------
    O | X | 6
    ---------
    O | 8 | X

    Začátečník navrhl tah {b_move} - {b_reason}. Velmi stručně zhodnoť:
    - Je tento tah dobrý?
    - Pokud ne, navrhni lepší.
    Odpověz stručně ve formátu:
    Hodnocení: <text>
    Tah: <číslo>
    Důvod: <text>
    """
    e_reply = call_openai_agent(e_prompt, board)
    e_move = extract_number(e_reply.split("Tah:")[-1])
    e_reason = e_reply.split("Důvod:")[-1].strip()
    e_feedback = e_reply.split("Hodnocení:")[1].split("Tah:")[0].strip()

    # 3) Začátečník se rozhodne – poslechne experta, nebo ne
    d_prompt = f"""
    Původní tah: {b_move} - {b_reason}
    Expert řekl: {e_feedback}, navrhl {e_move} - {e_reason}
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