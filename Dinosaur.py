from Picture import *

class Dinosaur(Picture):
    def __init__(self, screen, x=0, y=230):
        self.img_path = 'photos/dinosaur.png'
        super().__init__(screen, self.img_path, x=x, y=y)
