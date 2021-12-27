from Block import Block


class DangerBlock(Block):
    def __init__(self, app, map_arg, pos, image=None, damage=1):
        super().__init__(app, map_arg, pos, image)

        self.type = "danger_block"
        self.damage = damage
