from state import state


class paused(state):
    def __init__(self, game, surface):
        super().__init__(self, game, surface)

    def update(self):
        pass

    def render(self, surface):
        surface.blit(self.surface, ("COORDS"))
