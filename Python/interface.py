import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import prerecorded
import controlGrbl

sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id="ca4037574604402aa16cc9ead70aa2e3",
            client_secret="9b7ab94755874ebc8179da11926f68c3"
        )
    )

# define global veriables
name = ""
RESULTS = 0
features = []
options = []


# set up window with theme
root = ThemedTk(theme="breeze")
root.title("Music Visualizer")
root.geometry("800x800")
frmMain = tk.Frame(root)
frmMain.grid(row=0, column=0, sticky="")
frmMain.grid_rowconfigure(0, weight=1)
frmMain.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# add title to window
heading = ttk.Label(frmMain, text="Music Visualizer", font=("Arial", 25))
heading.grid(row=0, column = 0, pady = 7)

# set up dropdown for songs later
clicked = tk.StringVar() # datatype of menu text
clicked.set("Choose a song") # set initial text

# download music 
def displayArtists():
    """
    Display the first five songs that match the song the user enter in
    the text box.
    """
    # get the song name the user entered; should be a string
    global name 
    name = songName.get(1.0, "end-1c")

    # search the name of the song using spotify api
    global RESULTS
    RESULTS = sp.search(name, limit=5)

    # save the first five songs with artist names to options
    global options
    options.clear()
    for i, track in enumerate(RESULTS["tracks"]["items"]):
        options.append(f"[{i}] {track['name']} by {track['artists'][0]['name']}")
    
    # update screen
    updateScreen()

def updateScreen():
    """
    Update the screen to have a dropdown with list of songs and a button to draw.
    """
    
    # artist name instructions
    artistInstructions = ttk.Label(frmMain, 
                                    text="Once the list of songs appears, select the song you want and click done!",
                                    font=("Arial", 12),
                                    wraplength=500,
                                    justify="center")
    artistInstructions.grid(row=8, column = 0, pady = 7)

    # send artists to dropdown and display
    drop = ttk.OptionMenu(frmMain, clicked, options[0], *options)
    drop.grid(row=10, column = 0, pady = 7)
    button = ttk.Button(frmMain, text=" ")
    label = ttk.Label(frmMain, text=" ")
    label.grid(row=11, column = 0, pady = 7)
    
    # button to search name of song
    download = ttk.Button(frmMain, text="Done", command=getFeatures)
    download.grid(row=12, column = 0, pady = 7)

def getFeatures():
    """
    Get the audio features of the song the user choices and call the
    'visualizeMusic' function.
    """
    # get the id number associated with the song selected in the dropdown
    id = int(clicked.get()[1])
    id = RESULTS["tracks"]["items"][id]["id"]

    # use spotify api to get the audiofeatures of the song
    results = sp.audio_features(id)
    
    # store the values of the desired features in features
    global features
    i = 0
    for feature in ["danceability", "key", "loudness", "mode",\
        "acousticness", "instrumentalness", "liveness", "valence", \
        "energy"]:
        features.append(float(results[0][feature]))
    
    # call the visualize function
    visualizeMusic(features)

def visualizeMusic(features):
    """
    Use the feature values to visualize music. Calls the prerecorded.draw function.

    Parameters:
        features: Array of floats representing the song's feature values
            on a scale of 0 to 1.
    """

    # scale key so it is between 0 and 1; the normal range is -1 to 11
    features[1] = (features[1] + 1) / 12
    # scale loudness to 0 to 1; normal range is -60 to 0
    features[2] = features[2] * -1 / 60

    # draw with updated values
    controlGrbl.run_grbl("COM5", f"gcode_files\{name}.gcode", features)

# song name instructions
songInstructions = ttk.Label(frmMain, 
                            text="Type the name of the song you want to visualize and click search song!",
                            font=("Arial", 12),
                            wraplength=500,
                            justify="center")
songInstructions.grid(row=5, column = 0, pady = 7)

# text input for song
songName = tk.Text(frmMain, height=5, width=40)
songName.grid(row=6, column = 0, pady = 7)

# button to search name of song
searchName = ttk.Button(frmMain, text="Search Song", command=displayArtists)
searchName.grid(row=7, column = 0, pady = 7)

root.mainloop()