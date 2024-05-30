from state import State
from board import board
from junk import*
import numpy as np
class BreakThrough:
    def __init__(self,state):
        self.state = state
    def is_end_of_game(self,state:State, fliped: int = None):
        if fliped:
            if fliped == -1:
                
                for i in range(8):
                    # print(state.board[7,i])
                    # print(state.board)
                    if state.board[7,i] == 0:
                        continue
                    if state.board[7,i] == 1:
                        return 'white won'
                for i in range(8):
                    # print(state.board[0,i])
                    if state.board[0,i] == 0:
                        continue
                    if state.board[0,i] == -1:
                        return 'black won'   
            elif fliped == 1:
                for i in range(8):
                    if state.board[0,i] == 0:
                        continue
                    if state.board[0,i] == 1:
                        return 'white won'
                for i in range(8):
                    if state.board[7,i] == 0:
                        continue
                    if state.board[7,i] == -1:
                        return 'black won'   
                
        else:
            for i in range(8):
                if state.board[0,i] == 0:
                    continue
                if state.board[0,i] == 1:
                    return 'white won'
            for i in range(8):
                if state.board[7,i] == 0:
                    continue
                if state.board[7,i] == -1:
                    return 'black won'  
        countW,countB = 0,0 
        for i in range(8):
            for h in range(8):
                if state.board[i,h] == 1:
                    countW+=1
                elif state.board[i,h] == -1:
                    countB+=1
        if countW == 0: return 'black won'
        if countB == 0: return 'white won'

        
        

    def is_legal(self,state:State,action,player = 0):
        pos,act = action
        row,col = pos
        p = state.board[row,col] 

        

        if p == 0:
            return False
        if p != state.player:
            return False
        if row  > 7 or row  < 0:
                return False
        if act == forward:
            
            if state.board[row + state.player*-1 ,col] != 0:
                return False
        elif act == dia_right:
            if col+1 >7 or col+1<0:
                return False
            
            if state.board[row + state.player*-1,col+1] != 0:
                if state.board[row + state.player*-1,col+1] == p:
                    return False
        elif act == dia_left:
            if col-1 >7 or col-1<0:
                return False
            if state.board[row + state.player*-1,col-1] != 0:
                if state.board[row + state.player*-1,col-1] == p:
                    return False
        return True
    def legal_moves(self,state: State, row_col):
        L_moves = []
        
        if self.is_legal(state,(row_col,forward)):
            L_moves.append((row_col,forward))
        if self.is_legal(state,(row_col,dia_right)):
            L_moves.append((row_col,dia_right))
        if self.is_legal(state,(row_col,dia_left)):
            L_moves.append((row_col,dia_left))
        return L_moves
        
    def all_legal_moves(self,state:State,player):
        all_moves = []
        for row in range(8):
            for col in range(8):
                if 0 == state.board[row,col]:
                    continue
                if player == state.board[row,col]:
                    all_moves.extend(self.legal_moves(state,(row,col)))
        return all_moves
    def move(self,action):
        pos,act = action
        row,col = pos
        p = self.state.board[row,col]
        if act == forward:
            self.state.board[row,col] = 0
            self.state.board[row + self.state.player*-1, col] = p
        elif act == dia_right:
            self.state.board[row,col] = 0
            self.state.board[row + self.state.player*-1, col + 1] = p
        elif act == dia_left:
            self.state.board[row,col] = 0
            self.state.board[row + self.state.player*-1, col - 1 ] = p
    def next_state(self,state: State , action):  
        pos,act = action
        row,col = pos

        new_state = State(state.board,state.player)
        if new_state.board[row,col] == 0:
            return new_state
        p = new_state.board[row,col]
        if act == forward:
            new_state.board[row,col] = 0
            new_state.board[row + new_state.player*-1, col] = p
        elif act == dia_right:
            new_state.board[row,col] = 0
            new_state.board[row + new_state.player*-1, col + 1] = p
        elif act == dia_left:
            new_state.board[row,col] = 0
            new_state.board[row + new_state.player*-1, col - 1 ] = p
        new_state.player = new_state.player*-1
       
        return new_state
 

        
    def reward (self, state : State, action = None,fliped = None) -> tuple:
        
        win = self.is_end_of_game(state,fliped=fliped)
        if win == "white won": 
            return 1, True
        if win == "black won":
            return -1, True
        return 0, False