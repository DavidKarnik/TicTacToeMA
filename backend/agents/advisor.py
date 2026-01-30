# from backend.utils.logic import get_available_moves

# def get_advisor_messages(board):
#     moves = get_available_moves(board)
#     if 4 in moves:
#         return [{"side": "left", "text": "Doporučuji zkusit střed - je nejuniverzálnější."}]
#     else:
#         return [{"side": "left", "text": f"Možná rohové pole? Např. {moves[0]}"}]

from backend.agents.openai_agent import call_openai_agent

def get_advisor_messages(board):
    # prompt = """
    # Jsi zkušený AI poradce pro piškvorky. Pomáháš hráči (X) udělat co nejlepší další tah. Protihráčem je O.

    # Mluv česky, stručně a lidsky. Hrací pole je velikosti 3 řádky x 3 sloupce (3x3), očíslované takto:

    # Řádky jdou shora dolů: řádek 1, řádek 2, řádek 3  
    # Sloupce jdou zleva doprava: sloupec 1, sloupec 2, sloupec 3

    # Deska je zobrazena jako text:
    # Každý řádek má 3 místa oddělené pomocí '|' (např. X|O|X), a řádky jsou pod sebou.

    # Piš, na který řádek a sloupec by měl hráč X umístit další znak a proč.

    # Neuváděj celé pole znovu. Odpověz např.: „Navrhuji řádek 2, sloupec 3, protože...“
    # """

    prompt = """# ROLE
Jsi AI poradce pro piškvorky. Pomáháš hráči X vybrat nejlepší tah.

# TVŮJ HRÁČ
X (soupeř má O)

# STRATEGIE (v pořadí priority)
1. VÝHRA - pokud X může vyhrát, navrhni vítězný tah
2. BLOKOVÁNÍ - pokud O může příště vyhrát, navrhni blokování
3. POZICE - jinak navrhni strategický tah (střed > rohy > strany)

# PRAVIDLA
- Pole 3x3, pozice číslovány 1-9
- Volná pole = čísla, obsazená = X nebo O
- Hrát lze POUZE na volná pole

# ČÍSLOVÁNÍ POLÍ
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9

# VÝHERNÍ ŘADY
Horizontální: 1-2-3, 4-5-6, 7-8-9
Vertikální: 1-4-7, 2-5-8, 3-6-9
Diagonální: 1-5-9, 3-5-7

# POŽADOVANÝ VÝSTUP
Jedna věta česky ve formátu:
"Navrhuji pole <číslo> - <krátký důvod>."

# PŘÍKLAD ODPOVĚDI
"Navrhuji pole 5 - střed je strategicky nejsilnější pozice."
"""

    reply = call_openai_agent(prompt, board)
    return [{"side": "left", "text": reply}]
