from state import State
from BreakThrough import BreakThrough as env
import pygame
import numpy as np       


FPS = 60
WIDTH,HEIGHT =  600,600
ROWS,COLS = 8,8
square_size=75
line_width = 2
H_width,H_height = 600,100
M_width,M_height = 600,600
#RGB
black = (0,0,0)
white = (255,255,255)
cadet_blue=(152,245,255)
light_gray = (211,211,211)
green = (0,255,0)
red = (255,0,0)


class Graphics:
    
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.header_surf = pygame.Surface((H_width,H_height))
        self.main_surf = pygame.Surface((M_width,M_height))
        self.load_img()
        pygame.display.set_caption('breakThrough')
        

    
    def draw(self, state):
        self.header_surf.fill(cadet_blue)
        self.main_surf.fill(light_gray)
        
        self.draw_lines()
        self.draw_pieces(state)
        # if state.player == 1:
        #     self.write('player 1')
        # else:
        #     self.write('player 2')
        self.screen.blit(self.header_surf,(0,0))
        self.screen.blit(self.main_surf,(0,0))
        pygame.display.update()
    
    def __call__(self,state):
        self.draw(state)

    def draw_lines(self):
        for i in range(ROWS):
            pygame.draw.line(self.main_surf,black,(i*square_size,0),(i*square_size,WIDTH),width=line_width)
            pygame.draw.line(self.main_surf,black,(HEIGHT,i*square_size),(0 ,i*square_size),width=line_width)
    def load_img(self):
        b_pawn = pygame.image.load("AI\img\B_pawn.png")
        w_pawn = pygame.image.load("AI\img\W_pawn.png")
        self.b_pawn = pygame.transform.scale(b_pawn, (35,35))
        self.w_pawn = pygame.transform.scale(w_pawn, (35,35))
    def calc_pos(self,row_col):
        row, col = row_col
        x = col*square_size
        y = row*square_size
        return x,y
    def draw_piece(self,row_col,player):
        if player == 1:
            img = self.w_pawn
        elif player == -1:
            img = self.b_pawn

        x,y = self.calc_pos(row_col)
        self.main_surf.blit(img,(x+20,y+20))
    def draw_pieces(self,state: State):
        board = state.board
        for row in range(ROWS):
            for col in range(COLS):
                if board[row,col] != 0:
                    self.draw_piece((row,col), board[row,col])
    def calc_row_col(self,pos):
        x,y = pos
        if y<0:
            return None
        row = (y-H_height) // square_size
        col = x // square_size
        return row,col
    
    def nevo(self,pos):
        size = 75  # size of each square 
        width, height = 8 * size, 8 * size
        x,y = pos
        row = y // size
        col = x // size
        if 0 <= row < 8 and 0 <= col < 8:
            return row,col  # Return (x, y) in board coordinate
