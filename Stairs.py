from Block import Block


class Stairs(Block):
    def __init__(self, app, map_arg, pos, image=None):
        super().__init__(app, map_arg, pos, image)
        self.type = "stairs"
