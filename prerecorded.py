import pyaudio
import serial
import sys
import time
import wave

BAUD = 9600
BUFFER = 256

if __name__ == "__main__":
    try:
        port, audiofile = sys.argv[1]
    except ValueError:
        print("Error: Use like python microphone.py PORT, WAV_FILE")
        sys.exit(1)

    with wave.open(audiofile, "rb") as wav:
        data = wav.readframes(wav.getnframes())

    with serial.Serial(port, BAUD) as ser:
        i = 0
        while True:
            n = ser.write(data[i:i+BUFFER])

            i += n
            if n == 0:
                break