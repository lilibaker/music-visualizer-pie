import serial
import time
import sys
from threading import Event
import prerecorded

# baud rate for serial communication
BAUD_RATE = 115200

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

    # sort the values of audio_features in ascending order
    audio_features = list(sorted(audio_features))

    # generate first spiral
    curr_x, curr_y = prerecorded.draw(audio_features[0], \
                        audio_features[2], audio_features[1])
    # add the list of positions to the predefined lists
    x_positions.extend(curr_x)
    y_positions.extend(curr_y)
    # add color for first spiral
    first_color_value = int(audio_features[1] * 1000 % 7)
    colors.append(first_color_value)

    # generate second spiral
    curr_x, curr_y = prerecorded.draw(audio_features[3], \
                        audio_features[5], audio_features[4])
    # add the list of positions to the predefined lists
    x_positions.extend(curr_x)
    y_positions.extend(curr_y)
    # add color for first spiral
    second_color_value = int(audio_features[4] * 1000 % 7)
    colors.append(second_color_value)

    # generate third spiral
    curr_x, curr_y = prerecorded.draw(audio_features[6], \
                        audio_features[8], audio_features[7])
    # add the list of positions to the predefined lists
    x_positions.extend(curr_x)
    y_positions.extend(curr_y)
    # add color for first spiral
    third_color_value = int(audio_features[7] * 1000 % 7)
    colors.append(third_color_value)

    # get relative position of each point by subtarcting previous position for gcode
    # normalize the points and then scale for the rage of drawing area
    x_positions = [167.5 * (x_positions[i] - x_positions[i-1]) / max(x_positions) for i in range(1, len(x_positions))]
    y_positions = [167.5 * (y_positions[i] - y_positions[i-1]) / max(y_positions) for i in range(1, len(y_positions))]

    # seperate into three lists so there is one list per spiral for later color changing
    x_positions = [x_positions[0:1000], x_positions[1000:2000], x_positions[2000:3000]]
    y_positions = [y_positions[0:1000], y_positions[1000:2000], y_positions[2000:3000]]
    
    return x_positions, y_positions, colors


def write_gcode(x_positions, y_positions, colors, write_filename):
    """
    Create the gcode file based on the positions and colors.

    Args:
        x_positions: A list of lists containing floats with relative positions
            for x stepper.
        y_positions: A list of lists containing floats with relative positions
            for y stepper.
        colors: A list of integers representing desired color for each spiral.
        write_filename: A string with the desired name for the gcode file.
    """
    # create and write to a new gcode file
    with open(write_filename, "w") as f:
        # write header needed gcode that uses metric units and relative positions
        header = """$$\nG21 G91\n"""
        f.write(header)
        # write colors and positions needed for each of the three spirals
        # loop through each spiral
        for i in range(len(x_positions)):
            # for the current spiral, write the movement needed for desired color
            z = colors[i]
            f.write(f"G01 Z{z} F100\n")

            # loop through each position in each spiral and write required movement to file
            for j in range(len(x_positions[i])):
                x = x_positions[i][j]
                y = y_positions[i][j]
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
    Get positions, generate gcode file, and send file to grbl
    to run the stepper motors.

    Args:
        port: A string represnting the COM port for serial communication.
        gcode_path: A string representing the file path for where
            to save the gcode file.
        features: A list of floats representing the audio features of the
            song obtained from the spotify api.
    """
    print("USB Port: ", port)
    print("Gcode file: ", gcode_path)
    print("Features: ", features)
    x, y, colors = get_spiral_positions(features)
    write_gcode(x, y, colors, gcode_path)
    # stream_gcode(port, gcode_path)
    print(colors)
    print("Done")