import pygame
pygame.init()
from random import randint

from Background import *
from Dinosaur import *
from Tree import *

class Game_DinosaurGame:
    # Font chữ
    SMALL_FONT = pygame.font.SysFont('Sans', 20)
    BIG_FONT = pygame.font.SysFont('Sans', 40)

    # Màu sắc
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Âm thanh
    TICK_SOUND = pygame.mixer.Sound('music/tick.wav')
    TE_SOUND = pygame.mixer.Sound('music/te.wav')

    # Hằng số khác
    VALUE_DOMAIN = (600, 3000)
    NUMBER_OF_TREES = 3

    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode((600, 300))
        pygame.display.set_caption('Khủng long chạy bộ')
        programIcon = pygame.image.load('photos/pngegg.png')
        pygame.display.set_icon(programIcon)

        self.__background = Background(self.__screen)
        self.__dinosaur = Dinosaur(self.__screen)
        self.__trees = []
        count = 0
        while True:
            tree = Tree(self.__screen, randint(*Game_DinosaurGame.VALUE_DOMAIN))
            if self.check_new_tree(tree):
                self.__trees.append(tree)
                count += 1
                if count == Game_DinosaurGame.NUMBER_OF_TREES:
                    break
                else:
                    continue
            else:
                tree.x = randint(*Game_DinosaurGame.VALUE_DOMAIN)

        self.__score = 0
        self.__score_txt = Game_DinosaurGame.SMALL_FONT.render(f'Score: {self.__score}', True, Game_DinosaurGame.RED)
        self.__game_over_txt = Game_DinosaurGame.BIG_FONT.render(f'GAME OVER', True, Game_DinosaurGame.RED)

        self.__running = True
        self.__pausing = True
        self.__dino_jumping_up = False

        self.__starting_point = 0
        self.set_velocity()

    def set_velocity(self):
        self.__Vx = 5
        self.__Vy = 9

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value
        self.__score_txt = Game_DinosaurGame.SMALL_FONT.render(f'Score: {self.__score}', True, Game_DinosaurGame.RED)

    def draw_score(self):
        self.__screen.blit(self.__score_txt, (5, 5))

    def dino_jump(self):
        # Nhảy lên
        if 230 >= self.__dinosaur.y >= 50:
            if self.__dino_jumping_up == True:
                self.__dinosaur.y -= self.__Vy
        else:
            # Dừng nhảy lên
            self.__dino_jumping_up = False

        # Nhảy xuống
        if self.__dinosaur.y < 230:
            if self.__dino_jumping_up == False:
                self.__dinosaur.y += self.__Vy

    def draw_game_over(self):
        self.__screen.blit(self.__game_over_txt, (200, 150))   

    def check_dino_colliderect_tree(self, tree):
        if self.__dinosaur._Picture__obj.colliderect(tree._Picture__obj):
            if not self.__pausing:
                pygame.mixer.Sound.play(Game_DinosaurGame.TE_SOUND)
            self.__pausing = True
            self.draw_game_over()
            self.__Vx = 0
            self.__Vy = 0

    def check_new_tree(self, tree):
        for t in self.__trees:
            distance = abs(tree.x - t.x)
            if 20 < distance < 150:
                return False
        return True

    def run(self):
        while self.__running:
            self.__clock.tick(60)
            self.__screen.fill(Game_DinosaurGame.WHITE)
            self.__background.draw(self.__starting_point, 0)
            self.__background.draw(self.__starting_point + 600, 0)
            self.__dinosaur.draw()

            for tree in self.__trees:
                tree.draw()
                self.check_dino_colliderect_tree(tree)
            self.draw_score()

            if not self.__pausing:
                self.dino_jump()
                # Di chuyển background
                if self.__starting_point + 600 <= 0:
                    self.__starting_point = 0
                self.__starting_point -= self.__Vx

                # Di chuyển các cây
                for tree in self.__trees:
                    tree.x -= self.__Vx
                    if tree.x <= -20:
                        while True:
                            tree.x = randint(*Game_DinosaurGame.VALUE_DOMAIN)
                            if self.check_new_tree(tree):
                                break
                        self.score += 1

            # Xử lý sự kiện người dùng
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.__dinosaur.y == 230:
                            pygame.mixer.Sound.play(Game_DinosaurGame.TICK_SOUND)
                            self.__dino_jumping_up = True
                        if self.__pausing:
                            self.__background.reset()
                            self.__dinosaur.reset()
                            for tree in self.__trees:
                                tree.reset()
                            self.set_velocity()
                            self.score = 0
                            self.__pausing = False
            pygame.display.flip()
        pygame.quit()