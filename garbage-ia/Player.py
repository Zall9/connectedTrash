
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

        goodFiles = os.listdir(self.goodRoot)
        badFiles = os.listdir(self.badRoot)

        self.goodOnes = [f for f in goodFiles if os.path.isfile(os.path.join(self.goodRoot, f))]
        self.badOnes = [f for f in badFiles if os.path.isfile(os.path.join(self.badRoot, f))]

    def play(self):
        if self.is_good:
            file = self.goodRoot + random.choice(self.goodOnes)
        else:
            file = self.badRoot + random.choice(self.badOnes)
            print("Playing bad sound: " + file)
        os.system("aplay " + file)
        

