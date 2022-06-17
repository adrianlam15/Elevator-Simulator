# imports and libraries
import pygame, os, json, time
from states.state import state_format
from states.pause_menu import paused

# read from .json file
with open("button_coords.json", "r") as input:
    data = json.load(input)  # parsing json
input.close()  # closes files


# main game state class
class main_game(state_format):
    # initializer function of class
    def __init__(self, game):
        super().__init__(game)
        # pygame.mixer.set_num_channels(8) // for testing
        self.surface = pygame.Surface((672, 378))  # making overall surface of the game
        self.music = pygame.mixer.Sound(
            os.path.join(self.game.asset_dir, "sounds", "elevator_main.wav")
        )  # setting default elevator music

        # setting game sound option // experimental
        if self.game.sound_enabled:
            self.music.play(1, 0, 500)  # loops the music

        # initializing game objects (e.g. pole and elevator)
        self.pole1 = pole(self.game, 164, 345)  # first pole
        self.pole2 = pole(self.game, 532, 345)  # second pole
        self.elevator1 = elevator(self.game, True, 135, 300)  # first elevator
        self.elevator2 = elevator(self.game, False, 504, 300)  # second elevator
        self.elevator1.button_init(300, 340)  # initalizes the buttons for each elevator
        self.elevator2.button_init(364, 340)  # initalizes the buttons for each elevator

    # update function
    def update(self, actions):  # takes actions as args
        if actions["Pause"]:  # if pause is True
            next_state = paused(self.game)  # adds the next state
            next_state.enter_state()  # updates to the state
        self.elevator1.update(actions)  # updates the elevator
        self.elevator2.update(actions)  # updates the elevator

    # render function
    def render(self, surface):  # takes main surface as args
        self.surface.fill((40, 42, 54))  # fills the surface with Dracula theme

        # render poles
        self.surface.blit(
            self.pole1.image, self.pole1.rect
        )  # renders pole 1 onto state surface
        self.surface.blit(
            self.pole2.image, self.pole2.rect
        )  # renders pole 2 onto state surface

        # render elevators
        self.elevator1.render(self.surface)  # renders elevator 1 onto state surface
        self.elevator2.render(self.surface)  # renders elevator 2 onto state surface
        surface.blit(self.surface, (0, 0))  # renders state surface onto main surface


# button classes
class button(pygame.sprite.Sprite):  # inherits from pygame Sprite class
    # initalizer function of class
    def __init__(self, elevator, game, x, y, image, val):  # args
        super().__init__()  # inherit attrs from superclass
        self.game = game  # takes main game class as args
        self.x, self.y = x, y  # x and y vals of button
        self.val = val  # val of button
        self.dir = os.path.join("assets", "graphics", "Keys")  # dir of assets
        self.butt = image  # image of buttons
        self.image = pygame.image.load(
            os.path.join(self.dir, self.butt)
        )  # loads pygame image of button
        self.rect = self.image.get_rect(topleft=(x, y))  # gets rect obj of pygame image
        self.pushed = False  # if button is pushed
        # self.button_sound = pygame.mixer.Channel(1) // experiemental
        """self.sound = pygame.mixer.Sound(
            os.path.join(self.game.asset_dir, "sounds", "button_sound.wav")
        )"""

    # update function of button
    def update(self, pushed):  # takes pushed as args
        if pushed:  # if button is pushed
            self.image = pygame.image.load(
                os.path.join(self.dir, self.val + ".5-Key.png")
            )  # loads pressed image
        else:  # if button is not pushed
            self.image = pygame.image.load(
                os.path.join(self.dir, self.butt)
            )  # loads unpressed image

    # render function // not currently needed or implemented
    def render(self, surface):
        pass


# pole class
class pole:
    # initalizer function
    def __init__(self, game, x, y):  # args of constructor
        self.game = game  # inherits game attrs
        self.x, self.y = x, y  # x and y val of pole
        self.image = pygame.image.load(
            os.path.join(self.game.asset_dir, "graphics", "elevator", "pole.png")
        )  # loads pole image
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() * 2, self.image.get_height() * 2)
        )  # scales the pole iamge up
        self.rect = self.image.get_rect(
            midbottom=(x, y)
        )  # gets rect obj of pygame image


# elevator class
class elevator:
    # initializer function for elevator class
    def __init__(self, game, service, x, y):  # args
        # attrs
        self.game = game  # inherits attrs from game object
        self.x, self.y = x, y  # x and y position of elevators
        self.images = []  # sets of images class elevator contains
        self.service = service  # bool val (if True or False)
        self.door_state = {"Open": False}  # door state of elevator
        self.user_choice = {"Open": False}  # user's choice of elevator state
        self.curr_floor = 1  # current floor of elevator
        self.next_floor = 1  # next floor of elevator
        self.button_group = []  # button group of elevator
        self.floor_queue = []  # floor queue of elevator
        self.time_now = 0  # current time of elevator
        self.open_time = 0  # current open time of elevator

        # appends floor 1 if floor queue is empty
        if len(self.floor_queue) == 0:
            self.floor_queue.append(self.curr_floor)

        # sets current image index of elevator
        self.curr_frame = 0

        # using for loop to open dict and get values
        for image_name in data["frames"]["Elevator Pictures"]:
            img_load = pygame.image.load(
                os.path.join(self.game.asset_dir, "graphics", "elevator", image_name)
            )  # loads pygame image of elevator state
            img_load = pygame.transform.scale(
                img_load, (img_load.get_width() * 2, img_load.get_height() * 2)
            )  # scales the pygame image up
            self.images.append(img_load)  # adds the image to the elevator image list

        self.image = self.images[self.curr_frame]  # current self image is loaded
        self.surface = pygame.Surface(
            (img_load.get_width(), img_load.get_height())
        )  # loads surface
        self.rect = self.surface.get_rect(topleft=(x, y))  # gets rect obj of surface

    # button collision detection function
    def button_collision_detection(self, actions):  # takes actions args
        for self.button in self.button_group:  # for buttons in button group
            # if mouse pos collides with button rect and click is true
            if self.button.rect.collidepoint(self.game.mouse_pos) and actions["Click"]:
                self.button.pushed = True  # sets button pushed to True
                self.button.update(self.button.pushed)  # calls update function
                """self.button.button_sound.play(self.button.sound)
                if not self.button.button_sound.get_busy():
                    print("Not played")"""
                try:
                    self.next_floor = int(self.button.val)
                except:
                    self.next_floor = 1

                # elevator queue
                if (
                    len(self.floor_queue) <= 10
                ):  # if elevator queue is less or equal to 10
                    if (
                        self.floor_queue.count(self.next_floor) == 0
                    ):  # if next floor is not already in list
                        self.floor_queue.append(
                            self.next_floor
                        )  # adds next floor to floor queue
                self.user_choice["Open"] = True  # user choice is open

            # if mouse is not clicked
            if not actions["Click"]:
                self.button.pushed = False  # sets button pushed to False
                self.button.update(
                    self.button.pushed
                )  # calls update function in button
                # self.user_choice["Open"] = False

    # update function
    def update(self, actions):  # takes actions args
        # if mouse is clicked
        if actions["Click"]:
            self.button_collision_detection(
                actions
            )  # calls button collision detection function with actions args

        # if mouse is not clicked
        elif actions["Click"] == False:
            self.button_collision_detection(
                actions
            )  # calls button collision detection function with actions args

        # moving elevators
        if self.curr_frame == 0:  # if self curr frame is 0
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

        # delta time
        self.delta_time = pygame.time.get_ticks() - self.time_now

        # opening of doors and updating pictures
        if self.door_state["Open"] == True:  # if door state is open
            if self.user_choice["Open"] == True:  # if user choice is open
                # if current frame is less than 4
                if self.curr_frame < 4:
                    # if it has been 400 ms or more
                    if self.delta_time >= 400:
                        self.curr_frame += 1  # add index +1
                        self.time_now = (
                            pygame.time.get_ticks()
                        )  # get time since pygame.init()
                        self.image = self.images[
                            self.curr_frame
                        ]  # current image indexing
                # if current frame is 4
                elif self.curr_frame == 4:
                    self.open_door_timer = (
                        pygame.time.get_ticks() - self.open_time
                    )  # delta time for staying open for 5000 ms
                    # if it has been 5000 ms or more
                    if self.open_door_timer >= 5000:
                        self.open_time = (
                            pygame.time.get_ticks()
                        )  # get time since pygame.init()
                        self.time_now = (
                            pygame.time.get_ticks()
                        )  # get time since pygame.init()
                        self.door_state["Open"] = False  # door state set to False

        # close door
        elif self.door_state["Open"] == False:
            # delta time
            self.delta_time = pygame.time.get_ticks() - self.time_now
            # if it has been 400 ms or more
            if self.delta_time >= 400:
                # if current frame is bigger than 0
                if self.curr_frame > 0:
                    self.curr_frame -= 1  # updates index -1
                    self.open_time = (
                        pygame.time.get_ticks()
                    )  # get time since pygame.init()
                    self.time_now = (
                        pygame.time.get_ticks()
                    )  # get time since pygame.init()
                    self.image = self.images[self.curr_frame]  # sets image using index
        # print(self.floor_queue)

    # button initializing function
    def button_init(self, x=300, y=340):  # uses x and y vals as args
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

    # render function
    def render(self, surface):
        surface.blit(self.image, self.rect)
        self.button_group.draw(surface)
