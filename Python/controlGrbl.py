import serial
import time
import sys
from threading import Event
import prerecorded

BAUD_RATE = 115200

# sample positions
WRITE_FILENAME_0 = "test_write_gcode_0.gcode"

POSITION_0 = [
    [0, 2],
    [1, 3],
    [4, 4],
    [9, 5],
]

def get_spiral_positions(audio_features):
    """
    Get all of the relative positions for gantry movement.

    Args:
        audio_features: A list of floats represening audio features
            found through spotify api.
    """
    # get colors and points from audio features
    # set up lists
    colors = []
    x_positions = []
    y_positions = []
    
    audio_features = list(sorted(audio_features))

    # generate first spiral
    curr_x, curr_y = prerecorded.draw(audio_features[0], \
                        audio_features[2], audio_features[1])
    # add the list of positions to the predefined lists
    x_positions.extend(curr_x)
    y_positions.extend(curr_y)

    # generate second spiral
    curr_x, curr_y = prerecorded.draw(audio_features[3], \
                        audio_features[5], audio_features[4])
    # add the list of positions to the predefined lists
    x_positions.extend(curr_x)
    y_positions.extend(curr_y)

    # generate third spiral
    curr_x, curr_y = prerecorded.draw(audio_features[6], \
                        audio_features[8], audio_features[7])
    # add the list of positions to the predefined lists
    x_positions.extend(curr_x)
    y_positions.extend(curr_y)
    
    # get relative position of each point by subtarcting previous position for gcode
    # normalize the points and then scale for the rage of drawing area
    x_positions = [325 * (x_positions[i] - x_positions[i-1]) / prerecorded.norm(x_positions) for i in range(1, len(x_positions))]
    y_positions = [325 * (y_positions[i] - y_positions[i-1]) / prerecorded.norm(y_positions) for i in range(1, len(y_positions))]

    return x_positions, y_positions


def write_gcode(x_positions, y_positions, write_filename, colors=[]):
    """
    Create the gcode file based on the positions and colors.

    Args:
        colors: A list of integers representing desired color for each spiral.
        x_positions: A list of lists containing floats with relative positions
            for x stepper.
        y_positions: A list of lists containing floats with relative positions
            for y stepper.
        write_filename: A string with the desired name for the gcode file.
    """
    # crreate and write to a new gcode file
    with open(write_filename, "w") as f:
        # write header needed gcode that uses metric units and relative positions
        header = """$$\nG21 G91\n"""
        f.write(header)
        # write colors and positions needed for each of the three spirals
        # loop through each spiral
        for i in range(len(x_positions)):
            # for the current spiral, write the movement needed for desired color
            # f.write(f"G01 Z{z}\n") -- figure out how much to turn to send to gcode

            # loop through each position and write required movement to file
            x = x_positions[i]
            y = y_positions[i]
            f.write(f"G01 X{x} Y{y} F100\n")


def send_wake_up(ser):
    """
    TODO: Add docstring
    """
    # Wake up
    # Hit enter a few times to wake the Printrbot
    print("writing enter")
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)   # Wait for Printrbot to initialize
    ser.flushInput()  # Flush startup text in serial input

def wait_for_movement_completion(ser,line):
    """
    TODO: Add docstring
    """

    Event().wait(1)

    if line != '$X' or '$$':

        idle_counter = 0

        while True:

            # Event().wait(0.01)
            ser.reset_input_buffer()
            command = str.encode('?' + '\n')
            ser.write(command)
            grbl_out = ser.readline()
            grbl_response = grbl_out.strip().decode('utf-8')

            if grbl_response != 'ok':

                if grbl_response.find('Idle') > 0:
                    idle_counter += 1

            if idle_counter > 10:
                break
    return


def stream_gcode(port, gcode_path):
    """
    TODO: Add docstring
    """

    ser = serial.Serial(port, BAUD_RATE)
    #send_wake_up(ser)

    with open(gcode_path, "r") as file:
        lines = file.readlines()

    for raw_line in lines:
        line = raw_line.strip()
        print("Sending gcode: " + line)

        # converts string to byte encoded string and append newline
        command = str.encode(line + '\n')
        ser.write(command)  # Send g-code

        wait_for_movement_completion(ser,line)

        grbl_out = ser.readline()  # Wait for response with carriage return
        print(" : " , grbl_out.strip().decode('utf-8'))

    print('End of gcode')


def run_grbl(port, gcode_path, features):
    """
    TODO: Add docstring
    """
    print("USB Port: ", port)
    print("Gcode file: ", gcode_path)
    print("Features: ", features)
    # get_spiral_positions(features)
    #write_gcode(POSITION_0, WRITE_FILENAME_0)
    x, y = get_spiral_positions(features)
    write_gcode(x, y, gcode_path)
    # stream_gcode(port, gcode_path)
    print("Done")