import random
import sys
import time

import pygame

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Fun Math Game!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (50, 205, 50)
RED = (255, 99, 71)
ORANGE = (255, 165, 0)
PURPLE = (147, 112, 219)
GRAY = (128, 128, 128)

# Font setup
FONT_LARGE = pygame.font.Font(None, 72)
FONT_MEDIUM = pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(None, 36)


class ModeSelection:
    def __init__(self):
        self.addition_button = pygame.Rect(WINDOW_WIDTH // 4 - 100, 300, 200, 100)
        self.subtraction_button = pygame.Rect(
            3 * WINDOW_WIDTH // 4 - 100, 300, 200, 100
        )

    def draw(self):
        screen.fill(WHITE)

        # Draw title
        title_text = "Choose Your Math Mode!"
        title_surface = FONT_LARGE.render(title_text, True, BLACK)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)

        # Draw addition button
        pygame.draw.rect(screen, BLUE, self.addition_button, border_radius=15)
        add_text = "Addition"
        add_surface = FONT_MEDIUM.render(add_text, True, WHITE)
        add_rect = add_surface.get_rect(center=self.addition_button.center)
        screen.blit(add_surface, add_rect)

        # Draw subtraction button
        pygame.draw.rect(screen, PURPLE, self.subtraction_button, border_radius=15)
        sub_text = "Subtraction"
        sub_surface = FONT_MEDIUM.render(sub_text, True, WHITE)
        sub_rect = sub_surface.get_rect(center=self.subtraction_button.center)
        screen.blit(sub_surface, sub_rect)

    def handle_click(self, pos):
        if self.addition_button.collidepoint(pos):
            return "addition"
        if self.subtraction_button.collidepoint(pos):
            return "subtraction"
        return None


class MathGame:
    def __init__(self, mode):
        self.mode = mode
        self.score = 0
        self.problems_solved = 0
        self.wrong_answer_index = None
        self.wrong_answer_time = 0
        self.feedback_duration = 0.5
        self.answer_boxes = []
        self.attempts = 0
        self.menu_button = pygame.Rect(20, WINDOW_HEIGHT - 60, 200, 40)
        self.create_answer_boxes()
        self.generate_new_problem()

    def generate_new_problem(self):
        if self.mode == "addition":
            self.num1 = random.randint(0, 9)
            self.num2 = random.randint(0, 9)
            self.correct_answer = self.num1 + self.num2
            self.operator = "+"
        else:  # subtraction
            self.num1 = random.randint(0, 9)
            self.num2 = random.randint(0, 9)
            self.correct_answer = self.num1 - self.num2
            self.operator = "-"

        self.attempts = 0
        self.generate_answer_options()

    def generate_answer_options(self):
        wrong_answers = set()
        while len(wrong_answers) < 3:
            if self.mode == "addition":
                wrong = self.correct_answer + random.randint(-3, 3)
                if wrong != self.correct_answer and wrong >= 0 and wrong <= 18:
                    wrong_answers.add(wrong)
            else:  # subtraction
                wrong = self.correct_answer + random.randint(-3, 3)
                if wrong != self.correct_answer and wrong >= -9 and wrong <= 9:
                    wrong_answers.add(wrong)

        self.answers = list(wrong_answers) + [self.correct_answer]
        random.shuffle(self.answers)
        self.correct_answer_index = self.answers.index(self.correct_answer)
        self.wrong_answer_index = None

    def create_answer_boxes(self):
        box_width = 150
        box_height = 80
        spacing = 30
        total_width = (box_width * 4) + (spacing * 3)
        start_x = (WINDOW_WIDTH - total_width) // 2
        y = 400

        self.answer_boxes = []
        for i in range(4):
            x = start_x + (box_width + spacing) * i
            self.answer_boxes.append(pygame.Rect(x, y, box_width, box_height))

    def check_answer(self, answer_index):
        current_time = time.time()

        if self.wrong_answer_index is not None:
            if current_time - self.wrong_answer_time < self.feedback_duration:
                return
            else:
                self.wrong_answer_index = None

        if answer_index == self.correct_answer_index:
            self.score += 1
            self.problems_solved += 1
            self.generate_new_problem()
        else:
            self.attempts += 1
            self.wrong_answer_index = answer_index
            self.wrong_answer_time = current_time
            self.generate_answer_options()

    def handle_click(self, pos):
        # Check if menu button was clicked
        if self.menu_button.collidepoint(pos):
            return "menu"

        # Check answer boxes
        for i, box in enumerate(self.answer_boxes):
            if box.collidepoint(pos):
                self.check_answer(i)
                return None
        return None

    def handle_key(self, key):
        if pygame.K_1 <= key <= pygame.K_4:
            answer_index = key - pygame.K_1
            self.check_answer(answer_index)
        elif key == pygame.K_ESCAPE:
            return "menu"
        return None

    def draw(self):
        screen.fill(WHITE)

        # Draw problem text
        problem_text = f"{self.num1} {self.operator} {self.num2} = ?"
        text_surface = FONT_LARGE.render(problem_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200))
        screen.blit(text_surface, text_rect)

        # Draw score
        score_text = f"Score: {self.score}"
        score_surface = FONT_MEDIUM.render(score_text, True, BLACK)
        screen.blit(score_surface, (20, 20))

        # Draw problems solved counter
        problems_text = f"Problems Solved: {self.problems_solved}"
        problems_surface = FONT_MEDIUM.render(problems_text, True, PURPLE)
        problems_rect = problems_surface.get_rect(centerx=WINDOW_WIDTH // 2, top=20)
        screen.blit(problems_surface, problems_rect)

        # Draw attempts counter if there have been any attempts
        if self.attempts > 0:
            attempts_text = f"Attempts: {self.attempts}"
            attempts_surface = FONT_MEDIUM.render(attempts_text, True, ORANGE)
            attempts_rect = attempts_surface.get_rect(right=WINDOW_WIDTH - 20, top=20)
            screen.blit(attempts_surface, attempts_rect)

        # Draw answer boxes
        current_time = time.time()
        for i, box in enumerate(self.answer_boxes):
            box_color = BLUE
            if (
                i == self.wrong_answer_index
                and current_time - self.wrong_answer_time < self.feedback_duration
            ):
                box_color = RED

            pygame.draw.rect(screen, box_color, box, border_radius=10)

            # Draw the number (1-4) in small text above the answer
            key_text = f"Press {i + 1}"
            key_surface = FONT_SMALL.render(key_text, True, BLACK)
            key_rect = key_surface.get_rect(centerx=box.centerx, bottom=box.top - 5)
            screen.blit(key_surface, key_rect)

            # Draw the answer
            answer_text = str(self.answers[i])
            text_surface = FONT_MEDIUM.render(answer_text, True, WHITE)
            text_rect = text_surface.get_rect(center=box.center)
            screen.blit(text_surface, text_rect)

        # Draw menu button
        pygame.draw.rect(screen, GRAY, self.menu_button, border_radius=5)
        menu_text = "Back to Menu (Esc)"
        menu_surface = FONT_SMALL.render(menu_text, True, WHITE)
        menu_rect = menu_surface.get_rect(center=self.menu_button.center)
        screen.blit(menu_surface, menu_rect)

        # If showing wrong answer feedback, display "Try Again!" message with attempt count
        if (
            self.wrong_answer_index is not None
            and current_time - self.wrong_answer_time < self.feedback_duration
        ):
            feedback_text = f"Try Again! (Attempt {self.attempts})"
            feedback_surface = FONT_MEDIUM.render(feedback_text, True, RED)
            feedback_rect = feedback_surface.get_rect(center=(WINDOW_WIDTH // 2, 300))
            screen.blit(feedback_surface, feedback_rect)


def main():
    mode_selection = ModeSelection()
    game = None
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game is None:
                    selected_mode = mode_selection.handle_click(event.pos)
                    if selected_mode:
                        game = MathGame(selected_mode)
                else:
                    result = game.handle_click(event.pos)
                    if result == "menu":
                        game = None
            elif event.type == pygame.KEYDOWN and game is not None:
                result = game.handle_key(event.key)
                if result == "menu":
                    game = None

        if game is None:
            mode_selection.draw()
        else:
            game.draw()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
