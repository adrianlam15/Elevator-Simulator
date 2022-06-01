import pygame


class state_format:
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.surface = pygame.Surface((1280, 720))

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()

    def render(self):
        pass
