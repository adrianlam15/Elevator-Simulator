import pygame
from states.state import state_format


class paused(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface((672, 378))
        self.surface.fill("Red")

    def update(self, actions):
        if self.game.pause:
            print("Paused")
        else:
            print("Resume")
            self.game.state_stack.pop()

        self.game.reset_keys()

    def render(self, surface):
        surface.blit(self.surface, (0, 0))
