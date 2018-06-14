#  A module with Song, Artist and Discography data types

from musixmatch import Musixmatch
from aylienapiclient import textapi
from itertools import groupby
from help_functions import right_name

musixmatch = Musixmatch('<appkey>')  # type your key instead of <appkey>
client = textapi.Client("<appid>", "<appkey>")  # type your app id and app key


class Song:
    "A class for representing a song"

    def __init__(self):
        """
        Initialize a new song with it's name and singer
        :param name: str
        :param singer: str
        """
        self.artist = None
        self.artist_id = None
        self.id = None
        self.rating = None
        self.album = None
        self.genre = None
        self.has_lyrics = 0
        self.lyrics = None
        self.lyrics_link = None
        self.mood = 'neutral'
        self.keywords = []

    def get_mood(self):
        """
        Defines a mood of a song
        :return: None
        """
        if self.lyrics_link is not None:
            sentiment = client.Sentiment({'url': self.lyrics_link})
            self.mood = sentiment['polarity']
        return None

    def get_keywords(self):
        """
        Returns key words of a song
        :return: list
        """
        if self.lyrics_link is not None:
            data = client.Entities({'url': self.lyrics_link})
            all_words = data['entities']['keyword']
            exclude = ['languages', 'lyrics'] + self.artist.split()
            keywords = [word.lower() for word in all_words if (' ' not in word) and (word not in exclude)]
            self.keywords = keywords[:5]
        return None

    def search_song(self, name_line):
        """
        Searches a song
        :name: str
        :return: None
        """
        name_lst = right_name(name_line)

        def search_help(name, artist):
            js_data = musixmatch.track_search(q_artist=artist, page_size=1, page=1, s_track_rating='desc', q_track=name)
            if js_data['message']['header']['available'] == 0:
                return None
            song = js_data['message']['body']['track_list'][0]['track']
            self.id = song['track_id']
            self.rating = song['track_rating']
            self.artist = song['artist_name']
            self.artist_id = song['artist_id']
            self.name = song['track_name']
            self.album = song['album_name']
            self.has_lyrics = song['has_lyrics']
            link = song['track_share_url']
            if len(song['primary_genres']['music_genre_list']) != 0:
                self.genre = song['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
            else:
                self.genre = 'Pop'
            self.lyrics_link = link[:link.find('?utm')]
            self.get_keywords()
            self.get_mood()
            return 1

        if search_help(name_lst[0], name_lst[1]) is None:
            if search_help(name_lst[1], name_lst[0]) is None:
                return None


class Artist:
    "A class for representing a singer"

    def __init__(self, name):
        """
        Initialize a new singer with it's name
        :param name: str
        """
        self.name = name
        self.link = None
        self.genre = None
        self.id = None
        self.rating = None
        self.artist_info()

    def artist_info(self):
        js_data = musixmatch.artist_search(q_artist=self.name, page_size=1, page=1, f_artist_id=0, f_artist_mbid=0)
        if js_data['message']['header']['available'] == 0:
            return None
        info = js_data['message']['body']['artist_list'][0]['artist']
        self.name = info['artist_name']
        self.id = info['artist_id']
        self.country = info['artist_country']
        self.link = info['artist_share_url']
        self.rating = info['artist_rating']
        if len(info['primary_genres']['music_genre_list']) != 0:
            self.genre = info['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
        else:
            self.genre = 'Pop'


class Discography:
    "A class for representing a discography of a singer. Uses Singer() and Song() instances"

    def __init__(self, artist):
        """
        Initialize a new discography
        :param singer: Singer() instance
        """
        self.artist = artist
        self.songs_num = None
        self.songs = []
        self.top_songs = []
        self.get_songs(7)

    def get_songs(self, num):
        js_data = musixmatch.track_search(q_artist=self.artist.name, page_size=num, page=1, s_track_rating='desc',
                                          q_track='')
        if js_data['message']['header']['available'] == 0:
            return None
        self.songs_num = js_data['message']['header']['available']
        songs_list = js_data['message']['body']['track_list']
        top = []
        for song in songs_list:
            try:
                song = song['track']
                if song['has_lyrics'] == 1:
                    s = Song()
                    s.id = song['track_id']
                    s.rating = song['track_rating']
                    s.artist = song['artist_name']
                    s.artist_id = song['artist_id']
                    s.name = song['track_name']
                    s.album = song['album_name']
                    s.has_lyrics = song['has_lyrics']
                    link = song['track_share_url']
                    s.lyrics_link = link[:link.find('?utm')]
                    s.genre = song['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
                    s.get_keywords()
                    s.get_mood()
                    self.songs.append(s)
                    top.append(s.name)
                    self.top_songs = top[:5]
            except KeyError:
                continue
            except IndexError:
                continue

    def get_overall_mood(self):
        """
        Returns an overall mood of the discography in percentage.
        First is positive, second - negative, third - neutral.
        :return: list
        """
        moods = [song.mood for song in self.songs]
        all = len(moods)
        count_moods = [moods.count('positive'), moods.count('negative'), moods.count('neutral')]
        return [str(round(100 * num / all)) for num in count_moods]

    def get_overall_keywords(self):
        all_keywords = []
        lst = []
        for song in self.songs[:5]:
            all_keywords += song.keywords
        s_all_keywords = sorted(all_keywords)
        popular = sorted(s_all_keywords, key=lambda x: s_all_keywords.count(x), reverse=True)
        return [el for el, _ in groupby(popular)][:5]
