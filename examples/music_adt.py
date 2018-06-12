class Song:
   "A class for representing a song"

   def __init__(self, name, singer):
       """
       Initialize a new song with it's name and singer
       :param name: str
       :param singer: str
       """
       self.name = name
       self.singer = singer
       self.mood = self.mood()

   def text(self):
       """
       Returns a text of a song
       :return: str
       """
       pass

   def mood(self):
       """
       Returns a mood of a song
       :return: str
       """
       pass

   def theme(self):
       """
       Returns a theme of a song
       :return: str
       """
       pass

   def key_words(self):
       """
       Returns key words of a song
       :return: list
       """
       pass
    
class Singer:
   "A class for representing a singer"

   def __init__(self, name):
       """
       Initialize a new singer with it's name
       :param name: str
       """
       self.name = name

class Discography:
"A class for representing a discography of a singer. Uses Singer() and Song() instances"

   def __init__(self, singer):
       """
       Initialize a new discography
       :param singer: Singer() instance
       """
       self.singer = singer
       self.songs = []

   def add_song(self, song):
       """
       Adds a song to discography (self.songs)
       :param song: Song() instance
       :return: None
       """
       pass

   def number_of_songs(self):
       """
       Returns a number of songs in this discography
       :return: int
       """
       pass

   def mood(self):
       """
       Returns a a dictionary, with moods as keys and number of songs as values
       :return: dict
       """
       pass

   def themes(self):
       """
       Returns most popular themes of songs in this discography
       :return: list
       """
       pass

