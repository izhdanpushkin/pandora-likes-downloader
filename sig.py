def sig(h):
    """Signing algorythm for youtube-mp3.org."""
    f = 1.51214;
    result = 3219
    chars = {"a": 870, "b": 906, "c": 167, "d": 119, "e": 130, "f": 899
    , "g": 248 , "h": 123, "i": 627, "j": 706, "k": 694, "l": 421
    , "m": 214, "n": 561 , "o": 819, "p": 925, "q": 857, "r": 539
    , "s": 898, "t": 866, "u": 433 , "v": 299, "w": 137, "x": 285
    , "y": 613, "z": 635, "_": 638, "&": 639 , "-": 880, "/": 687, "=": 721}

    for e in range (0, len(h)):
        char = h[e].lower()
        if char.isdigit():
            result += float(char) * 121 * f
        elif char in chars:
            result += chars[char] * f
        result = result * 0.1
    result = int(round(result * 1000))
    return result
