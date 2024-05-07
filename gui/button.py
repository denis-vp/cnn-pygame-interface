import pygame


class Button:

    def __init__(self, root: pygame.Surface, action: callable,
                 x: int, y: int, width: int, height: int, color: tuple[int, int, int],
                 text: str, font: pygame.font.SysFont = pygame.font.SysFont("comicsans", 40)):
        self.root = root
        self.action = action
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.text, self.font = text, font

    def click(self, coordinates: tuple[int, int]):
        x, y = coordinates
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            self.action()

    def draw(self):
        pygame.draw.rect(self.root, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, 1, (255, 255, 255))
        self.root.blit(text, (self.x + self.width // 2 - text.get_width() // 2,
                              self.y + self.height // 2 - text.get_height() // 2))
