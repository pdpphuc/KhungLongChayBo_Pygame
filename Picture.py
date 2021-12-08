import pygame

class Picture:

    def __init__(self, screen, img_path, x, y):
        self.__screen = screen
        self.__img = pygame.image.load(img_path)
        self.x = self.rx = x
        self.y = self.ry = y
        self.__obj = screen.blit(self.__img, (self.x, self.y))

    def draw(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y
        self.__obj = self.__screen.blit(self.__img, (self.x, self.y))

    def reset(self):
        self.x = self.rx
        self.y = self.ry