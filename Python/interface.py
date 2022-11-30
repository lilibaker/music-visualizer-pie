from tkinter import *
from tkinter import ttk
root = Tk()
root.title("Music Visualizer")
root.geometry("500x500")
style = ttk.Style()
style.theme_use('classic')

# add title
heading = Label(root, text="Music Visualizer")
heading.pack()

# Add instructions
instructions = Label(root, text="Choose a song to visualize from the dropdown below!")
instructions.pack()

# change label text
def show():
    label.config(text=clicked.get())

def draw_spiro():
    print("value is: " + clicked.get())
    

#dropdown options
options = [
    "1",
    "2",
    "3"
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

root.mainloop()