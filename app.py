from flask import Flask, render_template, request, redirect, url_for
from music_data_types import Artist, Song, Discography

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def render_page():
    name = request.form['name']
    option = request.form['radios']
    if name:
        if option == "Song":
            return redirect(url_for('render_song', name=name))
        else:
            return redirect(url_for('render_artist', name=name))


@app.route('/song/<name>')
def render_song(name):
    song = Song()
    song.search_song(name)
    song.get_mood()
    song.get_keywords()
    mood = song.mood
    words = song.keywords
    song_name = song.name
    artist = song.artist
    rating = song.rating
    album = song.album
    genre = song.genre
    link = song.lyrics_link
    return render_template("song.html", song_name=song_name, mood=mood, words=words, artist=artist, rating=rating,
                           album=album, genre=genre, link=link)


@app.route('/artist/<name>')
def render_artist(name):
    artist = Artist(name)
    disc = Discography(artist)
    artist_name = artist.name
    rating = artist.rating
    genre = artist.genre
    country = artist.country
    words = disc.get_overall_keywords()
    moods = disc.get_overall_mood()
    songs_num = disc.songs_num
    songs = disc.top_songs
    link = artist.link
    return render_template("artist.html", artist_name=artist_name, moods=moods, words=words, genre=genre, rating=rating,
                           country=country, link=link, songs_num=songs_num, songs=songs)

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html')

@app.errorhandler(404)
def internal_error(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run()
