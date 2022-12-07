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
    # keep track of the index of the current feature
    feature_index = 0

    # for each of the three desired spirals, get the positions
    for i in range(3):
        # # scale and to get the mod 7 value to map to color
        # color_value = audio_features[i] * 1000 % 7
        # # add the corresponding color number
        # colors.append(color_value)
        # get a list representing x absolute positions and a list of 
        # y absolute positions using prerecorded.draw
        curr_x, curr_y = prerecorded.draw(audio_features[feature_index], \
                        audio_features[feature_index+1], audio_features[feature_index+2])
        # add the list of positions to thep predefined lists
        x_positions.append(curr_x)
        y_positions.append(curr_y)
        # update feature index to account for the three features already used
        feature_index += 3
    
    # change the positions to be relative by subtracting previous position from current position
    # store temp positions
    temp_x_2 = x_positions[1][0]
    temp_y_2 = y_positions[1][0]
    temp_x_3 = x_positions[2][0]
    temp_y_3 = y_positions[2][0]
    # calculate relatvie positions for each first point in the spirals
    x_positions[1][0] = x_positions[1][0] - x_positions[0][-1]
    y_positions[1][0] = y_positions[1][0] - y_positions[0][-1]
    x_positions[2][0] = x_positions[2][0] - x_positions[1][-1]
    y_positions[2][0] = y_positions[2][0] - y_positions[1][-1]
    for i in range(3):
        # x_positions[i].append(x_positions[i][0])
        # y_positions[i].append(y_positions[i][0])
        
        for j in range(1, len(x_positions)):
            if j == 1:
                if i == 1:
                    x_positions[i][j] = temp_x_2
                    y_positions[i][j] = temp_y_2
                else:
                    x_positions[i][j] = temp_x_3
                    y_positions[i][j] = temp_y_3
            else:
                x_positions[i][j] = x_positions[i][j] - x_positions[i][j-1]
                y_positions[i][j] = y_positions[i][j] - y_positions[i][j-1]
    
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

            # for the current spiral, loop through each position and write required
            # movement to file
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


# if __name__ == "__main__":
#     print("called")
#     try:
#         port, gcode_path, features = sys.argv[1:4]
#     except (ValueError, IndexError):
#         print("Error: Use like python controlGrbl.py ARDUINO_PORT test_grbl.gcode features")
#         sys.exit(1)

#     print("USB Port: ", port)
#     print("Gcode file: ", gcode_path)
#     print("Features: ", features)
#     # get_spiral_positions(features)
#     #write_gcode(POSITION_0, WRITE_FILENAME_0)
#     stream_gcode(port, gcode_path)

def run_grbl(port, gcode_path, features):
    print("USB Port: ", port)
    print("Gcode file: ", gcode_path)
    print("Features: ", features)
    # get_spiral_positions(features)
    #write_gcode(POSITION_0, WRITE_FILENAME_0)
    x, y = get_spiral_positions(features)
    write_gcode(x, y, gcode_path)
    stream_gcode(port, gcode_path)

# stream_gcode('COM5', "row row row your boat.gcode")
# stream_gcode('COM5', "test_grbl.gcode")
# stream_gcode('COM5', "gcode_files\yesterday.gcode")