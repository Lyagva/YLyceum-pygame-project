from Blocks import Block


class DangerBlock(Block):
    def __init__(self, app, map_arg, pos, image=None, damage=1, collide=True):
        super().__init__(app, map_arg, pos, image)

        self.type = "danger_block"
        self.is_collide = collide
        self.damage = damage
