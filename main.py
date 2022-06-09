# Adrian, Lam (705929)
# ICS4U Final Assignment: Elevator Simulator
# GitHub: https://github.com/adrianlam15/Elevator-Simulator
# 01-06-2022
#
# program desc:
# additional features:
# - states (title, main, paused)
# - .wav sound files have to be used because .mp3 and .ogg files
# contain errors when trying to load specified module
#
# proposed edits:

# imports
import pygame, time, os, json

# local imports
try:
    from states.title import title  # title module with 'title' class object
except ModuleNotFoundError as msg:  # catching exception messages
    msg = str(msg).lower()  # makes string lowercase
    print(
        f"Couldn't load modules; {msg}. Check path of modules."
    )  # shows user which modules can not be loaded/found
    exit()  # exit program

# game class
class Game:
    pygame.init()  # initialize pygame module

    # constructor for game class
    def __init__(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (
            672,
            378,
        )  # screen width and screen height
        self.running = True  # game state
        self.SCREEN = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )  # initialize window
        self.CAPTION = pygame.display.set_caption(
            "Elevator Simulator"
        )  # set caption of window
        self.FPS = 60  # FPS
        self.clock = pygame.time.Clock()
        self.dt, self.time_now, self.prev_time = (
            0,
            0,
            0,
        )  # delta time, current time, and previous time aspect // for framerate independence
        self.state_stack = []  # state stack of game
        self.actions = {
            "Click": False,
            "Pause": False,
            "Play": False,
        }  # possible actions detected from user
        self.pause = False  # pause state of game
        self.quit = False  # quit state
        self.sound_enabled = True  # sound is enabled by default
        self.load_asset()  # calls load asset function
        self.load_state()  # calls load state function

    # main loop function of game
    def main_loop(self):
        while self.running:
            self.get_event()  # gets events of user
            self.update()  # logic // update method
            self.render()  # rendering

            """For testing state stacking purposes"""
            # print(self.state_stack)

    # delta time function
    def delta_time(self):
        """For testing delta time"""
        # self.time_now = time.time()
        # self.dt = self.time_now - self.prev_time
        # self.dt *= self.FPS
        # self.prev_time = self.time_now
        pass

    # get event function of game
    def get_event(self):
        self.event = pygame.event.get()  # get events in self.event var

        # event handler
        for event in self.event:
            self.mouse_pos = pygame.mouse.get_pos()  # gets position of mouse
            if event.type == pygame.QUIT:  # if event is quit
                pygame.quit()  # quit pygame
            if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse button down is detected
                self.actions["Click"] = True  # set click to true
            if event.type == pygame.MOUSEBUTTONUP:  # if mouse button up is detected
                self.actions["Click"] = False  # set click to false

            # if state stack contains 2 states (title and main game)
            if len(self.state_stack) == 2:
                if event.type == pygame.KEYDOWN:  # if key down is detected
                    if event.key == pygame.K_ESCAPE:  # if escape key is detected
                        self.actions["Pause"] = True  # set pause to True
                        self.pause = True  # pause state
                        print("Paused")
                if event.type == pygame.KEYUP:  # if key up is detected
                    if event.key == pygame.K_ESCAPE:  # if escape key is detected
                        self.actions["Pause"] = False  # set pause to False

            # if state stack contains 3 states (title, main game, and pause menu)
            if len(self.state_stack) == 3:
                if event.type == pygame.KEYDOWN:  # if key down is detected
                    if event.key == pygame.K_ESCAPE:  # if escape key is detected
                        self.actions["Pause"] = True  # set pause to True
                        self.pause = False  # disables pause state

    # load asset function
    def load_asset(self):
        self.asset_dir = os.path.join("assets")  # directory of assets folder
        self.icon = pygame.image.load(
            os.path.join(self.asset_dir, "graphics", "icon.png")
        )  # loading icon image of program
        pygame.display.set_icon(self.icon)  # set icon of Program

    # load states function
    def load_state(self):
        self.title = title(self)  # assigning object Title state/class
        self.state_stack.append(
            self.title
        )  # adding Title state to state stack and putting it at the bottom of list [-1]

        # for future launch settings
        """self.launch_set = setting_state(self)
        self.state_stack.append(self.launch_set)"""

    # update function
    def update(self):
        self.state_stack[-1].update(
            self.actions
        )  # calls update function/method unique to each element in state stack

    # render function of game
    def render(self):
        self.state_stack[-1].render(
            self.SCREEN
        )  # calls render function/method unique to each element in state stack
        pygame.display.update()  # updates pygame display
        self.clock.tick(self.FPS)  # sets FPS of pygame display

    # reset keys function
    def reset_keys(self):
        # for each key in actions
        for keys in self.actions:
            self.actions[keys] = False  # set each key to False


# main program
game = Game()
if __name__ == "__main__":
    game.main_loop()  # calls main game loop function
