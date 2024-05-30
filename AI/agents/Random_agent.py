from BreakThrough import BreakThrough
import pygame
from graphics import *
import random
from junk import *
from state import State
class random_agent:
    def __init__(self, player, env: BreakThrough):
        self.env = env
        self.player = player
        

    def get_action(self, state: State):
        actions = self.env.all_legal_moves(state, self.player)
        return random.choice(actions)
        # while(True):
        #     row =  random.randint(0,7)
        #     col =  random.randint(0,7)
        #     if state.board[row,col] != 0:
        #         if state.board[row,col] == self.player:
        #             move = random.randint(1,3)
        #             if move == 1:
        #               return ((row,col),dia_left)
        #             if move == 2:
        #                 return ((row,col),forward)
        #             if move == 3:
        #                 return ((row,col),dia_right)

    def __call__(self, events):
        return self.get_action(events)
     