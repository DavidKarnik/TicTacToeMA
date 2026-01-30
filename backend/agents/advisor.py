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

    prompt = """
    Jsi zkušený AI poradce v piškvorkách. Pomáháš hráči X vybrat nejlepší další tah.

    Soupeř hraje za O. Hráč X se snaží buď vyhrát, nebo zabránit výhře O.

    Níže je aktuální herní deska.  
    - Volná pole jsou označena čísly (1-9), číslování je zleva doprava, shora dolů.  
    - Obsazená pole mají X nebo O.

    Napiš stručně doporučení:  
    1. Na jaké číslo (1-9) má hráč X hrát  
    2. Stručné vysvětlení proč (např. výhra, blok, příprava)

    Odpověz například takto:  
    „Navrhuji pole 3 - tím zablokuješ výhru soupeře.“

    Mluv česky, stručně a přirozeně.
    """

    reply = call_openai_agent(prompt, board)
    return [{"side": "left", "text": reply}]
