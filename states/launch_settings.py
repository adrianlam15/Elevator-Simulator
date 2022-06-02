import pygame
from states.state import state_format
from states.title import title


class setting_state(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface((672, 378))
        self.select = {"Resolution": None, "Sound": False}

    def update(self, actions):
        if actions["Click"]:
            next_state = title(self.game)
            next_state.enter_state()
        self.game.reset_keys()

    def render(self, surface):
        surface.blit(self.surface, (0, 0))


class drop_down:
    def __init__(self, game):
        self.game = game
