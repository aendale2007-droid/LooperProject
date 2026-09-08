from controller import Controller
from ui import LooperUI

if __name__ == "__main__":
    controller = Controller()
    ui = LooperUI(controller)
    ui.run()
