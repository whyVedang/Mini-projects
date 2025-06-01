from wordle import Wordle
import random

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
                print(f"Your guess must be {self.wordle.WORD_LENGTH} letters long.")
                continue
            
            if not self.wordle.isvalid(guess, self.words):
                print(self.words)
                print(guess)
                print("Not a valid word!")
                continue
                
            self.wordle.attempt(guess)
            temp = self.wordle.theguess(guess)
            print(*temp, sep="\n")
            
            if self.wordle.solved:
                print("Congratulations! You've guessed the word!")
                break
            
            print(f"Remaining attempts: {self.wordle.remainingAttempts}")
            
        if not self.wordle.solved:
            print(f"You lost !\nThe word was: {self.secret}")

    
    def loadsecret(self):
        try:
            with open('data/words.txt', 'r') as f:
                self.words = [word.strip().upper() for word in f.readlines()]
                # print(self.words)
                self.secret = random.choice(self.words)
        except FileNotFoundError:
            self.secret = None

if __name__ == "__main__":
    game = Terminal()
    game.main()