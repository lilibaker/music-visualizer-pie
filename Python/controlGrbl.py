import serial
import time
import sys
from threading import Event
import prerecorded

BAUD_RATE = 115200
WRITE_FILENAME_0 = "test_write_gcode_0.gcode"

POSITION_0 = [
    [0, 2],  
    [1, 3],
    [4, 4],
    [9, 5],
]

COLOR_OPTIONS = [i for i in range(0,6)]

#def scale_postion(raw_x, raw_y)

def draw_all_spirals(audio_features):
    # get points from audio features
    colors = []
    x_positions = []
    y_positions = []
    feature_index = 0
    for i in range(3):
        # scale and to get the mod 7 value to map to color
        color_value = audio_features[i] * 1000 % 7
        colors.append(color_value)
        curr_x, curr_y = prerecorded.draw(audio_features[feature_index], \
                        audio_features[feature_index+1], audio_features[feature_index+2])
        x_positions.append(curr_x)
        y_positions.append(curr_y)
        feature_index += 3
    for i in range(1, len(x_positions)):
        x_positions[i] = x_positions[i] - x_positions[i - 1]
        y_positions[i] = y_positions[i] - y_positions[i - 1]
    

def write_gcode(colors, x_positions, y_positions, write_filename):
    with open(write_filename, "w") as f:
        # write header
        header = """$$\n$X\nG21\nG28 G91\n"""
        f.write(header)
        # write x,y coordinates
        for i in range(len(x_positions)):
            # f.write(f"G01 Z{z}\n") -- figure out how much to turn to send to gcode
            for j in range(len(x_positions[i])):
                x = x_positions[1][j]
                y = y_positions[i][j]
                f.write(f"G01 X{x} Y{y}\n")


def send_wake_up(ser):
    # Wake up
    # Hit enter a few times to wake the Printrbot
    print("writing enter")
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)   # Wait for Printrbot to initialize
    ser.flushInput()  # Flush startup text in serial input

def wait_for_movement_completion(ser,line):

    Event().wait(2)

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


def stream_gcode(port,gcode_path):

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


if __name__ == "__main__":

    try:
        port, gcode_path = sys.argv[1:3]
    except (ValueError, IndexError):
        print("Error: Use like python controlGrbl.py ARDUINO_PORT test_grbl.gcode")
        sys.exit(1)

    print("USB Port: ", port)
    print("Gcode file: ", gcode_path)
    #write_gcode(POSITION_0, WRITE_FILENAME_0)
    stream_gcode(port, gcode_path)