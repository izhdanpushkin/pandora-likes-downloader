# This Python file uses the following encoding: utf-8
from bs4 import BeautifulSoup

file = "./pandora1.html"
files = []


def read_file(f):
    """Convert html to beautiful soup instance."""
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
        song = u" - ".join((artist, title)).encode("utf-8").strip()
        if station not in stations:
            stations[station] = [song]
        else:
            stations[station].append(song)

    with open("./songs.txt", mode="a+") as f:
        file = f.read()
        songs_set = set()
        for st in stations:
            for s in stations.get(st):
                song_line = ''.join((s, " | ", st, "\n"))
                if s not in songs_set and s not in file:
                    songs_set.add(s)
                    f.write(song_line)
                    print("++ " + song_line[:-1])
                else:
                    print("-- " + s + ' is already on the list')
    return


# write_songs(read_file(file))