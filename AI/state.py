import numpy as np
import torch
from board import board as b
from junk import *

class State:
    def __init__(self,board = None, player = 1,act = None) -> None:
        if board is not None: 
            self.board = self.copy_board(board)
            
        else:
            self.board = b.init_board()
        self.player = player
        self.action = act


    def copy_board(self,board):
        new_board = np.zeros((8,8),dtype=int)
        for row in range(8):
            for col in range(8):
                new_board[row,col] = board[row,col]
        return new_board

    def flip(self):
        new_board = np.zeros((8,8),dtype=int)
        for row in range(8):
            for col in range(8):
                new_board[row,col] = self.board[7-row,7-col]*-1
        
        return State(new_board,self.player)
        

    def toTensor (self, device = torch.device('cpu')) -> tuple:
        board_np = self.board.reshape(-1)
        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        return board_tensor

    [staticmethod]
    def TensorToState(state_tensor,player):
         board = state_tensor.reshape([8,8]).cpu().numpy()
         return State(board,player=player)

    