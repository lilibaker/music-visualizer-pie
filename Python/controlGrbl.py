import serial
import time
import sys
from threading import Event

BAUD_RATE = 115200

def send_wake_up(ser):
    # Wake up
    # Hit enter a few times to wake the Printrbot
    print("writing enter")
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)   # Wait for Printrbot to initialize
    ser.flushInput()  # Flush startup text in serial input

def wait_for_movement_completion(ser,line):

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

    #gcode_path = 'grbl_test.gcode'

    print("USB Port: ", port)
    print("Gcode file: ", gcode_path)
    stream_gcode(port, gcode_path)