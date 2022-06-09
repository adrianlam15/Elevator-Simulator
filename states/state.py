# imports
import pygame


# state formats class
class state_format:  # used as base class for adding states
    # initializer function of class
    def __init__(self, game):  # takes game arg
        self.game = game  # easier to call attr from game class
        self.prev_state = None  # prev state

    # enter state function
    def enter_state(self):
        if len(self.game.state_stack) > 1:  # if length of state stack is bigger than 1
            self.prev_state = self.game.state_stack[
                -1
            ]  # sets prev state to last state stack elem
        self.game.state_stack.append(self)  # append self (state class)

    # exit state function
    def exit_state(self):
        self.game.state_stack.pop()  # pops last state / elem
