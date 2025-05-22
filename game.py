import pygame
from sys import exit
from tictactoe_q import qlearning_move_X, qlearning_move_O, check_win
import pandas as pd
import time

#general game init
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Q-learning Tic-Tac-Toe")
clock = pygame.time.Clock()

#item init
grid = pygame.image.load("images/grid.jpg")
grid = pygame.transform.scale(grid, (300, 300))
x_object = pygame.image.load("images/x.png")
x_object = pygame.transform.scale(x_object, (100, 100))
o_object = pygame.image.load("images/o.png")
o_object = pygame.transform.scale(o_object, (100, 100))

AIO = pygame.image.load("images/AI-O.png")
AIO = pygame.transform.scale(AIO, (100, 100*2/3))
AIX = pygame.image.load("images/AI-X.png")
AIX = pygame.transform.scale(AIX, (100, 100*2/3))
PvP = pygame.image.load("images/PvP.png")
PvP = pygame.transform.scale(PvP, (100, 100*2/3))

reset = pygame.image.load("images/Reset.png")
reset = pygame.transform.scale(reset, (100, 66))

def display_message(message,distance_from_top = 50, font_size = 70):
    font = pygame.font.Font("fonts/Pixeltype.ttf", font_size)
    text_surface = font.render(message, True, "Black") 
    text_rect = text_surface.get_rect(center=(500 // 2, distance_from_top)) 
    screen.blit(text_surface, text_rect)

def draw_board(board):    
    screen.blit(grid,(100,100)) 
    for x in range(len(board)):
        if board[x] == "X":
            screen.blit(x_object,(100 * ((x % 3) + 1),100 * ((x // 3) + 1)))
        elif board[x] == "O":
            screen.blit(o_object,(100 * ((x % 3) + 1),100 * ((x // 3) + 1)))

#important vars init
game_active = False
welcome_screen = True
board = ["","","","","","","","",""]
current = 0
AI_control = ""
exploitation = 1
available = [0,1,2,3,4,5,6,7,8]
path_X = "q-table_X.csv"
path_O = "q-table_O.csv"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            #welocme screen and menu
            if welcome_screen:
                if mouse_x >= 50 and mouse_x <= 150 and mouse_y >= 300 and mouse_y <= 366:
                    AI_control = "O"
                elif mouse_x >= 200 and mouse_x <= 300 and mouse_y >= 300 and mouse_y <= 366:
                    AI_control = "X"
                elif mouse_x >= 350 and mouse_x <= 450 and mouse_y >= 300 and mouse_y <= 366:
                    AI_control = ""
                else: 
                    continue
                
                board = ["","","","","","","","",""]
                available = [0,1,2,3,4,5,6,7,8]
                current = 0
                game_active = True
                welcome_screen = False
            
            #main game loop
            elif game_active:

                #placing x's and o's
                if mouse_x >= 100 and mouse_x <= 400 and mouse_y >= 100 and mouse_y <= 400:
                    square_x = mouse_x // 100
                    square_y = mouse_y // 100
                    square = int((((square_y-1) * 3) + square_x)-1)

                    if board[square] != "X" and board[square] != "O":
                        if current == 0 :
                            available.pop(available.index(square))
                            board[square] = "O"
                            current = 1
                        elif current == 1:
                            available.pop(available.index(square))
                            board[square] = "X"
                            current = 0
                
                #hitting reset
                elif mouse_x >= 200 and mouse_x <= 300 and mouse_y >= 417 and mouse_y <= 473:
                    board = ["","","","","","","","",""]
                    available = [0,1,2,3,4,5,6,7,8]
                    current = 0
                else:
                    continue
            
            #reseting the game state
            else:
                if mouse_x >= 200 and mouse_x <= 300 and mouse_y >= 417 and mouse_y <= 473:
                    board = ["","","","","","","","",""]
                    available = [0,1,2,3,4,5,6,7,8]
                    current = 0
                    game_active = True
                else:
                    continue
    
    #welcome screen options
    if welcome_screen:
        screen.fill("White")
        display_message("Welcome to",150)
        display_message("Tic-Tac-Toe!", 200, 100)

        screen.blit(AIO, (50,300))
        screen.blit(AIX, (200,300))
        screen.blit(PvP, (350,300))
    
    #during gameplay options
    elif game_active:
        screen.fill("Orange")
        draw_board(board) 
        screen.blit(reset, (200,417))

        to_return = check_win(board)
        if to_return:
            print(to_return)
            game_active = False
        elif len(available) == 0:
            game_active = False
        else:
            if current == 0 and AI_control == "O":
                board,available,item = qlearning_move_O(board,available,exploitation,path_O)
                current = 1
            elif current == 1 and AI_control == "X":
                board,available,item = qlearning_move_X(board,available,exploitation,path_X)
                current = 0

        if current == 0:
            display_message("It is currently O's turn")
        else: 
            display_message("It is currently X's turn")
            
    #end screen / reset functionality
    else:
        screen.fill("Green")
        draw_board(board)
        display_message(f"The winner is {check_win(board)}")
        screen.blit(reset, (200,417))

    pygame.display.update()
    clock.tick(60)
