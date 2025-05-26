import random
import pandas as pd
import pickle
import os

def list_to_string(list):
    temp = ""
    for x in list:
        if x == "":
            x = " "
        temp = temp + x
    return temp

def string_to_list(string):
    temp = list(string)
    for x in range(len(temp)):
        if temp[x] == " ":
            temp[x] = ""
    return temp

def print_board(board):
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

def human_move(board,available,current):
    pos = 9999
    while pos not in available:
        print(available)
        print_board(board)
        pos = int(input("What position would you like to take? : "))

    available.pop(available.index(pos))
    
    if current == 1:
        board[pos] = "X"
    else:
        board[pos] = "O"

    return board,available

#make a random move (not used)
def random_move(board, available,current):
    pos = 9999
    pos = random.randint(0,len(available)-1)
    print(f"The super smart bot has taken the square in position {pos}")

    if current == 1:
        board[available[pos]] = "O"
    else:
        board[available[pos]] = "X"

    available.pop(pos)

    return board,available

#gets a q learning move for X, use proper table and such
def qlearning_move_X(board,available,exploitation,path_X):
    #check whether to pick random or known
    if random.random() >= exploitation:
        action_pos = random.randint(0,len(available)-1)
        action = available[action_pos]
        item = [list(board),action,0]
        qtable_add(path_X,item)
        board[available[action_pos]] = "X"
        available.pop(action_pos)
        return board,available,item 
    
    #choose from the q table
    else:
        #if random used instead (same as above)
        if qtable_getbest(path_X, board) == None:
            action_pos = random.randint(0,len(available)-1)
            action = available[action_pos]
            item = [list(board),action,0]
            qtable_add(path_X,item) 
            board[available[action_pos]] = "X"
            available.pop(action_pos)

        else:
            action = qtable_getbest(path_X, board)
            action_pos = available.index(action)
            item = [list(board),action,0]
            qtable_add(path_X,item)
            board[available[action_pos]] = "X"
            available.pop(action_pos)

        return board,available,item
    
#O for q learning
def qlearning_move_O(board,available,exploitation,path_O):
    
    #check whether to pick random or known
    if random.random() >= exploitation:
        action_pos = random.randint(0,len(available)-1)
        action = available[action_pos]
        item = [list(board),action,0]
        qtable_add(path_O,item)
        board[available[action_pos]] = "O"
        available.pop(action_pos)
        return board,available,item 
    
    #choose from the q table
    else:
        #if random used instead (same as above)
        if qtable_getbest(path_O, board) == None:
            action_pos = random.randint(0,len(available)-1)
            action = available[action_pos]
            item = [list(board),action,0]
            qtable_add(path_O,item) 
            board[available[action_pos]] = "O"
            available.pop(action_pos)

        else:
            action = qtable_getbest(path_O, board)
            action_pos = available.index(action)
            item = [list(board),action,0]
            qtable_add(path_O,item)
            board[available[action_pos]] = "O"
            available.pop(action_pos)

        return board,available,item

def check_win(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8], 
        [0, 4, 8], [2, 4, 6] 
    ]

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]]:
            if board[condition[0]] != "":
                return board[condition[0]]
    
    return None

def tictactoe(player,exploitation):
    current = 0

    movelist_X = []
    movelist_O = []

    board = ["","","","","","","","",""]
    available = [0,1,2,3,4,5,6,7,8]
    gameon = True

    while gameon == True:
        #O move
        if current == 0:
            if player == "O":
                board,available = human_move(board,available,current)
            else:
                board,available,item = qlearning_move_O(board,available,exploitation,path_O)
                movelist_O.append(item)
            current = 1
        #X move
        else:
            if player == "X":
                board,available = human_move(board,available,current)
            else:
                board,available,item = qlearning_move_X(board,available,exploitation,path_X)
                movelist_X.append(item)
            current = 0
        
        #win cons
        to_return = check_win(board)
        if to_return:
            return movelist_X,movelist_O,board,to_return
        elif len(available) == 0:
            return movelist_X,movelist_O,board,None
        
#setup of an initial q table 
def qtable_setup(path):
    if (os.path.exists(path)):
        print(f"q-table already exists at {path}")
    else:
        df = pd.DataFrame(columns=['state', 'action', 'pos'])
        df.to_csv(path)
        print(f"q-table has been setup at {path}")

#adding item to qtable
def qtable_add(path,item):
    data = pd.read_csv(path)

    item_state_str = list_to_string(item[0])
    item_action = item[1]
    item_pos = item[2]

    new_row_df = pd.DataFrame([[item_state_str, item_action, item_pos]], columns=["state", "action", "pos"])

    if not qtable_exist(path,item):
        data = pd.concat([data, new_row_df], ignore_index=True)
        data.to_csv(path, index=False)

#check if an item is in the table
def qtable_exist(path,item):
    data = pd.read_csv(path)

    item_state_str = list_to_string(item[0])
    item_action = item[1]
    mask = (data["state"] == item_state_str) & (data["action"] == item_action)

    if data.loc[mask].empty:
        return False
    else:
        return True

#get the best move for the current state
def qtable_getbest(path,state):
    data = pd.read_csv(path)
    state_str = list_to_string(state)
    data = data[data["state"] == state_str]

    if data.empty:
        return None
    return data[data["pos"] == data["pos"].max()]["action"].iloc[0]

#change the expected positive outcome (pos) of a cerain state, action combination by a flat value
def qtable_changepos(path, item):
    data = pd.read_csv(path)
    data["state"] = data["state"].astype(str)
    item_state_str = list_to_string(item[0])
    item_action = item[1]
    add_value = item[2]
    mask = (data["state"] == item_state_str) & (data["action"] == item_action)
    if not data.loc[mask].empty:
        data.loc[mask, "pos"] += add_value
        data.to_csv(path, index=False)
    
if __name__ == "__main__":
    print("Welcome to Tic Tac Toe")
    print()

    #important variables
    path_X = "q-table_X.csv"
    path_O = "q-table_O.csv"

    #change here for training or gameplay
    training = True

    #setting up the q-table (check and spaces fixed)
    qtable_setup(path_X)
    qtable_setup(path_O)
    print()

    if training:
        exploitation = 0
        exploration = 1 - exploitation 
        alpha = 1
        alpha_decay = 0.01

        for x in range(100):
            #exploration_decay = exploration / (100/2) #create decay
            exploration_decay = 0.01
            exploration -= exploration_decay #apply decay
            exploration = max(0.01, exploration) #prevent too low
            exploitation = 1 - exploration

            alpha -= alpha_decay
            if alpha < 0:
                alpha = 0

            print("*"*30)
            print(f"training round {x}, exploitation of {exploitation}")

            X_wins = 0
            O_wins = 0
            Draws = 0

            #one round of training
            for x in range(500):
                print(f"game {x} / 500", end='\r')
                movelist_X,movelist_O,board,winner = tictactoe(0,exploitation)
                if winner =="O":
                    O_wins += 1
                    reward = 1
                    for item in movelist_O[::-1]:
                        item[2] += reward * alpha
                        reward = reward * 0.9
                        qtable_changepos(path_O,item)

                    punish = -1
                    for item in movelist_X[::-1]:
                        item[2] += punish * alpha
                        punish = punish * 0.9
                        qtable_changepos(path_X,item)

                elif winner =="X":
                    X_wins += 1
                    reward = 1
                    for item in movelist_X[::-1]:
                        item[2] += reward * alpha
                        reward = reward * 0.9
                        qtable_changepos(path_X,item)

                    punish = -1
                    for item in movelist_O[::-1]:
                        item[2] += punish * alpha
                        punish = punish * 0.9
                        qtable_changepos(path_O,item)

                else: 
                    Draws += 1
                    reward = 0.5
                    for item in movelist_O[::-1]:
                        item[2] += reward * alpha
                        reward = reward * 0.9
                        qtable_changepos(path_O,item)

                    reward = 0.5
                    for item in movelist_X[::-1]:
                        item[2] += reward * alpha
                        reward = reward * 0.9
                        qtable_changepos(path_X,item)
            
            print("game 500 / 500")
            print(f"X wins : {X_wins}")
            print(f"O wins : {O_wins}")
            print(f"Draws : {Draws}")

    #human wants to play
    else:
        exploration = 1

        player = input("What side would you like to start with? (X or O)")
        while player != "X" and player != "O":
            player = input("What side would you like to start with? (X or O)")

        movelist_X,movelist_O,board,winner = tictactoe(player,exploration)

        print_board(board)
        print("*"*30)
        print(f"winner : {winner}")

