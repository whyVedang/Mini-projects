from wordle import Wordle
import random
from Letter_state import Letter_state
from typing import List
from colorama import Fore
class Terminal:
    def __init__(self):
        self.words = []
        self.loadsecret()
        self.wordle=Wordle(self.secret)
        print("Welcome to Wordle!")
    def main(self):
        while self.wordle.can_attempt:
            guess = input("Enter your guess! ").upper()
            if len(guess) != self.wordle.WORD_LENGTH:
                print(
                Fore.RED
                + f"Word must be {self.wordle.WORD_LENGTH} characters long!"
                + Fore.RESET
            )
                continue

            if not self.wordle.isvalid(guess, self.words):
                print(
                Fore.RED
                + f"{guess} is not a valid word!"
                + Fore.RESET
            )
                continue
            
            self.wordle.attempt(guess)
            self.display_results()
            
            if self.wordle.solved:
                print("Congratulations! You've guessed the word!")
                break
            print(f"Remaining attempts: {self.wordle.remainingAttempts}")
            
        if not self.wordle.solved:
            print(f"You lost !\nThe word was: {self.secret}")

    


    def loadsecret(self):
        try:
            with open('words.txt', 'r') as f:
                self.words = [word.strip().upper() for word in f.readlines()]
                # print(self.words)
                self.secret = random.choice(self.words)
        except FileNotFoundError:
            self.secret = None

    def display_results(self):
        print("\nYour results so far...")
        print(f"You have {self.wordle.remainingAttempts} attempts remaining.\n")

        lines = []

        for word in self.wordle.attempts:
            result = self.wordle.theguess(word)
            colored_result_str = self.convert_result_to_color(result)
            lines.append(colored_result_str)

        for _ in range(self.wordle.remainingAttempts):
            lines.append(" ".join(["_"] * self.wordle.WORD_LENGTH))
        self.draw_border_around(lines)

    def convert_result_to_color(self, result: List[Letter_state]):
        result_with_color = []
        for letter in result:
            if letter.inpos:
                color = Fore.GREEN
            elif letter.inword:
                color = Fore.YELLOW
            else:
                color = Fore.WHITE
            colored_letter = color + letter.character + Fore.RESET
            result_with_color.append(colored_letter)
        return " ".join(result_with_color)


    def draw_border_around(self, lines: List[str], size: int = 9, pad: int = 1):

        content_length = size + pad * 2
        top_border = "┌" + "─" * content_length + "┐"
        bottom_border = "└" + "─" * content_length + "┘"
        space = " " * pad
        print(top_border)

        for line in lines:
            print("│" + space + line + space + "│")

        print(bottom_border)

if __name__ == "__main__":
    game = Terminal()
    game.main()