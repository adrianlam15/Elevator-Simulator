# imports
import pygame, time
from sprites import elevator

# game class
class Game:
    pygame.init()  # initialize pygame module

    # constructor for game class
    def __init__(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (
            500,
            400,
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

    # main loop funtion of game
    def main_loop(self):
        self.load_asset()
        while game.running:
            self.get_event()
            self.render()

    # delta time function
    def delta_time(self):
        self.time_now = time.time()
        self.dt = self.time_now - self.prev_time
        self.dt *= self.FPS
        self.prev_time = self.time_now

    # get event function of game
    def get_event(self):
        self.event = pygame.event.get()  # get events in self.event var
        for event in self.event:
            if event.type == pygame.QUIT:
                pygame.quit()
        pass

    def load_asset(self):
        self.elevator = elevator(self)

    # render function of game
    def render(self):
        self.state_stack[-1].render()
        pygame.display.update()
        self.clock.tick(self.FPS)


# main program
game = Game()
if __name__ == "__main__":
    game.main_loop()
