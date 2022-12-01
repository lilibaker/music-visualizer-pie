# import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import prerecorded

sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id="ca4037574604402aa16cc9ead70aa2e3",
            client_secret="9b7ab94755874ebc8179da11926f68c3"
        )
    )

# define global veriables
RESULTS = 0
features = []


# set up window
root = ThemedTk(theme="breeze")
root.title("Music Visualizer")
root.geometry("800x800")
frmMain = tk.Frame(root)
frmMain.grid(row=0, column=0, sticky="")
frmMain.grid_rowconfigure(0, weight=1)
frmMain.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# add title
heading = ttk.Label(frmMain, text="Music Visualizer", font=("Arial", 25))
heading.grid(row=0, column = 0, pady = 7)

# # Add instructions
# instructions = ttk.Label(frmMain, 
#                         text="Choose a song to visualize from the dropdown below, or enter a different song name in the box below!",
#                         font=("Arial", 12),
#                         wraplength=500,
#                         justify="center")
# instructions.grid(row=1, column = 0, pady = 7)

# # change label text
# def show():
#     label.config(text=clicked.get())

# def draw_spiro():
#     print("value is: " + clicked.get() + ".mp3")
#     os.system("python3 prerecorded.py COM5" + clicked.get() + ".mp3")
    

# #dropdown options
# options = [
#     "Her Majesty",
#     "Parachutes",
#     "Stop"
# ]

# clicked = tk.StringVar() # datatype of menu text
# clicked.set(options[0]) # set initial text
# drop = ttk.OptionMenu(frmMain, clicked, *options)
# drop.grid(row=2, column = 0, pady = 7)
# button = ttk.Button(frmMain, text=" ")
# label = ttk.Label(frmMain, text=" ")
# label.grid(row=3, column = 0, pady = 7)

# # button to send data and run prerecorded.py
# draw = ttk.Button(frmMain, text="Draw", command=draw_spiro)
# draw.grid(row=4, column = 0, pady = 7)

# download music 
def displayArtists():
    name = songName.get(1.0, "end-1c")
    artists = ""
    global RESULTS
    RESULTS = sp.search(name, limit=5)

    for i, track in enumerate(RESULTS["tracks"]["items"]):
        artists += f"[{i}] {track['name']} by {track['artists'][0]['name']}\n"
    
    artistNames.config(text = artists)

def getFeatures():
    id = int(artistID.get(1.0, "end-1c"))
    id = RESULTS["tracks"]["items"][id]["id"]
    results = sp.audio_features(id)
    global features
    i = 0
    for feature in ["danceability", "key", "loudness", "mode",\
        "acousticness", "instrumentalness", "liveness", "valence", \
        "tempo"]:
        features.append(int(results[0][feature]))
    visualizeMusic(features)

def visualizeMusic(features):
    # run prerecorded with features
    prerecorded.draw(features[0], features[1], features[2])
    prerecorded.draw(features[3], features[4], features[5])
    prerecorded.draw(features[6], features[7], features[8])

# song name instructions
songInstructions = ttk.Label(frmMain, 
                            text="Type the name of the song you want to visualize and click search song!",
                            font=("Arial", 12),
                            wraplength=500,
                            justify="center")
songInstructions.grid(row=5, column = 0, pady = 7)
# text input
songName = tk.Text(frmMain, height=5, width=40)
songName.grid(row=6, column = 0, pady = 7)
# button to search name of song
searchName = ttk.Button(frmMain, text="Search Song", command=displayArtists)
searchName.grid(row=7, column = 0, pady = 7)

# artist name instructions
artistInstructions = ttk.Label(frmMain, 
                                text="Once the list of songs appears, type the number corresponding to the song you want and click done!",
                                font=("Arial", 12),
                                wraplength=500,
                                justify="center")
artistInstructions.grid(row=8, column = 0, pady = 7)
# label for artist names
artistNames = ttk.Label(frmMain, text="")
artistNames.grid(row=9, column = 0, pady = 7)

# artist text input
artistID = tk.Text(frmMain, height=5, width=40)
artistID.grid(row=10, column = 0, pady = 7)
# button to search name of song
download = ttk.Button(frmMain, text="Done", command=getFeatures)
download.grid(row=11, column = 0, pady = 7)


root.mainloop()