import pygame, os, json, time
from states.state import state_format
from states.pause_menu import paused


class main_game(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface((672, 378))
        self.surface.fill("White")
        self.elevator1 = elevator(self.game, True, self.surface)
        self.elevator2 = elevator(self.game, False, self.surface)

    def update(self, actions):
        if actions["Pause"]:
            next_state = paused(self.game)
            next_state.enter_state()

        self.elevator1.update(actions)
        self.game.reset_keys()

        # elevator velocity changes go here

    def render(self, surface):
        self.elevator1.render(self.surface)
        surface.blit(self.surface, (0, 0))


class button(pygame.sprite.Sprite):
    def __init__(self, elevator, game, file, x, y):
        super().__init__()
        self.elevator = elevator
        self.game = game
        self.file = file
        self.x, self.y = x, y
        self.dir = os.path.join("assets", "graphics", "Keys")

    def update(self, action):
        if action["Clicked"]:
            pass

    def render(self, surface):
        surface.blit()
        pass


class elevator:
    def __init__(self, game, service, surface):
        self.game = game
        self.image = ""
        self.service = service
        self.surface = surface  # temp
        self.rect = self.surface.get_rect()
        self.direction = {"Up": False, "Down": False}
        self.door_state = {"Open": False, "Closed": True}
        self.curr_floor = {
            "1": True,
            "2": False,
            "3": False,
            "4": False,
            "5": False,
            "6": False,
        }
        self.button_config = "button_coords.json"
        self.button_group = []
        with open(self.button_config, "r") as input:
            self.data = json.load(input)
        input.close()

    def update(self, actions):
        self.button_update()
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

    def button_update(self):
        for elem in self.data["frames"]:
            x, y = 200, 200
            buttons = button(self, self.game, self.button_config, x, y)
            print(x)
            buttons.button_val = elem[0]
            buttons.w, buttons.h = (
                self.data["frames"][elem]["size"]["w"],
                self.data["frames"][elem]["size"]["h"],
            )
            buttons.image = pygame.image.load(os.path.join(buttons.dir, elem))
            if self.service:
                buttons.image = pygame.image.load(os.path.join(buttons.dir, elem))
            else:
                if elem == "S-Key.png":
                    break
                buttons.image = pygame.image.load(os.path.join(buttons.dir, elem))
            buttons.rect = buttons.image.get_rect(topleft=(buttons.x, buttons.y))
            self.button_group.append(buttons)
            x += 50
        self.button_group = pygame.sprite.Group(buttons)

    def render(self, surface):
        """self.buttons.draw(surface)"""
        pass
