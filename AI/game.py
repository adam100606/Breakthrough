
import pygame
import numpy as np
from state import State
from graphics import *
from BreakThrough import BreakThrough
from agents.human_agent import human_agent 
from agents.Random_agent import random_agent
from agents.minMax_agent import minMax_agent
from agents.alphaBeta_agent import AlphaBeta_agent
from agents.gpt import MinMaxAgentGPT
from DQN_agent import DQN_Agent
import time

pygame.init()
clock = pygame.time.Clock()
graphics = Graphics()
env = BreakThrough(State())

# player1 = random_agent(1,env,graphics)
# player2 = random_agent(-1,env,graphics)


# player1 = human_agent(1,env,graphics)
# player2 = human_agent(-1,env,graphics)


player1 = minMax_agent(1,2,env)
# player2 = MinMaxAgentGPT(-1,2,env)


# player1 = AlphaBeta_agent(1,5,env)
player2 = AlphaBeta_agent(-1,3,env)

# player1 = DQN_Agent(player=1,parametes_path=f'data\params_4.pth',train=False ,env=env)
# player2 = DQN_Agent(player=-1,parametes_path=f'data\params_1.pth',train=False,env=env)

# player1 = minMax_agent_gpt(-1,4,env)
player = player1

def switch_players(player, state:State):
    state.player = state.player* -1 
    if player == player1:
        return player2
    else:
        return player1

def main():
    run = True
    player = player1
    while(run):
        action = player.get_action(env.state)
        
        if action:
            print(action)
            # if env.is_legal(env.state,action):
            env.move(action)
            graphics.draw_pieces(env.state)
            pygame.display.flip()
            # print(env.state.board)
            player = switch_players(player,env.state)      
            player.LST = []
            
              
        if env.is_end_of_game(env.state):
            print(env.is_end_of_game(env.state))
            
            run = False
        graphics(env.state)
        clock.tick(FPS)
        time.sleep(0.1)
        
    



 
     

if __name__ == '__main__':
    main()