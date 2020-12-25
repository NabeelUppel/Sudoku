import numpy as np
import pygame
import pygame.freetype
from Solution import SudokuSolution
import copy
from pygame.locals import (
    K_ESCAPE,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9
)

pygame.init()


class Block(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super(Block, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((25, 80, 45))
        self.neighbours = []
        self.pos = (x_pos, y_pos)
        self.image = None
        self.rect = self.surf.get_rect(bottomright=self.pos)
        self.value = 0

    def setImage(self, num):
        self.image = pygame.image.load('Art/' + str(num) + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))

    def highlightBlock(self):
        self.surf.fill(HIGHLIGHT_GREEN)

    def unhighlightBlock(self):
        self.surf.fill(DARK_GREEN)
        if self.image is not None:
            self.surf.blit(self.image, self.image.get_rect())

    def update(self, num):
        self.surf.fill(DARK_GREEN)
        self.setImage(num)
        self.value = num
        self.surf.blit(self.image, self.image.get_rect())

    def getCoord(self):
        X = (self.pos[0] // 50) - 1
        Y = (self.pos[1] // 50) - 1
        return X, Y

    def setCurrentBoard(self):
        X, Y = self.getCoord()
        currentBoard[Y][X] = self.value


GAME_FONT = pygame.font.SysFont('Comic Sans MS', 25)
DARK_GREEN = (25, 80, 45)
HIGHLIGHT_GREEN = (25, 95, 45, 255)
clock = pygame.time.Clock()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450
BOARD_HEIGHT = 450
BOARD_WIDTH = 450
BOARD_MARGIN = 1
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

Board = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
Board.fill((255, 0, 255))

all_blocks = pygame.sprite.Group()
fixed_blocks = pygame.sprite.Group()
variable_blocks = pygame.sprite.Group()

for y in range(1, 10):
    for x in range(1, 10):
        block = Block(x * 50, y * 50)
        all_blocks.add(block)

puzzle = np.array([
    [0, 0, 0, 4, 0, 0, 0, 0, 0],
    [4, 0, 9, 0, 0, 6, 8, 7, 0],
    [0, 0, 0, 9, 0, 0, 1, 0, 0],
    [5, 0, 4, 0, 2, 0, 0, 0, 9],
    [0, 7, 0, 8, 0, 4, 0, 6, 0],
    [6, 0, 0, 0, 3, 0, 5, 0, 2],
    [0, 0, 1, 0, 0, 7, 0, 0, 0],
    [0, 4, 3, 2, 0, 0, 6, 0, 5],
    [0, 0, 0, 0, 0, 5, 0, 0, 0]])

solution = copy.copy(puzzle)
currentBoard = copy.copy(puzzle)

for x, y in np.ndenumerate(puzzle):
    xp, yp = x
    pos_x = (xp + 1) * 50
    pos_y = (yp + 1) * 50
    for bl in all_blocks:
        if bl.pos[0] == pos_y and bl.pos[1] == pos_x and y != 0:
            bl.update(y)
            fixed_blocks.add(bl)

for x in all_blocks:
    if x not in fixed_blocks:
        variable_blocks.add(x)

sudoku = SudokuSolution(solution)
solution = sudoku.board
print(solution)
wrongCount = 0
currentMins = 00
currentSecs = 00
CurrentBlock = None
running = True
Lost =False
while running:
    screen.fill((255, 255, 255))
    key = 0
    text = GAME_FONT.render("Strikes" + ": " + str(wrongCount), False, DARK_GREEN)
    if wrongCount == 3:
        win = GAME_FONT.render("You Lose", False, DARK_GREEN)
        screen.blit(win, (500, 200))
        Lost =True
        # running = False

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for b in all_blocks:
                if b.rect.collidepoint(x, y):
                    if not fixed_blocks.has(b):
                        CurrentBlock = b
                        CurrentBlock.highlightBlock()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if CurrentBlock is not None:
                if event.key == K_1:
                    key = 1
                if event.key == K_2:
                    key = 2
                if event.key == K_3:
                    key = 3
                if event.key == K_4:
                    key = 4
                if event.key == K_5:
                    key = 5
                if event.key == K_6:
                    key = 6
                if event.key == K_7:
                    key = 7
                if event.key == K_8:
                    key = 8
                if event.key == K_9:
                    key = 9


        elif event.type == pygame.QUIT:
            running = False

    if key != 0:
        CurrentBlock.update(key)
        x, y = CurrentBlock.getCoord()
        if solution[y][x] == key:
            fixed_blocks.add(CurrentBlock)
            CurrentBlock.setCurrentBoard()
            CurrentBlock = None
            # print("correct")
        else:
            wrongCount = wrongCount + 1
            print(wrongCount)

    for x in variable_blocks:
        if x is not CurrentBlock:
            x.unhighlightBlock()

    for b in all_blocks:
        Board.blit(b.surf, b.rect)

    for row in range(9):
        for column in range(9):
            if row % 3 == 0 and column % 3 == 0:
                width = 3
            else:
                width = 1
            pygame.draw.line(Board, (0, 0, 0), (row * 50, 0), (row * 50, 450), width)
            pygame.draw.line(Board, (0, 0, 0), (0, column * 50), (450, column * 50), width)


    # out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)


    if len(fixed_blocks.sprites()) != 81 :
        if not Lost:
            ticks = pygame.time.get_ticks()
            seconds = int(ticks / 1000 % 60)
            minutes = int(ticks / 60000 % 24)
            currentMins = minutes
            currentSecs =seconds
            out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
            timer = GAME_FONT.render(out, False, DARK_GREEN)
            screen.blit(timer, (500, 150))
    else:
        win = GAME_FONT.render("You Win", False, DARK_GREEN)
        screen.blit(win, (500, 200))
        timeOut = '{minutes:02d}:{seconds:02d}'.format(minutes=currentMins, seconds=currentSecs)
        time= GAME_FONT.render(timeOut, False, DARK_GREEN)
        screen.blit(time, (500, 250))

    screen.blit(text, (500, 100))
    screen.blit(Board, Board.get_rect())

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
