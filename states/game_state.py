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
        self.elevator1.button_init(300, 340)
        self.elevator2.button_init(364, 340)

    def update(self, actions):
        if actions["Pause"]:
            next_state = paused(self.game)
            next_state.enter_state()
        self.elevator1.update(actions)
        self.elevator2.update(actions)
        self.game.reset_keys()

        # elevator velocity changes go here

    def render(self, surface):
        surface.blit(self.surface, (0, 0))
        self.elevator1.render(self.surface)
        self.elevator2.render(self.surface)


class button(pygame.sprite.Sprite):
    def __init__(self, elevator, game, file, x, y, image):
        super().__init__()
        self.elevator = elevator
        self.game = game
        self.file = file
        self.x, self.y = x, y
        self.dir = os.path.join("assets", "graphics", "Keys")
        self.image = pygame.image.load(os.path.join(self.dir, image))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pushed = False

    def update(self, action, image, cooldown):
        if self.pushed == False:
            self.image = pygame.image.load(os.path.join(self.dir, image))

    def render(self, surface):
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

    def button_collision_detection(self):
        for self.button in self.button_group:
            if self.button.rect.collidepoint(self.game.mouse_pos):
                print("collisions")

    def update(self, actions):
        if actions["Click"]:
            self.button_collision_detection()

        """if actions["Click"]:
        self.button_collision_detection()"""
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

    def button_init(self, x=300, y=340):
        for elem in self.data["frames"]:
            if not self.service:
                print(self.service)
                if elem == "S-Key.png":
                    break
            self.buttons = button(self, self.game, self.button_config, x, y, elem)
            self.buttons.button_val = elem[0]
            self.buttons.w, self.buttons.h = (
                self.data["frames"][elem]["size"]["w"],
                self.data["frames"][elem]["size"]["h"],
            )
            y -= 30
            self.button_group.append(self.buttons)
        self.button_group = pygame.sprite.Group(self.button_group)

    def render(self, surface):
        self.button_group.draw(surface)
