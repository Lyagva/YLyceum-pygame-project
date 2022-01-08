# Sound

import pygame as pg


class Sound:
    def __init__(self, file_path, volume=100):
        self.audio = pg.mixer.Sound(file_path)
        self.volume = volume / 100

    def play(self):
        self.audio.play()

    def stop(self):
        self.audio.stop()