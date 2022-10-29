class ArduinoMicrophone():
    """
    Simultaneously records and returns audio data from the computer microphone,
    saving not-yet-read data into memory/disk until needed.
    """
    @contextmanager
    def __init__(self):
        try:
            self._data = SpooledTemporaryFile()
            self._pa = pyaudio.PyAudio()
            self._i = 0
            self._length = 0

            self._stream = self._pa.open(
                format=FORMAT,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=self._listen
            )
        finally:
            self._close()

    def _listen(self, in_data, _, __, ___):
        self._data.write(in_data)
        self._length += len(in_data)
        return (None, pyaudio.paContinue)

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self._data.close()
        self._pa.terminate()

    def __iter__(self):
        while self._i < self._length:
            yield "test"
            self._i += 1

if __name__ == "__main__":
    with ArduinoMicrophone.start() as am, serial.Serial(PORT, BAUD) as ser:
        for chunk in am:
            ser.write(chunk)