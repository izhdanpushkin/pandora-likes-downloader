import json
import os
import requests
from bs4 import BeautifulSoup

songs = []
with open ("./songs-clean.txt", "r") as s:
    for e in s.readlines():
        if "/" in e:
            e = e.replace("/", "")
        songs.append(e[0:-1])


def yt_query(song):
    """Create a query for youtube search from song name."""
    if " " in song:
        song_split = ""
        for word in song.split():
            if song.split().index(word) == len(song.split()) - 1:
                song_split += str(word + "+lyrics")
                continue
            song_split += str(word) + "+"
        return song_split
    return song


def yt_request(query):
    """Search youtube with provided query
    and extract id of the first video.
    """
    r = requests.get(
        "https://www.youtube.com/results?search_query={}".format(query))
    soup = BeautifulSoup(r.text, "html.parser")
    video = soup.find_all("div", "yt-lockup-video")
    video_id = video[0]["data-context-item-id"]
    return video_id


def yt_download(video_id):
    """Request download link from youtubeinmp3.com."""
    link = ("https://www.youtubeinmp3.com/fetch/?format=JSON&video=" +
            "https://www.youtube.com/watch?v={}".format(video_id))
    r = requests.get(link)
    json_text = json.loads(r.text)
    dl_link = json_text["link"]
    return dl_link


def download_file(dl_link, song, cnt=0):
    """Download file and write it in the current folder as song."""
    if cnt == 0:
        print("started writing " + song)
    song_file = "./" + song + ".mp3"
    with open(song_file, "wb") as f:
        r = requests.get(dl_link)
        if r.status_code == 200:
            for chunk in r:
                if chunk:
                    f.write(chunk)
    x = os.path.getsize(song_file)

    if x < 30000 and cnt < 10:  # Retry writing if it fails
        print("({}) retrying writing ".format(cnt+1) + song)
        return download_file(dl_link, song, cnt+1)
    elif cnt >= 10:
        print("writing fucked up\n")
        with open("./failed-songs.txt", "a+") as fails:
            line = (str(song + "\n"))
            if not line in fails:
                fails.write(line)
        return
    print("finished writing " + song + "\n")
    return


def get_songs(songs):
    """Download files from songs list."""
    counter = 0
    for song in songs:
        print(songs.index(song))
        query = yt_query(song)
        try:
            request = yt_request(query)
            dl_link = yt_download(request)
        except:
            print("downloading site fucked up with " + song + "\n")
            with open("./failed-songs.txt", "a+") as fails:
                line = (str(song + "\n"))
                if not line in fails:
                    fails.write(line)
            continue
        download_file(dl_link, song)
        counter += 1
    print("Songs downloaded - " + str(counter))
    return


# get_songs(songs)
