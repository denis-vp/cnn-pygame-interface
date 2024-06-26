from dataclasses import dataclass

import keras.src.saving
import numpy as np
import pygame

from gui.button import Button
from gui.percentage_display import PercentageDisplay

# Window settings
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 900

# Grid settings
NUM_ROWS, NUM_COLUMNS = 28, 28
CELL_HEIGHT = WINDOW_HEIGHT // NUM_ROWS
CELL_WIDTH = CELL_HEIGHT
GRID_HEIGHT = CELL_HEIGHT * NUM_ROWS
GRID_WIDTH = CELL_WIDTH * NUM_COLUMNS

# Button settings
BUTTON_HEIGHT = 50
BUTTON_WIDTH = WINDOW_WIDTH - GRID_WIDTH

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)


@dataclass
class Cell:
    x: int
    y: int
    value: int


class MNISTGui:
    def __init__(self):
        self.root = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Neural Network - Drawing Board")

        self.cells: list[Cell] = []
        self.create_grid(NUM_ROWS, NUM_COLUMNS)

        self.states_history = [self.cells.copy()]
        self.undo_history = []

        self.clear_button = Button(self.root, self.clear, GRID_WIDTH, 70, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, "Clear")
        self.buttons = [self.clear_button]

        self.percentages = []
        self.create_percentage_displays()

        self.model = keras.src.saving.load_model("./models/mnist_cnn.keras")

    def create_grid(self, num_rows: int, num_columns: int):
        for row in range(num_rows):
            for col in range(num_columns):
                self.cells.append(Cell(row * CELL_WIDTH, col * CELL_HEIGHT, 255))
        return self.cells

    def create_percentage_displays(self):
        for i in range(10):
            x = GRID_WIDTH + 10
            y = 70 + BUTTON_HEIGHT * 2 + i * 50
            percentage_display = PercentageDisplay(self.root, x, y, BUTTON_WIDTH, BUTTON_HEIGHT, PURPLE, f"{i}: ")
            self.percentages.append(percentage_display)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    for button in self.buttons:
                        button.click(pygame.mouse.get_pos())
                    self.draw(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                    self.erase(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                    self.draw(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEMOTION and event.buttons[2]:
                    self.erase(pygame.mouse.get_pos())
            self.update_display()

    def update_display(self):
        self.root.fill(CYAN)
        self.draw_grid()
        for button in self.buttons:
            button.draw()
        for percentage in self.percentages:
            percentage.draw()

        font = pygame.font.SysFont("comicsans", 12)
        draw_text = font.render("Left click to draw.", 1, BLACK)
        erase_text = font.render("Right click to erase.", 1, BLACK)
        self.root.blit(draw_text, (GRID_WIDTH + 10, 10))
        self.root.blit(erase_text, (GRID_WIDTH + 10, 40))

        pygame.display.update()

    def draw_grid(self):
        for cell in self.cells:
            cell_color = (cell.value, cell.value, cell.value)
            pygame.draw.rect(self.root, cell_color, (cell.x, cell.y, CELL_WIDTH, CELL_HEIGHT))

    #       Interaction

    def draw(self, coordinates: tuple[int, int]):
        x, y = coordinates
        for cell in self.cells:
            distance = ((cell.x - x) ** 2 + (cell.y - y) ** 2) ** 0.5
            if distance < CELL_WIDTH:
                color_value = max(0, cell.value - int(255 * (1 - distance / CELL_WIDTH)))
                cell.value = color_value
        self.guess()

    def erase(self, coordinates: tuple[int, int]):
        x, y = coordinates
        for cell in self.cells:
            distance = ((cell.x - x) ** 2 + (cell.y - y) ** 2) ** 0.5
            if distance < CELL_WIDTH:
                color_value = min(255, cell.value + int(255 * (1 - distance / CELL_WIDTH)))
                cell.value = color_value if color_value > 0 else 0
        self.guess()

    def clear(self):
        for cell in self.cells:
            cell.value = 255
        self.states_history.append(self.cells.copy())
        self.reset_percentages()

    def get_image(self):
        grayscale_values = [cell.value for cell in self.cells]
        image = np.array(grayscale_values).reshape(1, 28, 28, 1)
        image = image / 255  # Normalize grayscale values
        return image

    def guess(self):
        image = self.get_image()
        prediction = self.model.predict(image)
        for i, percentage in enumerate(self.percentages):
            percentage.update(prediction[0][i] * 100)

    def reset_percentages(self):
        for percentage in self.percentages:
            percentage.update(0)
