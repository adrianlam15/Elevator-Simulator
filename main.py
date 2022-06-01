# imports
import pygame, time, os

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
            "Hello There!"
        )  # set caption of window
        self.FPS = 60  # FPS
        self.clock = pygame.time.Clock()
        self.dt, self.time_now, self.prev_time = (
            0,
            0,
            0,
        )  # delta time, current time, and previous time aspect // for framerate independence
        self.state_stack = []
        self.actions = {"Click": False, "Pause": False}
        self.pause = False
        self.load_asset()
        self.load_state()

    # main loop function of game
    def main_loop(self):
        while self.running:
            self.get_event()  # gets events of user
            self.update()  # logic // update method
            self.render()  # rendering

            """For testing state stacking purposes"""
            print(self.state_stack)

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
        for event in self.event:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.actions["Click"] = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.actions["Click"] = False
            if (
                len(self.state_stack) == 2
            ):  # if state stack contains 2 states (title and main game)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.actions["Pause"] = True
                        self.pause = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.actions["Pause"] = False
            if (
                len(self.state_stack) == 3
            ):  # if state stack contains 3 states (title, main game, and pause menu)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.actions["Pause"] = True
                        self.pause = False

    def load_asset(self):
        pass

    def load_state(self):
        self.title = title(self)
        self.state_stack.append(self.title)

        # for future launch settings
        """self.launch_set = setting_state(self)
        self.state_stack.append(self.launch_set)"""

    def update(self):
        self.state_stack[-1].update(self.actions)

    # render function of game
    def render(self):
        self.state_stack[-1].render(self.SCREEN)
        pygame.display.update()
        self.clock.tick(self.FPS)

    def reset_keys(self):
        for keys in self.actions:
            self.actions[keys] = False


# main program
game = Game()
if __name__ == "__main__":
    game.main_loop()
