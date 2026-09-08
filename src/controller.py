import threading
import time
import sounddevice as sd
from audio_engine import AudioEngine

class Controller:
    def __init__(self, ui=None):
        self.engine = AudioEngine()
        self.ui = ui
        self.running = True

        # Start background audio loop thread
        self.thread = threading.Thread(target=self.audio_loop, daemon=True)
        self.thread.start()

    def audio_loop(self):

        print("audio loop started")
        #runs constantly in the background
        while self.running:
            try:
                state = self.engine.state
                print("audio_loop state:", state)

                if state in ("recording", "overdub"):
                    print("calling record_chunk")
                    self.engine.record_chunk()

                elif state == "playing":
                    try:
                        stream = sd.get_stream()
                        if stream is None or not stream.active:
                            print("starting playback...")
                            self.engine.play_loop()
                        else:
                            time.sleep(0.1) #breaks while playing back
                    except Exception:
                        print("starting playback failed")
                        self.engine.play_loop()

                else: #take breaks while idle
                    time.sleep(0.01)

            except Exception as e:
                print("audio loop error: ", e)



    def pedal_press(self): #when user hits space
        state = self.engine.state

        if state == "idle": #starts recording
            self.engine.begin_layer("recording")
            self.update_ui("Recording...")

        elif state == "recording": #stops recording and starts playing audio
            self.engine.finish_layer()
            self.update_ui("Playing...")

        elif state == "playing":  #stops playing and starts overdubbing
            self.engine.begin_layer("overdub")
            self.update_ui("Overdubbing...")

        elif state == "overdub":    #stops overdub and starts playing
            self.engine.finish_layer()
            self.update_ui("Playing...")

    def undo(self): #calls undo and removes layer
        self.engine.undo_last_layer()
        self.update_ui("Undo last layer")

    def save(self):  #calls save in engine and saves mix as wav file
        self.engine.save_layers()
        self.update_ui("Saved layers")

    def update_ui(self, text):
        if self.ui:
            self.ui.update_status(text)

    def stop(self):  #stops the thread
        self.running = False
