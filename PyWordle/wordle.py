from Letter_state import Letter_state
class Wordle:
    MAX_ATTEMPTS = 6
    WORD_LENGTH = 5
    def __init__(self,secret):
        self.attempts=[]
        self.secret=secret.upper()
    
    def attempt(self,guess):
        self.attempts.append(guess)


    def theguess(self,guess):
        res=[]
        for i in range (self.WORD_LENGTH):
            letter=Letter_state(guess[i])
            letter.inword = guess[i] in self.secret
            letter.inpos= guess[i] ==self.secret[i]
            res.append(letter)
        return res
    @property
    def solved(self):
        return self.attempts and self.attempts[-1] == self.secret
    
    def isvalid(self, guess, words):
        return True if guess in words else False

    @property
    def can_attempt(self):
        return len(self.attempts)< self.MAX_ATTEMPTS and not self.solved
    
    @property
    def remainingAttempts(self):
        return self.MAX_ATTEMPTS - len(self.attempts)
    