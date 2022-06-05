import pygame, os, json
from states.state import state_format
from states.game_state import main_game


class button(pygame.sprite.Sprite):
    def __init__(self, game, image_name):
        super().__init__()
        self.game = game
        self.image_name = image_name
        self.dir = os.path.join(self.game.asset_dir, "graphics", "UI")
        x_val, y_val = 672 / 2, 378 / 2
        if self.image_name == "Play-Key.png":
            self.x, self.y = x_val, y_val
            self.multiplier = 2
            self.val = "Play"
        elif self.image_name == "Quit-Key.png":
            self.x, self.y = x_val - 100, y_val
            self.multiplier = 1
            self.val = "Quit"
        else:
            self.x, self.y = 20, 28
            self.multiplier = 1
            self.val = "Sound"
        self.image = pygame.image.load(os.path.join(self.dir, self.image_name))
        self.image = pygame.transform.scale(
            self.image,
            (
                self.image.get_width() * self.multiplier,
                self.image.get_height() * self.multiplier,
            ),
        )
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, pushed):
        if pushed:
            self.image = pygame.image.load(
                os.path.join(self.dir, self.val + ".5-Key.png")
            )
            self.image = pygame.transform.scale(
                self.image,
                (
                    self.image.get_width() * self.multiplier,
                    self.image.get_height() * self.multiplier,
                ),
            )
            if self.val == "Sound":
                if self.game.sound_enabled == False:
                    self.image = pygame.image.load(
                        os.path.join(self.dir, self.val + ".5-Key.png")
                    )
                    self.image = pygame.transform.scale(
                        self.image,
                        (
                            self.image.get_width() * self.multiplier,
                            self.image.get_height() * self.multiplier,
                        ),
                    )
                else:
                    self.image = pygame.image.load(
                        os.path.join(self.dir, self.image_name)
                    )
                    self.image = pygame.transform.scale(
                        self.image,
                        (
                            self.image.get_width() * self.multiplier,
                            self.image.get_height() * self.multiplier,
                        ),
                    )
        else:
            if not self.val == "Sound":
                self.image = pygame.image.load(os.path.join(self.dir, self.image_name))
                self.image = pygame.transform.scale(
                    self.image,
                    (
                        self.image.get_width() * self.multiplier,
                        self.image.get_height() * self.multiplier,
                    ),
                )


class title(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface((672, 378))
        self.surface.fill((40, 42, 54))

        # Testing spinning planet and list comprehension
        """self.planet_images = [
            "spritesheet_" + str(x) + ".png" for x in range(1, 32 + 1)
        ]
        self.x = 1
        self.image = pygame.image.load(
            os.path.join(
                self.game.asset_dir, "graphics", "Planet", self.planet_images[self.x]
            )
        )"""
        self.button_config = "button_coords.json"

        with open(self.button_config, "r") as input:
            self.data = json.load(input)
        input.close()
        self.button_group = []
        self.i = 1
        self.init_elem()

    def init_elem(self):
        self.music = pygame.mixer.Sound(
            os.path.join(self.game.asset_dir, "sounds", "menu_music.wav")
        )
        self.disc_text = pygame.font.Font(
            os.path.join(self.game.asset_dir, "fonts", "pressstart2p.ttf"), 20
        )
        proj_link = "Project can be found on GitHub at: https://github.com/adrianlam15/Elevator-Simulator"
        welcome = "Welcome to Elevator Simulator!"
        self.disc_text = self.disc_text.render(
            proj_link.ljust(len(proj_link) + 20) + welcome,
            True,
            "White",
        )
        self.disc_text_rect = self.disc_text.get_rect(topright=(0, 350))

        self.creator_text = pygame.font.SysFont("Arial", 12)
        self.creator_text = self.creator_text.render(
            "Made by Adrian Lam - 2022", True, (51, 51, 51)
        )

        self.creator_text_rect = self.creator_text.get_rect(topright=(672, 0))
        self.bottom_bar = pygame.Rect(0, 340, 672, 378)

        for elem in self.data["frames"]["Main Menu Buttons"]:
            self.buttons = button(self.game, elem)
            self.button_group.append(self.buttons)
        self.button_group = pygame.sprite.Group(self.button_group)

    def button_collision_detection(self, actions):
        for self.button in self.button_group:
            if self.button.rect.collidepoint(self.game.mouse_pos) and actions["Click"]:
                if self.button.val == "Play":
                    self.game.actions["Play"] = True
                elif self.button.val == "Sound":
                    if self.game.sound_enabled == True:
                        self.game.sound_enabled = False
                    elif self.game.sound_enabled == False:
                        self.game.sound_enabled = True
                elif self.button.val == "Quit":
                    self.game.quit = True
                self.button.pushed = True
                self.button.update(self.button.pushed)
            if not actions["Click"]:
                self.button.pushed = False
                self.button.update(self.button.pushed)
                if self.game.quit == True:
                    exit()

    def music_enabled(self, sound_enabled, i):
        if sound_enabled and self.i == 1:
            self.music.play(1, 0, 500)
            self.i = 0
        elif sound_enabled == False and self.i == 0:
            self.music.stop()
            self.i += 1

    def update(self, actions):
        if actions["Click"]:
            self.button_collision_detection(actions)
        elif actions["Click"] == False:
            self.button_collision_detection(actions)
            if actions["Play"]:
                next_state = main_game(self.game)
                next_state.enter_state()
                self.music.stop()
                self.game.actions["Play"] = False
        self.music_enabled(self.game.sound_enabled, self.i)

        # updating frame of spinning planet
        """self.image = pygame.image.load(
            os.path.join(
                self.game.asset_dir,
                "graphics",
                "Planet",
                self.planet_images[self.x],
            )
        )
        if self.x < 32:
            self.x += 1
        if self.x == 32:
            self.x = 0"""
        if self.disc_text_rect.x > 672:
            self.disc_text_rect.x = -1800
        else:
            self.disc_text_rect.x += 3

    def render(self, surface):
        pygame.draw.rect(self.surface, (189, 147, 249), self.bottom_bar)
        self.surface.blit(self.disc_text, self.disc_text_rect)
        self.surface.blit(self.creator_text, self.creator_text_rect)
        self.button_group.draw(self.surface)
        surface.blit(self.surface, (0, 0))
