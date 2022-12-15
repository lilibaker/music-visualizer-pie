# music-visualizer-pie
*A way to visualize music*

## Description
The goal for this project was to use an xy-gantry and produce distinct art based on song input. To fulfill this goal, we developed a simple user interface using Tkinter. We then used the Spotify Web API to collect data on the songs chosen by the users. These values were used to generate points for three concentric spirographs, and the points were then sent to the CNC motorshield to control the gantry system.


## Getting Started

### Local Setup
1. Clone the repository.<br>
    `git clone https://github.com/lilibaker/music-visualizer-pie.git`
2. Navigate to the local repository using your terminal.<br>
    ex: `cd music-visualizer-pie`
3. Install the dependencies listed below if they are not already installed.

### Dependencies
To install all the required dependencies, enter the following line in your terminal: <br>
`pip install -r requirements.txt`

This project relies upon the following dependencies:
* Pyserial
* Spotipy
* Ttkthemes

### Executing program
To run this program, connect the laptop to a CNC motorshield as defined on our website. Then navigate to the Python folder by typing `cd Python` and type `python3 interface.py` in the command line. The user interface should appear with directions for generating the spirographs.


### Authors
Lili Baker, Anthony Costarelli, Jiayuan Liu, Malvina Clavering, and Stephanie Cho
