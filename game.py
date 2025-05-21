import pygame
from sys import exit

from tictactoe_q import qtable_getbest, qlearning_move_X, qlearning_move_O, check_win
import pandas as pd
import time

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Q-learning Tic-Tac-Toe")
clock = pygame.time.Clock()

grid = pygame.image.load("images/grid.jpg")
grid = pygame.transform.scale(grid, (300, 300))

x_object = pygame.image.load("images/x.png")
x_object = pygame.transform.scale(x_object, (100, 100))

o_object = pygame.image.load("images/o.png")
o_object = pygame.transform.scale(o_object, (100, 100))

font = pygame.font.Font("fonts/Pixeltype.ttf", 70)
text_surface = font.render("hello", False, "black")

def display_message(message):
    """Renders and displays a message on the screen."""
    text_surface = font.render(message, True, "Black") # Render the text (antialias, color)
    # Position the text at the top center of the screen
    text_rect = text_surface.get_rect(center=(500 // 2, 50)) # 50 pixels from the top
    screen.blit(text_surface, text_rect)

def draw_board(board):    
    screen.blit(grid,(100,100)) 
    for x in range(len(board)):
        if board[x] == "X":
            screen.blit(x_object,(100 * ((x % 3) + 1),100 * ((x // 3) + 1)))
        elif board[x] == "O":
            screen.blit(o_object,(100 * ((x % 3) + 1),100 * ((x // 3) + 1)))

game_active = False
board = ["","","","","","","","",""]
current = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            
            if game_active:
                #placing x's and o's
                if mouse_x >= 100 and mouse_x <= 400 and mouse_y >= 100 and mouse_y <= 400:
                    square_x = mouse_x // 100
                    square_y = mouse_y // 100
                    square = int((((square_y-1) * 3) + square_x)-1)

                    if board[square] != "X" and board[square] != "O":
                        if current == 0:
                            board[square] = "O"
                            current = 1
                        else:
                            board[square] = "X"
                            current = 0

                #hitting reset
                elif mouse_x <= 100:
                    print("not quite")
            
            #hitting new game
            else:
                board = ["","","","","","","","",""]
                current = 0
                game_active = True

    if game_active:
        screen.fill("Orange")
        draw_board(board)

        to_return = check_win(board)
        if to_return:
            print(to_return)
            game_active = False
        elif board.count("") == 0:
            game_active = False

        if current == 0:
            display_message("It is currently O's turn")
        else: 
            display_message("It is currently X's turn")
            
    #end screen
    else:
        screen.fill("Green")
        draw_board(board)
        display_message(f"The winner is {check_win(board)}")

    pygame.display.update()
    clock.tick(60)

if __name__ == "__main__":
    main()