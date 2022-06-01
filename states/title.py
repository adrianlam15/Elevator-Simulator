import pygame
from states.state import state_format
from states.game_state import main_game


class title(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface((672, 378))
        self.surface.fill("White")

    def update(self, actions):
        print(actions["Click"])
        if actions["Click"] is True:
            next_state = main_game(self.game)
            next_state.enter_state()
            print("Entered 2nd state.")
        self.game.reset_keys()

    def render(self, surface):
        surface.blit(self.surface, (0, 0))
