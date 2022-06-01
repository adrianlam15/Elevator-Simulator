import pygame
from states.state import state_format
from states.title import title


class setting_state(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface()
        self.select = {"Resolution": None, "Sound": False}
        self.actions = {"Start": False}

    def update(self):
        if self.actions["Start"]:
            next_state = title(self.game)
            next_state.enter_state()

    def render(self, surface):
        pass


class drop_down:
    def __init__(self, game):
        self.game = game
