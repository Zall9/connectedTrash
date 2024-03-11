
import random
from time import sleep

import os
## Create a python class called Player

class Player:
    ## constructor
    def __init__(self, is_good=True):
        self.is_good = is_good
        self.goodRoot = "sounds/positive/"
        self.badRoot = "sounds/negative/"
        self.goodOnes = ["clapttrap1.wav", "intelligence.wav", "neuronne.wav"]
        self.badOnes = ["rate1.wav"]

    def play(self):
        if self.is_good:
            file = self.goodRoot + random.choice(self.goodOnes)
        else:
            file = self.badRoot + random.choice(self.badOnes)
            print("Playing bad sound: " + file)
        os.system("afplay " + file)
        