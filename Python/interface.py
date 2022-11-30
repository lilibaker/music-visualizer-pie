import os
from tkinter import *
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_uri
from spotdl import __main__ as start # To initialize
# from spotdl.search.songObj import SongObj
# from pytube import YouTube

sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id="ca4037574604402aa16cc9ead70aa2e3",
            client_secret="9b7ab94755874ebc8179da11926f68c3"
        )
    )

# define global veriables
RESULTS = 0

# set up window
root = Tk()
root.title("Music Visualizer")
root.geometry("800x800")
style = ttk.Style()
style.theme_use('classic')

# add title
heading = Label(root, text="Music Visualizer")
heading.pack()

# Add instructions
instructions = Label(root, text="Choose a song to visualize from the dropdown below, or enter a different song name in the box below!")
instructions.pack()

# change label text
def show():
    label.config(text=clicked.get())

def draw_spiro():
    print("value is: " + clicked.get() + ".mp3")
    os.system("prerecorded.py COM5" + clicked.get() + ".mp3")
    

#dropdown options
options = [
    "Her Majesty",
    "Parachutes",
    "Stop"
]

clicked = StringVar() # datatype of menu text
clicked.set(options[0]) # set initial text
drop = OptionMenu(root, clicked, *options)
drop.pack()
button = Button(root, text=" ")
label = Label(root, text=" ")
label.pack()

# button to send data and run prerecorded.py
draw = Button(root, text="Draw", command=draw_spiro)
draw.pack()

# download music 
def displayArtists():
    name = songName.get(1.0, "end-1c")
    artists = ""
    global RESULTS
    RESULTS = sp.search(name, limit=5)

    for i, track in enumerate(RESULTS["tracks"]["items"]):
        artists += f"[{i}] {track['name']} by {track['artists'][0]['name']}\n"
    
    artistNames.config(text = artists)

def downloadMusic():
    id = int(artistID.get(1.0, "end-1c"))
    uri = RESULTS["tracks"]["items"][id]["uri"]
    url = spotify_uri.formatOpenURL(uri)
    print(url)
    # song = SongObj.from_url(url)
    # youtube_url = song.get_youtube_link()
    # yt = YouTube(youtube_url)
    # yts = yt.streams.get_audio_only()
    # fname = yts.download('~/music')
    # print(fname)

    # other option is just to use os system
    os.system("spotdl " + url)


# text input
songName = Text(root, height=5, width=40)
songName.pack()
# button to search name of song
searchName = Button(root, text="Search Song", command=displayArtists)
searchName.pack()

# label for artist names
artistNames = Label(root, text="")
artistNames.pack()

# artist text input
artistID = Text(root, height=5, width=40)
artistID.pack()
# button to search name of song
download = Button(root, text="Done", command=downloadMusic)
download.pack()


root.mainloop()