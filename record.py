import pyaudio
import serial
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1

BAUD = 9600
BUFFER = 256

def listen(in_data, frame_count, time_info, status_flags):
    audio_data.extend(in_data)

    return (None, pyaudio.paContinue)

if __name__ == "__main__":
    try:
        arduino, audiofile = sys[1:]
    except:
        print("Error: Need to specify Arduino port, and optionally a test audio file.")
        sys.quit(1)

    pA = pyaudio.PyAudio()
    data = []

    if audiofile:
        with open(audiofile, "rb") as wav:
            data = wav.readframes(wav.getnframes())
    else:
        def listen(in_data, _, __, ___):
            data.extend(in_data)
            return (None, pyaudio.paContinue)
        
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=listen)
        stream.start_stream()

    with serial.Serial(arduino, BAUD) as ser:
        i = 0
        while True:
            n = ser.write(audio_data[audio_i + BUFFER])

            i += n
            if n == 0:
                break

    pA.terminate()