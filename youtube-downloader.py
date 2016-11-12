# This script searches youtube for songs in 'songs.txt' and downloads
# them as mp3 files.
import json
import re
import random
import time
import os
from sig import sig
import requests
from bs4 import BeautifulSoup

songs = []
with open("./songs.txt", "r") as s:
    downloaded = ""
    failed = ""
    try:
        with open("./songs-downloaded.txt", "r") as d:
            downloaded = d.read()
        with open("./songs-failed.txt", "r") as f:
            failed = f.read()
    except IOError:
        pass

    for e in s.readlines():
        if "/" in e:
            e = e.replace("/", "")
        name = e.split(" | ")[0]
        if name in downloaded or name in failed:
            continue
        songs.append(name)


def yt_query(song):
    """Create a query for youtube search from song name."""
    if " " in song:
        song_split = ""
        for word in song.split():
            if song.split().index(word) == len(song.split()) - 1:
                # song_split += str(word + "+lyrics")
                song_split += str(word)
                continue
            song_split += str(word) + "+"
        return song_split
    return song


def yt_request(query):
    """Search youtube with provided query, match videos with
    song's name and extract id of the best match.
    """
    r = requests.get(
        "https://www.youtube.com/results?search_query={}".format(query))
    soup = BeautifulSoup(r.text, "html.parser")
    videos = soup.find_all("div", "yt-lockup-video")
    titles = soup.find_all("h3", "yt-lockup-title")
    best_match = ["", 0, ""]

    for e in range(0, len(videos)):
        song = query.lower().split("+")
        video_id = videos[e]["data-context-item-id"]
        title = soup.find(
            'a', 'yt-uix-tile-link', href=re.compile(video_id)).string

        matched = 0
        for word in title.lower().split():
            if word in song:
                matched += 1
                # Remove word to avoid further comparisons to it
                song.pop(song.index(word))

        if matched > best_match[1]:
            # print video_id, matched, title  # For testing purposes
            best_match[0] = video_id
            best_match[1] = matched
            best_match[2] = title

    return best_match[0]


def yt_download(video_id):
    """Request download link from youtube-mp3.com."""
    timestamp = str(int(time.time()))
    tail = random.sample(range(100, 999), 2)
    # Generate timestamp that complies with site's version
    ts = [timestamp + str(min(tail)), timestamp + str(max(tail))]
    push = 'http://www.youtube-mp3.org/a/pushItem/?item=https%3A//www.youtube.com/watch%\3Fv%3D{}&el=ma&bf=false&r={}&s={}'.format(video_id, ts[0], sig(ts[0]))
    info = 'http://www.youtube-mp3.org/a/itemInfo/?video_id={}&ac=www&t=grp&r={}&s={}'.format(video_id, ts[1], sig(ts[1]))

    requests.get(push)  # Make sure video is converted
    r = requests.get(info)
    txt = r.text.split('info = ')[1][:-1]  # JSON-friendly part of response
    js = json.loads(txt)
    dl_link = ('http://www.youtube-mp3.org/get?video_id={}&ts_create={}&r=MTg4LjIzMS4xMzEuNzQ%3D&h2={}&s={}'.format(video_id, js["ts_create"], js["h2"], sig(js["h2"])))
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
        print("writing messed up\n")
        with open("./songs-failed.txt", "a+") as fails:
            line = (str(song + "\n"))
            if not line in fails:
                fails.write(line)
        return None

    with open("./songs-downloaded.txt", "a+") as d:
        line = (str(song + "\n"))
        if not line in d:
            d.write(line)
    print("finished writing " + song + "\n")
    return True


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
            print("downloading site messed up with " + song + "\n")
            with open("./songs-failed.txt", "a+") as fails:
                line = (str(song + "\n"))
                if not line in fails:
                    fails.write(line)
            continue
        if download_file(dl_link, song):
            counter += 1
    print("Songs downloaded - " + str(counter))
    return


get_songs(songs)
