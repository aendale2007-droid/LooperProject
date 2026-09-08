import tkinter as tk

class LooperUI:
    def __init__(self, controller):
        self.controller = controller
        self.controller.ui = self  # attach UI to controller

        self.root = tk.Tk()
        self.root.title("Looper Pedal")
        self.root.geometry("400x250")
        self.root.configure(bg="#1e1e1e")

        #Status label
        self.status_label = tk.Label(
            self.root,
            text="Idle",
            font=("Arial", 18),
            fg="white",
            bg="#1e1e1e"
        )
        self.status_label.pack(pady=20)

        #layer count label
        self.layer_label = tk.Label(
            self.root,
            text="Layers: 0",
            font=("Arial", 14),
            fg="#cccccc",
            bg="#1e1e1e"
        )
        self.layer_label.pack(pady=10)

        #buttons
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=20)

        undo_btn = tk.Button(
            button_frame,
            text="Undo Last Layer",
            command=self.undo,
            width=15,
            bg="#444",
            fg="white"
        )
        undo_btn.grid(row=0, column=0, padx=10)

        save_btn = tk.Button(
            button_frame,
            text="Save Layers",
            command=self.save,
            width=15,
            bg="#444",
            fg="white"
        )
        save_btn.grid(row=0, column=1, padx=10)

        #binds spacebar to pedal (basically use space as the pedal)
        self.root.bind("<space>", self.spacebar_pressed)

    def spacebar_pressed(self, event):
        self.controller.pedal_press() #tells controller space/pedal has been pressed
        self.update_layer_count()

    def undo(self):
        self.controller.undo() #calls undo
        self.update_layer_count()

    def save(self):
        self.controller.save() #calls save function and saves file

    def update_status(self, text):
        self.status_label.config(text=text)

    def update_layer_count(self):
        count = len(self.controller.engine.layers)
        self.layer_label.config(text=f"Layers: {count}")

    def run(self):
        self.root.mainloop()
