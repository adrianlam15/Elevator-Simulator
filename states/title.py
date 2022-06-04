import pygame, os
from states.state import state_format
from states.game_state import main_game


class title(state_format):
    def __init__(self, game):
        super().__init__(game)
        self.surface = pygame.Surface((672, 378))
        self.surface.fill("White")

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
        self.music = pygame.mixer.Sound(
            os.path.join(self.game.asset_dir, "sounds", "menu_music.wav")
        )
        self.music.play(1, 0, 500)
        self.disc_text = pygame.font.Font(
            os.path.join(self.game.asset_dir, "fonts", "fibberish.ttf"), 32
        )
        proj_link = "Project can be found on GitHub at: https://github.com/adrianlam15/Elevator-Simulator"
        welcome = "Welcome to Elevator Simulator!"
        self.disc_text = self.disc_text.render(
            proj_link.ljust(len(proj_link) + 20) + welcome,
            True,
            "White",
        )
        self.disc_text_rect = self.disc_text.get_rect(topright=(0, 345))

        self.creator_text = pygame.font.SysFont("Arial", 12)
        self.creator_text = self.creator_text.render(
            "Made by Adrian Lam - 2022", True, (51, 51, 51)
        )

        self.creator_text_rect = self.creator_text.get_rect(topright=(672, 0))
        self.bottom_bar = pygame.Rect(0, 340, 672, 378)

    def update(self, actions):
        if actions["Click"] is True:
            next_state = main_game(self.game)
            next_state.enter_state()
            self.music.stop()

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
        print(self.disc_text_rect.x)
        self.game.reset_keys()

    def render(self, surface):
        pygame.draw.rect(self.surface, "Black", self.bottom_bar)
        self.surface.blit(self.disc_text, self.disc_text_rect)
        self.surface.blit(self.creator_text, self.creator_text_rect)

        surface.blit(self.surface, (0, 0))
