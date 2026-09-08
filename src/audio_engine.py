import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

#default constants for audio quality
RATE = 48000
CHUNK = 4096

class AudioEngine:
    def __init__(self):
        self.layers = []   #array that stores layers
        self.current_layer = []
        self.state = "idle" #state shows what is currently happening

    def begin_layer(self, mode): #recording starts
        self.current_layer = [] #clears current layer
        self.state = mode #sets state to either recording or overdub

    def finish_layer(self): #recording stops, audio starts playing
        print("Finished layer with", len(self.current_layer), "chunks")
        if self.current_layer:
            self.layers.append(self.current_layer.copy()) #adds finished layer to the list
        self.state = "playing"


    def start_recording_stream(self): #starts continuous recording stream (no breaks)
        self.stream = sd.InputStream(samplerate=RATE, channels=1, dtype='float32', blocksize=CHUNK, callback=self.record_callback)
        self.stream.start()

    def record_callback(self, indata,frames,time,status):
        if self.state in ("recording","overdub"):
            self.current_layer.append(indata.copy())


    def mix_layers(self): #combines each layer into one audio array
        if not self.layers:
            return None

        processed_layers = []

        for layer in self.layers:
            if len(layer) == 0:
                continue

            flat_chunks = [chunk.reshape(-1).astype('float32') for chunk in layer] #flatten chunks to 1D

            arr = np.concatenate(flat_chunks).astype('float32') #put in one large array
            processed_layers.append(arr)

        if not processed_layers:
            return None

        max_len = max(len(layer) for layer in processed_layers)

        padded = [np.pad(layer, (0, max_len - len(layer)), mode='constant') #keeps audio layers the same length
                  for layer in processed_layers]

        mixed = np.sum(padded, axis=0) #adds the layers
        mixed = np.clip(mixed, -1.0, 1.0) #clips audio

        return mixed.astype('float32')

    def play_loop(self): #plays mixed audio
        mixed = self.mix_layers()
        print("MIXED TYPE:", type(mixed))
        print("MIXED DTYPE:", mixed.dtype if hasattr(mixed, "dtype") else "NO DTYPE")
        print("MIXED SHAPE:", mixed.shape if hasattr(mixed, "shape") else "NO SHAPE")
        print("Playback samplerate: ", RATE)

        if mixed is not None:
            sd.play(mixed, RATE, blocking=False)

    def undo_last_layer(self):
        if self.layers:
            self.layers.pop()

    def save_layers(self, folder_path ="loops/saved"):
        for idx, layer in enumerate(self.layers):
            audio = np.concatenate(layer, axis=0)
            filename = f"{folder_path}/layer_{idx+1}.wav"
            write(filename, RATE, audio)