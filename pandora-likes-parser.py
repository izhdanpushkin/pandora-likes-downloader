# This Python file uses the following encoding: utf-8
from bs4 import BeautifulSoup

file = "./pandora.html"
files = []


def read_file(f):
    with open(f, mode="r") as html_doc:
        soup = BeautifulSoup(html_doc, "html.parser")
    return soup


def write_songs(soup):
    """Find songs in soup and write them to file."""
    stations = {}

    for line in soup.find_all("div", "infobox-body"):
        artist = line.p.a.text
        title = line.h3.a.text
        station = line.find("a", "like_context_stationname").text.encode(
            "utf-8")
        try:
            song = str(artist + " - " + title).strip()
        except UnicodeEncodeError as e:
            song = u" - ".join((artist, title)).encode("utf-8").strip()
        if station not in stations:
            stations[station] = [song]
        else:
            stations[station].append(song)

    with open("./songs.txt", mode="a+") as f:
        songs_set = set()
        for st in stations:
            for s in stations.get(st):
                song_line = s + " | " + st + '\n'
                if s not in songs_set:
                    songs_set.add(s)
                    f.write(song_line)
                else:
                    print s
    return


write_songs(read_file(file))
# with open("./songs.txt", "r") as f1, open("./songs10.txt", "w+") as f2:
#     songs = set()
#     for line in f1.readlines():
#         songs.add(line)
#     for song in songs:
#         f2.write(song)