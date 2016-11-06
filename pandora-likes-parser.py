from bs4 import BeautifulSoup

file = "./pandora.html"
files = []


def read_file(f):
    with open(f, mode="r") as html_doc:
        soup = BeautifulSoup(html_doc, "html.parser")
    return soup


def write_songs(soup):
    c = 0
    stations = {}
    for line in soup.find_all("div", "infobox-body"):
        if c < 10:
            artist = line.p.a.text
            title = line.h3.a.text
            # f.write(artist + " - " + title + "\n")
            station = line.find("a", "like_context_stationname").text
            # print artist, title, station
            if station not in stations:
                stations[station] = [str(artist + " - " + title).strip()]
            else:
                stations[station].append(
                    str(artist + " - " + title).strip())
            c += 1
        else:
            break
    with open("./songs1.txt", mode="a+") as f:

        # print stations
        for st in stations:
            # print st
            for s in stations.get(st):
                song_line = s + " | " + st + '\n'
                if s not in f:
                    f.write(song_line)
write_songs(read_file(file))


def clean_dupes():
    with open("./songs.txt", mode="r") as old:
        with open("./songs-clean.txt", mode="w+") as new:
            songset = set()
            for line in old:
                songset.add(line)
            for song in songset:
                new.write(song)
