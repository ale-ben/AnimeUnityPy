import colorama

from AnimeUnityEngine import logging_aux, common_classes

"""
Print mode levels:
1) Print only anime info
2) Print 1 and episode list
"""

colorama.init()


@logging_aux.logger_wraps()
def print_anime_list(search_res, config, print_mode):
    # Se search_res è un anime singolo lo trasformo in array per comodità
    if isinstance(search_res, common_classes.Anime):
        search_res = [search_res]
    for res in search_res:
        # Primo livello di print, uso l'str della classe anime + info varie
        if print_mode >= 1 and config['print_level'] >= 1:
            print(str(res))
            print(
                f"year: {res.year}\t Episodes: {len(res.episodes)}\t Episode length: {res.episodes_length} minutes")
        if print_mode >= 2 and config['print_level'] >= 2:
            print("Episodes: ")
            for episode in res.episodes:
                print(str(episode))
