import pygame


class buttons:
    pass


class elevator:
    def __init__(self, game):
        self.game = game
        self.image = ""
        self.surface = ""
        self.rect = ""
        self.direction = {"Up": False, "Down": False}
        self.door_state = {"Open": False, "Closed": True}

    def door_logic(self):
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
