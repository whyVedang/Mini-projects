class Letter_state:
    def __init__(self,character):
        self.character = character
        self.inword= False
        self.inpos=False

    def __repr__(self):
        return f"[{self.character} inword={self.inword} inpos={self.inpos}]"