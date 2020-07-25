import colorama
import os
import platform
from shutil import which
from platform import system
from youtube_dl import YoutubeDL
from tqdm import trange
from tqdm import tqdm
from time import sleep
from AnimeUnityEngine import logging_aux, common_classes
import re

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
                if "vvvvid.it" in str(episode):
                    vvvvid_downloader(res)
                    break
                else:
                    print(str(episode))

def vvvvid_downloader(anime):
    #ep = "ajeje"
    #pbar = tqdm(total=len(anime.episodes), bar_format=(ep + "{l_bar}{bar}| {n_fmt}/{total_fmt}"))
    content_dir = os.path.join("Download", anime.slug)
    if not os.path.exists(content_dir):
        os.makedirs(content_dir)

    ffmpeg_local = ""
    if which("ffmpeg") is None:
        # If the user is running the script from Windows or Mac, ffmpeg's build can be inside dependency folder
        if system() in ["Windows", "Darwin"]:
            _dir = os.path.dirname(os.path.realpath(__file__))
            ffmpeg_dir_files = os.listdir(os.path.join(_dir, "ffmpeg"))
            ffmpeg_dir_files.remove("readme.md")
            # If the directory is ambiguous stop the script
            if len(ffmpeg_dir_files) > 1:
                print(
                    "La tua directory di ffmpeg contiene troppi file/cartelle. Assicurati che contenga solo il readme e la cartella con la build di ffmpeg."
                )
                quit()
            elif len(ffmpeg_dir_files) == 0:
                print(
                    "Questo script ha una dipendenza da ffmpeg, che non risulta essere installato. Per maggiori informazioni, consulta il readme sulla pagina GitHub del progetto."
                )
                quit()

            ffmpeg_local = os.path.join(
                _dir, "ffmpeg", ffmpeg_dir_files[0], "bin"
            )
        else:
            print(
                "Questo script ha una dipendenza da ffmpeg, che non risulta essere installato. Per maggiori informazioni, consulta il readme sulla pagina GitHub del progetto, nella sezione installazione per Ubuntu."
            )
            quit()
    pbar = tqdm(anime.episodes, bar_format=("{l_bar}{bar}| {n_fmt}/{total_fmt}"))
    for episode in pbar:
        title = re.findall("(.*)/(.*)$", episode.link)[0][1]
        #https://www.vvvvid.it/show/558/sword-art-online/1104/541488/il-mondo-della-spada
        pbar.set_description("Processing %s" % title)
        #pbar.bar_format = (str(episode.e_id) + " " + "{l_bar}{bar}| {n_fmt}/{total_fmt}")
        #ep = "brazorf "#episode.e_id
        ydl_opts = {
            "format": "best",
            "outtmpl": "%s/%s.%%(ext)s" % (content_dir, title),
            "continuedl": True,
            "quiet" : True,
        }
        if ffmpeg_local:
            ydl_opts["ffmpeg_location"] = ffmpeg_local
        with YoutubeDL(ydl_opts) as ydl:
            #pbar.update(1)
            #sleep(2)
            ydl.download([episode.link])

    #pbar.close()