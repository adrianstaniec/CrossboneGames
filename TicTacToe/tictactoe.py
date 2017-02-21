from time import sleep
import pygame
import numpy as np

def draw_board(matrix):
    for x in range(3):
        for y in range(3):
            if matrix[x][y] != 0:
                screen.blit(markers[matrix[x][y]-1], (30+200*x, 30+200*y))

def draw_cursor(player, cursor_pos):
    x = cursor_pos[0]
    y = cursor_pos[1]
    screen.blit(cursors[player], (30+200*x, 30+200*y))

def move_cursor(pos, vec):
    new_pos = pos + vec
    if new_pos[0] >= 0 and new_pos[0] <= 2:
        if new_pos[1] >= 0 and new_pos[1] <= 2:
            return new_pos
    return pos

def mark_spot(player, cursor_pos):
    x = cursor_pos[0]
    y = cursor_pos[1]
    if matrix[x][y] == 0:
        matrix[x][y] = player + 1
        return abs(player-1)
    return player

def check_status(matrix):
    for row in range(3):
        if matrix[row][0] == matrix[row][1]:
            if (matrix[row][1] == matrix[row][2]):
                return matrix[row][0]
    for col in range(3):
        if matrix[0][col] == matrix[1][col]:
            if (matrix[1][col] == matrix[2][col]):
                return matrix[0][col]
    # diagonals
    if matrix[0][0] == matrix[1][1]:
        if matrix[1][1] == matrix[2][2]:
            return matrix[1][1]
    if matrix[2][0] == matrix[1][1]:
        if matrix[1][1] == matrix[0][2]:
            return matrix[1][1]
    return 0

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

board = pygame.image.load("resources/board.png")
ends = [pygame.image.load("resources/end0.png"),
        pygame.image.load("resources/end1.png")]
markers = [pygame.image.load("resources/marker0.png"),
        pygame.image.load("resources/marker1.png")]
cursors = [pygame.image.load("resources/cursor0.png"),
        pygame.image.load("resources/cursor1.png")]

player = 0

cursor_pos=np.array([1,1])

matrix = [[0,0,0],
          [0,0,0],
          [0,0,0]]

while True:
    screen.fill(0) #clear screen
    vector = (0, 0)
    mark = False
    screen.blit(board, (0, 0))
    draw_board(matrix)
    draw_cursor(player,cursor_pos)
    pygame.display.flip() #update screen

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                exit(0)
            if event.key == pygame.K_SPACE:
                mark = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_h:
                vector = (-1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_j:
                vector = (0, 1)
            elif event.key == pygame.K_UP or event.key == pygame.K_k:
                vector = (0, -1)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                vector = (1, 0)
            cursor_pos = move_cursor(cursor_pos, np.array(vector))
            if mark:
                player = mark_spot(player, cursor_pos)
                status = check_status(matrix)
                if status != 0:
                    screen.blit(ends[player-1],(0,0))
                    pygame.display.flip() #update screen
                    sleep(1)
                    exit(0)
