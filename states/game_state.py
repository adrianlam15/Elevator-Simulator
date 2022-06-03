import pygame, os, json, time
from states.state import state_format
from states.pause_menu import paused


class main_game(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface((672, 378))
        self.surface.fill("White")
        self.elevator = elevator(self.game, True, self.surface)

    def update(self, actions):
        if actions["Pause"]:
            next_state = paused(self.game)
            next_state.enter_state()
        self.elevator.update()
        self.game.reset_keys()

        # elevator velocity changes go here

    def render(self, surface):
        self.elevator.render(self.surface)
        surface.blit(self.surface, (0, 0))


class button(pygame.sprite.Sprite):
    def __init__(self, elevator, game, file):
        super().__init__()
        self.elevator = elevator
        self.game = game
        self.file = file
        self.dir = os.path.join("assets", "graphics", "Keys")

    def get_button(self, x, y, w, h):
        button = pygame.Surface((w, h))
        button.set_colorkey((0, 0, 0))
        button.blit(self.image, (0, 0), (x, y, w, h))
        self.rect = button.get_rect(topleft=(0, 0))
        print(self.rect)
        return button

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
        self.button_surface = pygame.Surface((672, 378))
        self.button_config = "button_coords.json"
        self.button_group = []
        self.button_click_group = []
        with open(self.button_config, "r") as input:
            self.data = json.load(input)
        input.close()
        for elem in self.data["frames"]:
            buttons = button(self, self.game, self.button_config)
            buttons.button_val = elem[0]
            buttons.x, buttons.y, buttons.w, buttons.h = (
                self.data["frames"][elem]["coords"]["x"],
                self.data["frames"][elem]["coords"]["y"],
                self.data["frames"][elem]["coords"]["w"],
                self.data["frames"][elem]["coords"]["h"],
            )

            buttons.image = pygame.image.load(os.path.join(buttons.dir, elem))
            if self.service:
                """buttons.surface = pygame.Surface((buttons.w, buttons.h))"""
                buttons.get_button(buttons.x, buttons.y, buttons.w, buttons.h)
            else:
                if elem == "S-Key.png":
                    break
                buttons.get_button(buttons.x, buttons.y, buttons.w, buttons.h)
            if elem[2] == "5":
                self.button_click_group.append(buttons)
                print("Added click")
            else:
                self.button_group.append(buttons)
                print("Added")

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

    def render(self, surface):
        surface.blit()
