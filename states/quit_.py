# Сосотяние выхода из игры

class Quit:
    def __init__(self, app):
        self.app = app

    def update(self):
        self.app.stop()

    def render(self):
        pass