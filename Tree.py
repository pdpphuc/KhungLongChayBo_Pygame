from Picture import *

class Tree(Picture):
    def __init__(self, screen, x=550, y=230):
        self.img_path = 'photos/tree.png'
        super().__init__(screen, self.img_path, x=x, y=y)
