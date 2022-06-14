import pygame, os, json, time
from states.state import state_format
from states.pause_menu import paused

with open("button_coords.json", "r") as input:
    data = json.load(input)
input.close()


class main_game(state_format):
    def __init__(self, game):
        super().__init__(game)
        service = True
        pygame.mixer.set_num_channels(8)
        self.surface = pygame.Surface((672, 378))
        self.music = pygame.mixer.Sound(
            os.path.join(self.game.asset_dir, "sounds", "elevator_main.wav")
        )
        if self.game.sound_enabled:
            self.music.play(1, 0, 500)

        self.pole1 = pole(self.game, 164, 345)
        self.pole2 = pole(self.game, 532, 345)

        self.elevator_group = []

        self.elevator1 = elevator(self.game, True, 135, 300)
        self.elevator2 = elevator(self.game, False, 504, 300)
        self.elevator_group.append(self.elevator1)
        self.elevator_group.append(self.elevator2)
        self.elevator1.button_init(300, 340)
        self.elevator2.button_init(364, 340)

    def update(self, actions):
        if actions["Pause"]:
            next_state = paused(self.game)
            next_state.enter_state()
        self.elevator1.update(actions)
        self.elevator2.update(actions)

    def render(self, surface):
        self.surface.fill((40, 42, 54))
        self.surface.blit(self.pole1.image, self.pole1.rect)
        self.surface.blit(self.pole2.image, self.pole2.rect)

        self.elevator1.render(self.surface)
        self.elevator2.render(self.surface)
        surface.blit(self.surface, (0, 0))


class button(pygame.sprite.Sprite):
    def __init__(self, elevator, game, x, y, image, val):
        super().__init__()
        self.game = game
        self.x, self.y = x, y
        self.val = val
        self.dir = os.path.join("assets", "graphics", "Keys")
        self.butt = image
        self.image = pygame.image.load(os.path.join(self.dir, self.butt))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pushed = False
        self.button_sound = pygame.mixer.Channel(1)
        self.sound = pygame.mixer.Sound(
            os.path.join(self.game.asset_dir, "sounds", "button_sound.wav")
        )

    def update(self, pushed):
        if pushed:
            self.image = pygame.image.load(
                os.path.join(self.dir, self.val + ".5-Key.png")
            )
        else:
            self.image = pygame.image.load(os.path.join(self.dir, self.butt))

    def render(self, surface):
        pass


class pole:
    def __init__(self, game, x, y):
        self.game = game
        self.x, self.y = x, y
        self.image = pygame.image.load(
            os.path.join(self.game.asset_dir, "graphics", "elevator", "pole.png")
        )
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() * 2, self.image.get_height() * 2)
        )
        self.rect = self.image.get_rect(midbottom=(x, y))


class elevator:
    def __init__(self, game, service, x, y):
        self.game = game
        self.x, self.y = x, y
        self.images = []
        self.service = service
        self.direction = {"Up": False, "Down": False}
        self.door_state = {"Open": False}
        self.user_choice = {"Open": False}
        self.curr_floor = 1
        self.next_floor = 1
        self.button_group = []
        self.floor_queue = []
        self.time_now = 0
        self.open_time = 0
        if len(self.floor_queue) == 0:
            self.floor_queue.append(self.curr_floor)
        self.curr_frame = 0
        for image_name in data["frames"]["Elevator Pictures"]:
            img_load = pygame.image.load(
                os.path.join(self.game.asset_dir, "graphics", "elevator", image_name)
            )
            img_load = pygame.transform.scale(
                img_load, (img_load.get_width() * 2, img_load.get_height() * 2)
            )
            self.images.append(img_load)
        self.image = self.images[self.curr_frame]
        self.surface = pygame.Surface((img_load.get_width(), img_load.get_height()))
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.prev_y = self.rect.y

    def button_collision_detection(self, actions):
        for self.button in self.button_group:
            if self.button.rect.collidepoint(self.game.mouse_pos) and actions["Click"]:
                self.button.pushed = True
                self.button.update(self.button.pushed)
                """self.button.button_sound.play(self.button.sound)
                if not self.button.button_sound.get_busy():
                    print("Not played")"""
                try:
                    self.next_floor = int(self.button.val)
                except:
                    self.next_floor = 1
                if len(self.floor_queue) <= 10:
                    if self.floor_queue.count(self.next_floor) == 0:
                        self.floor_queue.append(self.next_floor)
                self.user_choice["Open"] = True
                print("Added to queue")
            if not actions["Click"]:
                self.button.pushed = False
                self.button.update(self.button.pushed)
                # self.user_choice["Open"] = False

    def update(self, actions):
        if actions["Click"]:
            self.button_collision_detection(actions)
        elif actions["Click"] == False:
            self.button_collision_detection(actions)

        if self.curr_frame == 0:
            if len(self.floor_queue) != 0:
                if self.floor_queue[0] == 1:
                    if self.rect.y != 300:
                        self.rect.y += 1
                        self.door_state["Open"] = False
                    elif self.rect.y == 300:
                        self.curr_floor = 1
                        if self.floor_queue.count(self.curr_floor) == 1:
                            self.floor_queue.remove(self.curr_floor)
                        self.door_state["Open"] = True
                elif self.floor_queue[0] == 2:
                    if self.rect.y > 254:
                        self.door_state["Open"] = False
                        self.rect.y -= 1
                    elif self.rect.y < 254:
                        self.rect.y += 1
                        self.door_state["Open"] = False
                    else:
                        self.curr_floor = 2
                        if self.floor_queue.count(self.curr_floor) == 1:
                            self.floor_queue.remove(self.curr_floor)
                        self.door_state["Open"] = True
                elif self.floor_queue[0] == 3:
                    if self.rect.y > 208:
                        self.rect.y -= 1
                        self.door_state["Open"] = False
                    elif self.rect.y < 208:
                        self.rect.y += 1
                        self.door_state["Open"] = False
                    else:
                        self.curr_floor = 3
                        if self.floor_queue.count(self.curr_floor) == 1:
                            self.floor_queue.remove(self.curr_floor)
                        self.door_state["Open"] = True
                elif self.floor_queue[0] == 4:
                    if self.rect.y > 162:
                        self.rect.y -= 1
                        self.door_state["Open"] = False
                    elif self.rect.y < 162:
                        self.rect.y += 1
                        self.door_state["Open"] = False
                    else:
                        self.curr_floor = 4
                        if self.floor_queue.count(self.curr_floor) == 1:
                            self.floor_queue.remove(self.curr_floor)
                        self.door_state["Open"] = True
                elif self.floor_queue[0] == 5:
                    if self.rect.y > 116:
                        self.rect.y -= 1
                        self.door_state["Open"] = False
                    elif self.rect.y < 116:
                        self.rect.y += 1
                        self.door_state["Open"] = False
                    else:
                        self.curr_floor = 5
                        if self.floor_queue.count(self.curr_floor) == 1:
                            self.floor_queue.remove(self.curr_floor)
                        self.door_state["Open"] = True
                elif self.floor_queue[0] == 6:
                    if self.rect.y > 69:
                        self.rect.y -= 1
                        self.door_state["Open"] = False
                    elif self.rect.y < 69:
                        self.rect.y += 1
                        self.door_state["Open"] = False
                    else:
                        self.curr_floor = 6
                        if self.floor_queue.count(self.curr_floor) == 1:
                            self.floor_queue.remove(self.curr_floor)
                        self.door_state["Open"] = True

        self.delta_time = pygame.time.get_ticks() - self.time_now
        if self.door_state["Open"] == True:
            if self.user_choice["Open"] == True:
                if self.curr_frame < 4:
                    if self.delta_time >= 400:
                        self.curr_frame += 1
                        self.time_now = pygame.time.get_ticks()
                        self.image = self.images[self.curr_frame]
                elif self.curr_frame == 4:
                    self.open_door_timer = pygame.time.get_ticks() - self.open_time
                    if self.open_door_timer >= 5000:
                        self.open_time = pygame.time.get_ticks()
                        self.time_now = pygame.time.get_ticks()
                        self.door_state["Open"] = False

        elif self.door_state["Open"] == False:
            self.delta_time = pygame.time.get_ticks() - self.time_now
            if self.delta_time >= 400:
                if self.curr_frame > 0:
                    self.curr_frame -= 1
                    self.open_time = pygame.time.get_ticks()
                    self.time_now = pygame.time.get_ticks()
                    self.image = self.images[self.curr_frame]
        # print(self.floor_queue)

    def button_init(self, x=300, y=340):
        for elem in data["frames"]["elevator buttons"]:
            if not self.service:
                print(self.service)
                if elem == "S-Key.png":
                    break
            val = elem[0]
            self.buttons = button(self, self.game, x, y, elem, val)
            self.buttons.w, self.buttons.h = (
                data["frames"]["elevator buttons"][elem]["size"]["w"],
                data["frames"]["elevator buttons"][elem]["size"]["h"],
            )
            y -= 30
            self.button_group.append(self.buttons)
        self.button_group = pygame.sprite.Group(self.button_group)

    def render(self, surface):
        surface.blit(self.image, self.rect)
        self.button_group.draw(surface)
