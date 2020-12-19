import os
import subprocess  # nosec


class Player:
    def __init__(self, song, power_state):
        if song is not None and not os.path.isfile(song):
            raise ValueError("File does not exist: %s" % song)
        self.path = song
        self.player = None
        self.power_state = power_state
        self.power_state.callbacks.append(self.toggle)

    def toggle(self, value):
        if value:
            self.play()
        else:
            self.stop()

    def play(self):
        if self.path and self.player is None and self.power_state:
            self.player = subprocess.Popen(  # nosec
                ["ffplay", "-loop", "0", "-loglevel", "24", self.path]
            )

    def stop(self):
        if self.player is not None:
            self.player.terminate()
            self.player = None
