import pygame


class PercentageDisplay:
    def __init__(self, root: pygame.Surface, x: int, y: int, width: int, height: int, color: tuple[int, int, int],
                 text: str, font: pygame.font.SysFont = pygame.font.SysFont("comicsans", 40)):
        self.root = root
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.text, self.font = text, font

        self.value = 0

    def update(self, value: float):
        self.value = value

    def draw(self):
        pygame.draw.rect(self.root, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text + f"{self.value:.2f}%", 1, (255, 255, 255))
        self.root.blit(text, (self.x + self.width // 2 - text.get_width() // 2,
                              self.y + self.height // 2 - text.get_height() // 2))
