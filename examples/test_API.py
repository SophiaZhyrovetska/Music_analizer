#  A module for defining currently top songs in a certain country, using python wrapper for Musixmatch API
from musixmatch import Musixmatch
musixmatch = Musixmatch('<apikey>') #  type your key instead of <apikey>

def create_dict(js_data):
    """
    Creates a dictionary with a song name as a key and a list with an album name and an artist name as a value.
    :param js_data: json data
    :return: dict
    """
    songs_dict = dict()
    track_list = js_data['message']['body']['track_list']
    for song in track_list:
        track = song['track']
        key = track['track_name']
        value = [track['album_name'], track['artist_name']]
        songs_dict[key] = value
    return songs_dict


def top_songs(songs_num, country):
    """
    Returns a dictionary with <songs_num> top sons in a <country> country.
    :param songs_num: int
    :param country: str
    :return: dict
    """
    songs = musixmatch.chart_tracks_get(1, songs_num, f_has_lyrics=True, country=country)
    top_songs_dict = create_dict(songs)
    return  top_songs_dict









