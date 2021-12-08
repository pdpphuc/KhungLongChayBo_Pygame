from Picture import *

class Background(Picture):
    def __init__(self, screen, x=0, y=0):
        self.img_path = 'photos/background.jpg'
        super().__init__(screen, self.img_path, x=x, y=y)
