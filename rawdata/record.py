import pyaudio, wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream= p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")

stream.stop_stream()
stream.close()
p.terminate()

filename = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
filename.setnchannels(CHANNELS)
filename.setsampwidth(p.get_sample_size(FORMAT))
filename.setframerate(RATE)
filename.writeframes(b''.join(frames))
filename.close()


