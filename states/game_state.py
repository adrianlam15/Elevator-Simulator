import pygame
from states.state import state_format
from states.pause_menu import paused


class main_game(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface((672, 378))
        self.surface.fill("Black")

    def update(self, actions):
        if actions["Pause"]:
            next_state = paused(self.game)
            next_state.enter_state()
        """self.elevator = elevator(self.game)
        self.elevator.update()"""
        self.game.reset_keys()

        # elevator velocity changes go here

    def render(self, surface):
        surface.blit(self.surface, (0, 0))


class elevator:
    def __init__(self, game):
        self.game = game
        self.image = ""
        self.surface = ""
        self.rect = ""
        self.direction = {"Up": False, "Down": False}
        self.door_state = {"Open": False, "Closed": True}

    def update(self):
        if self.direction["Up"] is True:
            self.direction["Down"] = False
        elif self.direction["Down"] is True:
            self.direction["Up"] = False
        if self.door_state["Open"] is True:
            self.door_state["Closed"] = False
        elif self.door_state["Open"] is False:
            self.door_state["Closeded"] = True
        if self.door_state["Open"] is True:
            for keys in self.direction.keys():
                self.direction[keys] = False
        print(self.direction)
