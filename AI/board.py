import numpy as np

class board:
    def __init__(self):
        board = np.zeros((8,8),dtype=int)
        
    def init_board():
        board = np.zeros((8,8),dtype=int)
        
        for h in range(2):
            for i in range(8):
                board[h,i] = -1
        for h in range(6,8):
            for i in range(8):
                board[h,i] = 1
        return board

    def set_board(board):
        board = np.zeros((8,8),dtype=int)
        
        for h in range(2):
            for i in range(8):
                board[h,i] = -1
        for h in range(6,8):
            for i in range(8):
                board[h,i] = 1


    
