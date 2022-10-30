import pyaudio
import serial
import sys
import time
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

BAUD = 9600
BUFFER = 256

if __name__ == "__main__":
    try:
        port = sys.argv[1]
    except ValueError:
        print("Error: Use like python microphone.py ARDUINO_PORT")
        sys.exit(1)

    data = []
    def listen(in_data, _, __, ___):
        data.extend(in_data)
        return (None, pyaudio.paContinue)

    pA = pyaudio.PyAudio()
    stream = pA.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=listen)
    stream.start_stream()

    with serial.Serial(arduino, BAUD) as ser:
        i = 0
        while True:
            n = ser.write(data[i:i+BUFFER])

            i += n
            if n == 0:
                break

    pA.terminate()