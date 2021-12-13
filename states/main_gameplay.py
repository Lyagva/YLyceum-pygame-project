import Map
import Player


class MainGameplay:
    def __init__(self, app):
        self.app = app

        # PLAYER
        self.player = Player.Player(self.app)

        # MAP
        self.map = Map.Map(self.app)

    def update(self):
        self.map.update()
        self.map.map_move((50 * self.app.clock.get_time() / 1000, 0))
        self.player.update()

    def render(self):
        # Map
        self.map.render()

        # Player
        self.player.render()