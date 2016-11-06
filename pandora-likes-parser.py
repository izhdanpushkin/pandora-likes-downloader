# This script processes pandora.html file and writes songs as lines
# to songs.txt
from bs4 import BeautifulSoup

file = "./pandora.html"


def read_file(f):
    """Convert html to a beautiful soup instance."""
    try:
        with open(f, mode="r") as html_doc:
            soup = BeautifulSoup(html_doc, "html.parser")
    except IOError as e:
        print("No 'pandora.html' file was found in the current directory")
        raise e
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
        songs_dupes = []
        list_dupes = []
        for st in stations:
            for s in stations.get(st):
                # Make line from song followed by the station it's from
                song_line = ''.join((s, " | ", st, "\n"))
                if s not in songs_set and s not in file:
                    songs_set.add(s)
                    f.write(song_line)
                    print("++ " + song_line[:-1])
                elif s not in file:
                    print("-- " + s + " was already added")
                    songs_dupes.append(s)
                else:
                    print("== " + s + ' is already on the list')
                    list_dupes.append(s)
        if not songs_set and not list_dupes:
            print("HTML file doesn't seem to have any songs")
        elif songs_dupes:
            print(str(len(songs_dupes)) + " songs were duplicates")
        if list_dupes:
            print(str(len(list_dupes)) + " songs were already on the list")
        if songs_set:
            print(str(len(songs_set)) + " songs added to the list")
    return


# write_songs(read_file(file))
