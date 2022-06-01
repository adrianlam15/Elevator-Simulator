import pygame
from state import state
from pause_menu import paused


class main_game(state):
    def __init__(self, game, surface):
        super().__init__(self, game, surface)
        self.action = {"Paused": False}
        self.surface = ""

    def update(self):
        if self.action["Paused"]:
            next_state = paused(self.game)
            next_state.enter_state()

        self.elevator = elevator(self.game)
        self.elevator.update()
        # elevator velocity changes go here

    def render(self, surface):
        surface.blit(self.surface, ("COORDS"))


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
