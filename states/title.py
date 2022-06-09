# imports
import pygame, os, json
from states.state import state_format
from states.game_state import main_game

# buttons class
class button(pygame.sprite.Sprite):  # inherits from pygame.sprite.Sprite classes

    # initializer function of classes
    def __init__(self, game, image_name):
        super().__init__()  # inherit pygame Sprite attrs
        self.game = game  # makes game attrs available in button class
        self.image_name = image_name  # image_name attr
        self.dir = os.path.join(
            self.game.asset_dir, "graphics", "UI"
        )  # directory of UI graphics
        x_val, y_val = 672 / 2, 378 / 2  # x and y coords

        # setting coords of each button
        if self.image_name == "Play-Key.png":  # if image_name is "Play-Key.png"
            self.x, self.y = x_val, y_val  # sets x and y attrs of class
            self.multiplier = 2  # multiplier val used later for scaling button
            self.val = "Play"  # makes val attr of button equal to "Play"
        elif self.image_name == "Quit-Key.png":  # if image_name is "Quit"
            self.x, self.y = x_val - 100, y_val  # sets x and y attrs of class
            self.multiplier = 1  # multiplier val used later for scaling button
            self.val = "Quit"  # makes val attr of button equal to "Quit"
        else:  # if image_name is "Sound"
            self.x, self.y = 20, 28  # sets x and y attrs of class
            self.multiplier = 1  # multiplier val used later for scaling button
            self.val = "Sound"  # makes val attr of button equal to "Sound"

        # loading images and getting rect objects
        self.image = pygame.image.load(os.path.join(self.dir, self.image_name))
        self.image = pygame.transform.scale(
            self.image,
            (
                self.image.get_width() * self.multiplier,
                self.image.get_height() * self.multiplier,
            ),
        )  # scale image
        self.rect = self.image.get_rect(
            center=(self.x, self.y)
        )  # getting rect object of image attr

    # update function
    def update(self, pushed):
        # takes argument, "pushed", as bool
        if pushed:  # if button is pushed
            self.image = pygame.image.load(
                os.path.join(self.dir, self.val + ".5-Key.png")
            )  # sets button image
            self.image = pygame.transform.scale(
                self.image,
                (
                    self.image.get_width() * self.multiplier,
                    self.image.get_height() * self.multiplier,
                ),
            )  # scales button image
            if self.val == "Sound":  # if val attr is equal to "Sound"
                if self.game.sound_enabled == False:  # if sound is enabled
                    self.image = pygame.image.load(
                        os.path.join(self.dir, self.val + ".5-Key.png")
                    )  # sets buttom image to show user that music is enabled
                    self.image = pygame.transform.scale(
                        self.image,
                        (
                            self.image.get_width() * self.multiplier,
                            self.image.get_height() * self.multiplier,
                        ),
                    )  # scales button image
                else:
                    self.image = pygame.image.load(
                        os.path.join(self.dir, self.image_name)
                    )  # changes button image to show user that music has been disabled
                    self.image = pygame.transform.scale(
                        self.image,
                        (
                            self.image.get_width() * self.multiplier,
                            self.image.get_height() * self.multiplier,
                        ),
                    )  # scales button image
        else:  # if button is not pushed
            if not self.val == "Sound":  # if val attr is not "Sound"
                self.image = pygame.image.load(
                    os.path.join(self.dir, self.image_name)
                )  # sets image
                self.image = pygame.transform.scale(
                    self.image,
                    (
                        self.image.get_width() * self.multiplier,
                        self.image.get_height() * self.multiplier,
                    ),
                )  # scales image


# title class
class title(
    state_format
):  # inherits from state_format class found in states.state (states -> state.py)
    # initializer function of class
    def __init__(self, game):  # makes game attr available in class
        super().__init__(game)  # inherit from state_format class
        self.surface = pygame.Surface((672, 378))  # makes title surface
        self.surface.fill((40, 42, 54))  # fill surface with custom colour (40, 42, 54)
        self.button_config = (
            "button_coords.json"  # button config file (coords and names of pictures)
        )

        # open the button config file
        with open(
            self.button_config, "r"
        ) as input:  # open the button config file as input
            self.data = json.load(input)  # parse data
        input.close()  # closes file

        self.button_group = []  # button group attr for list of buttons
        self.init_elem()  # init elem function which is called to initalize elements in title screen
        self.i = 1  # instance of music

    # init elem function
    def init_elem(self):
        # sound
        self.music = pygame.mixer.Sound(
            os.path.join(self.game.asset_dir, "sounds", "menu_music.wav")
        )  # sets music (main menu)

        # texts and rect
        self.disc_text = pygame.font.Font(
            os.path.join(self.game.asset_dir, "fonts", "pressstart2p.ttf"), 20
        )  # font of text
        proj_link = "Project can be found on GitHub at: https://github.com/adrianlam15/Elevator-Simulator"  # github link :)
        welcome = "Welcome to Elevator Simulator!"  # welcome to elevator simulator
        self.disc_text = self.disc_text.render(
            proj_link.ljust(len(proj_link) + 20) + welcome,
            True,
            "White",
        )  # renders text as surface
        self.disc_text_rect = self.disc_text.get_rect(
            topright=(0, 350)
        )  # get rect object of text
        self.creator_text = pygame.font.SysFont("Arial", 12)  # font of creator text
        self.creator_text = self.creator_text.render(
            "Made by Adrian Lam - 2022", True, (51, 51, 51)
        )  # renders text as surface
        self.creator_text_rect = self.creator_text.get_rect(
            topright=(672, 0)
        )  # get rect object of creator text
        self.bottom_bar = pygame.Rect(
            0, 340, 672, 378
        )  # pygame Rect object // for purple bar at the bottom of screen

        # pulls dict from data file from json config file
        for elem in self.data["frames"][
            "Main Menu Buttons"
        ]:  # iterates through dict elements
            self.buttons = button(self.game, elem)  # makes button object
            self.button_group.append(self.buttons)  # adds button object to button group
        self.button_group = pygame.sprite.Group(
            self.button_group
        )  # makes button group a pygame Sprite group // easier for handling buttons

        # image and rects of main title
        self.image = pygame.image.load(
            os.path.join(self.game.asset_dir, "graphics", "UI", "main_title.png")
        )  # sets main title image
        self.image_rect = self.image.get_rect(
            midbottom=(672 / 2, 150)
        )  # gets rect object of main title image

    # button collision detection function
    def button_collision_detection(self, actions):  # takes game actions as arg
        for self.button in self.button_group:  # for buttons found in button group
            if (
                self.button.rect.collidepoint(self.game.mouse_pos) and actions["Click"]
            ):  # if there is collision between user mouse position and button rects
                if self.button.val == "Play":  # if the val of button is "Play"
                    self.game.actions["Play"] = True  # sets "Play" to true
                elif self.button.val == "Sound":  # if the val of button is "Sound"
                    if self.game.sound_enabled == True:  # if sound enabled is True
                        self.game.sound_enabled = False  # set sound enabled to False
                    elif self.game.sound_enabled == False:  # if sound enabled is False
                        self.game.sound_enabled = True  # set sound enabled to True
                elif self.button.val == "Quit":  # if the val of button is "Quit"
                    self.game.quit = True  # sets quit to True
                self.button.pushed = True  # sets pushed attr to True
                self.button.update(
                    self.button.pushed
                )  # calls button update function with self.button.pushed as arg (bool)
            if not actions["Click"]:  # if user does not click (for image animation)
                self.button.pushed = False  # sets pushed to False
                self.button.update(
                    self.button.pushed
                )  # calls button update function with self.button.pushed as arg (bool)
                if self.game.quit == True:  # if quit attr is True
                    exit()  # quit program

    # music enabled function !! USE PYGAME CHANNELS AND GET BUSY FUNCTION FOR FINDING IF AUDIO CHANNEL IS PLAYING / BUSY
    def music_enabled(self, sound_enabled):  # takes sound_enabled from Game class
        if sound_enabled and self.i == 1:  # if sound is enabled
            self.music.play(1, 0, 500)  # play music
            self.i = 0
        elif (
            sound_enabled == False and self.i == 0
        ):  # takes sound_enabled from Game class
            self.music.stop()
            self.i += 1

    # update function
    def update(self, actions):  # takes action arg from game class
        # if user has clicked
        if actions["Click"]:
            self.button_collision_detection(
                actions
            )  # call button collision detection function with actions arg (bool)

        # if user has not clicked
        elif actions["Click"] == False:
            self.button_collision_detection(
                actions
            )  # call button collision detection function with actions arg (bool)
            if actions["Play"]:  # if "Play" is True
                next_state = main_game(self.game)  # initializes main_game state
                next_state.enter_state()  # enter state (to append self to main state stack)
                self.music.stop()  # stops music
                self.game.actions["Play"] = False  # sets "Play" to False

        self.music_enabled(self.game.sound_enabled)  # calls music enabled function

        # updates rect.x position of texts // moving text
        if self.disc_text_rect.x > 672:  # if position of rect.x is bigger than 672
            self.disc_text_rect.x = (
                -2800
            )  # sets position of rect.x to -2800 (off screen)
        else:  # if position of rect.x is not bigger than 672
            self.disc_text_rect.x += 3  # updates rect.x position by 3

    # render function
    def render(self, surface):  # takes surface arg (main surface)
        # drawing commands
        pygame.draw.rect(
            self.surface, (189, 147, 249), self.bottom_bar
        )  # drawing rect at bottom of screen to title surface
        self.surface.blit(
            self.image, self.image_rect
        )  # blits title image and rect to title surface
        self.surface.blit(
            self.disc_text, self.disc_text_rect
        )  # blits fun texts and rect to title surface
        self.surface.blit(
            self.creator_text, self.creator_text_rect
        )  # blit creator texts and rect to title surface
        self.button_group.draw(self.surface)  # draws buttons to title surface
        surface.blit(self.surface, (0, 0))  # draws title surface to main game surface
