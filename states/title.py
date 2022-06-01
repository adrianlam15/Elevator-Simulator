import pygame
from state import state
from game_state import main_game


class title(state):
    def __init__(self, game, surface):
        super().__init__(self, game, surface)
        self.actions = {"Start": False, "Quit": False}

    def update(self):
        if self.actions["Start"]:
            next_state = main_game(self.game)
            next_state.enter_state()
        elif self.actions["Quit"]:
            if len(self.game.state_stack) == 1:
                self.exit_state()
                exit()

    def render(self, surface):
        surface.blit(self.surface, ("COORDS"))
        pass
