import serial
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
    # use 107.5 as scale to maximize size; 56 for speed
    scale = 107.5
    x_positions = [scale * (x_positions[i] - x_positions[i-1]) / max(x_positions) for i in range(1, len(x_positions))]
    y_positions = [scale * (y_positions[i] - y_positions[i-1]) / max(y_positions) for i in range(1, len(y_positions))]

    # seperate into three lists so there is one list per spiral for later color changing
    # for less points uncomment this code
    x_positions = [x_positions[0:50], x_positions[50:100], x_positions[100:150]]
    y_positions = [y_positions[0:50], y_positions[50:100], y_positions[100:150]]
    # for more points, uncomment this code
    # x_positions = [x_positions[0:100], x_positions[100:200], x_positions[200:300]]
    # y_positions = [y_positions[0:100], y_positions[100:200], y_positions[200:300]]
    
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
            f.write(f"G01 Z{z} F1000\n")

            # loop through each position in each spiral and write required movement to file
            for j in range(len(x_positions[i])):
                x = x_positions[i][j]
                y = y_positions[i][j]
                f.write(f"G01 X{x} Y{y} F1000\n")


def wait_for_movement_completion(ser,line):
    """
    Wait for position command line to run while constantly checking status.

    Args: 
        ser: Serial object name.
        line: A string representing one of the gcode command line.
    """

    Event().wait(1)

    # for every position command line
    if line != '$X' or '$$':

        # initialize counter for status report
        idle_counter = 0

        while True:
            # flush serial input buffer
            ser.reset_input_buffer()
            # send grbl status status reporting request
            command = str.encode('?' + '\n')
            ser.write(command)

            # get grbl response line that ends with carriage return
            grbl_out = ser.readline()

            # decode and display grbl response
            grbl_response = grbl_out.strip().decode('utf-8')

            # pick out status report lines
            if grbl_response != 'ok':

                # keep counting status report times
                if grbl_response.find('Idle') > 0:
                    idle_counter += 1

            # finish waiting after getting 10 status reports
            if idle_counter > 10:
                break
    return


def stream_gcode(port, gcode_path):
    """
    Streaming gcode line by line through serial communication to grbl.

    Args:
        port: A string represnting the COM port for serial communication.
        gcode_path: A string representing the file path for where
        to save the gcode file. 
    """

    # create serial port object
    ser = serial.Serial(port, BAUD_RATE)

    # open generated gcode read all lines
    with open(gcode_path, "r") as file:
        lines = file.readlines()

    # clean up each line and display what the line is
    for raw_line in lines:
        line = raw_line.strip()
        print("Sending gcode: " + line)

        # converts string to byte encoded string and append newline
        command = str.encode(line + '\n')

        # Send g-code to grbl
        ser.write(command)  

        # wait for the line's command to execute and check status
        wait_for_movement_completion(ser,line)

        # get grbl response line that ends with carriage return
        grbl_out = ser.readline() 

        # decode and display grbl response
        print(" : " , grbl_out.strip().decode('utf-8'))

    # end of all lines in gcode file
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
    # display input port name, gcode file name, and features chosen
    print("USB Port: ", port)
    print("Gcode file: ", gcode_path)
    print("Features: ", features)

    # generate spiral points positions and colors list
    x, y, colors = get_spiral_positions(features)

    # generate gcode file
    write_gcode(x, y, colors, gcode_path)
    
    # stream gcode to grbl
    stream_gcode(port, gcode_path)

    print("Done")