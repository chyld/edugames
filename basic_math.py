import json
import os
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
        button_width = 200
        button_height = 100
        spacing = 30
        total_width = (button_width * 2) + spacing
        start_x = (WINDOW_WIDTH - total_width) // 2

        # Basic mode buttons (top row)
        self.basic_addition_button = pygame.Rect(
            start_x, 200, button_width, button_height
        )
        self.basic_subtraction_button = pygame.Rect(
            start_x + button_width + spacing, 200, button_width, button_height
        )

        # Advanced mode buttons (bottom row)
        self.advanced_addition_button = pygame.Rect(
            start_x, 350, button_width, button_height
        )
        self.advanced_subtraction_button = pygame.Rect(
            start_x + button_width + spacing, 350, button_width, button_height
        )

    def draw(self):
        screen.fill(WHITE)

        # Draw title
        title_text = "Choose Your Math Mode!"
        title_surface = FONT_LARGE.render(title_text, True, BLACK)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Draw basic mode label
        basic_label = "Basic Mode (0-9)"
        basic_surface = FONT_MEDIUM.render(basic_label, True, BLACK)
        basic_rect = basic_surface.get_rect(center=(WINDOW_WIDTH // 2, 170))
        screen.blit(basic_surface, basic_rect)

        # Draw basic mode buttons
        pygame.draw.rect(screen, BLUE, self.basic_addition_button, border_radius=15)
        basic_add_text = "Addition"
        basic_add_surface = FONT_MEDIUM.render(basic_add_text, True, WHITE)
        basic_add_rect = basic_add_surface.get_rect(
            center=self.basic_addition_button.center
        )
        screen.blit(basic_add_surface, basic_add_rect)

        pygame.draw.rect(
            screen, PURPLE, self.basic_subtraction_button, border_radius=15
        )
        basic_sub_text = "Subtraction"
        basic_sub_surface = FONT_MEDIUM.render(basic_sub_text, True, WHITE)
        basic_sub_rect = basic_sub_surface.get_rect(
            center=self.basic_subtraction_button.center
        )
        screen.blit(basic_sub_surface, basic_sub_rect)

        # Draw advanced mode label
        advanced_label = "Advanced Mode (0-20)"
        advanced_surface = FONT_MEDIUM.render(advanced_label, True, BLACK)
        advanced_rect = advanced_surface.get_rect(center=(WINDOW_WIDTH // 2, 320))
        screen.blit(advanced_surface, advanced_rect)

        # Draw advanced mode buttons
        pygame.draw.rect(screen, GREEN, self.advanced_addition_button, border_radius=15)
        adv_add_text = "Addition"
        adv_add_surface = FONT_MEDIUM.render(adv_add_text, True, WHITE)
        adv_add_rect = adv_add_surface.get_rect(
            center=self.advanced_addition_button.center
        )
        screen.blit(adv_add_surface, adv_add_rect)

        pygame.draw.rect(
            screen, ORANGE, self.advanced_subtraction_button, border_radius=15
        )
        adv_sub_text = "Subtraction"
        adv_sub_surface = FONT_MEDIUM.render(adv_sub_text, True, WHITE)
        adv_sub_rect = adv_sub_surface.get_rect(
            center=self.advanced_subtraction_button.center
        )
        screen.blit(adv_sub_surface, adv_sub_rect)

    def handle_click(self, pos):
        if self.basic_addition_button.collidepoint(pos):
            return "basic_addition"
        if self.basic_subtraction_button.collidepoint(pos):
            return "basic_subtraction"
        if self.advanced_addition_button.collidepoint(pos):
            return "advanced_addition"
        if self.advanced_subtraction_button.collidepoint(pos):
            return "advanced_subtraction"
        return None


class MathGame:
    def __init__(self, mode):
        self.mode = mode
        self.score = 0
        self.high_score = self.load_high_score()
        self.problems_solved = 0
        self.wrong_answer_index = None
        self.wrong_answer_time = 0
        self.feedback_duration = 0.5
        self.answer_boxes = []
        self.attempts = 0
        self.menu_button = pygame.Rect(20, WINDOW_HEIGHT - 60, 200, 40)
        self.create_answer_boxes()
        self.generate_new_problem()

    def load_high_score(self):
        try:
            with open("basic_math.score", "r") as f:
                scores = json.load(f)
                return scores.get(self.mode, 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_high_score(self):
        try:
            if os.path.exists("basic_math.score"):
                with open("basic_math.score", "r") as f:
                    scores = json.load(f)
            else:
                scores = {}

            scores[self.mode] = max(scores.get(self.mode, 0), self.score)

            with open("basic_math.score", "w") as f:
                json.dump(scores, f)
        except Exception as e:
            print(f"Error saving high score: {e}")

    def generate_new_problem(self):
        if "addition" in self.mode:
            max_num = 20 if "advanced" in self.mode else 9
            self.num1 = random.randint(0, max_num)
            self.num2 = random.randint(
                0, max_num - self.num1
            )  # Ensure sum doesn't exceed max
            self.correct_answer = self.num1 + self.num2
            self.operator = "+"
        else:  # subtraction modes
            max_num = 20 if "advanced" in self.mode else 9
            self.num1 = random.randint(0, max_num)
            self.num2 = random.randint(0, self.num1)  # Ensure result is non-negative
            self.correct_answer = self.num1 - self.num2
            self.operator = "-"

        self.attempts = 0
        self.generate_answer_options()

    def generate_answer_options(self):
        wrong_answers = set()
        max_result = 40 if "advanced" in self.mode else 18
        min_result = -20 if "advanced" in self.mode else -9

        if "addition" in self.mode:
            while len(wrong_answers) < 3:
                wrong = self.correct_answer + random.randint(-3, 3)
                if wrong != self.correct_answer and wrong >= 0 and wrong <= max_result:
                    wrong_answers.add(wrong)
        else:  # subtraction modes
            # Always include the opposite sign of the correct answer
            opposite = -self.correct_answer
            if opposite >= min_result and opposite <= max_result:
                wrong_answers.add(opposite)

            # Add additional wrong answers
            while len(wrong_answers) < 3:
                wrong = self.correct_answer + random.randint(-3, 3)
                if (
                    wrong != self.correct_answer
                    and wrong != opposite
                    and wrong >= min_result
                    and wrong <= max_result
                ):
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
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
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
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 250))
        screen.blit(text_surface, text_rect)

        # Draw scores
        current_score_text = f"Score: {self.score}"
        current_score_surface = FONT_MEDIUM.render(current_score_text, True, BLACK)
        screen.blit(current_score_surface, (20, 20))

        high_score_text = f"High Score: {self.high_score}"
        high_score_surface = FONT_MEDIUM.render(high_score_text, True, GREEN)
        high_score_rect = high_score_surface.get_rect(right=WINDOW_WIDTH - 20, top=20)
        screen.blit(high_score_surface, high_score_rect)

        # Draw problems solved counter
        problems_text = f"Problems Solved: {self.problems_solved}"
        problems_surface = FONT_MEDIUM.render(problems_text, True, PURPLE)
        problems_rect = problems_surface.get_rect(centerx=WINDOW_WIDTH // 2, top=70)
        screen.blit(problems_surface, problems_rect)

        # Draw attempts counter if there have been any attempts
        if self.attempts > 0:
            attempts_text = f"Attempts: {self.attempts}"
            attempts_surface = FONT_MEDIUM.render(attempts_text, True, ORANGE)
            attempts_rect = attempts_surface.get_rect(right=WINDOW_WIDTH - 20, top=70)
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
            feedback_rect = feedback_surface.get_rect(center=(WINDOW_WIDTH // 2, 350))
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
