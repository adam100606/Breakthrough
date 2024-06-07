import pygame
from graphics import Graphics
from BreakThrough import BreakThrough
from agents.human_agent import human_agent
from agents.minMax_agent import minMax_agent
from agents.alphaBeta_agent import AlphaBeta_agent
from DQN import DQN
from DQN_agent import DQN_Agent
from state import State
from agents.Random_agent import random_agent
import torch

# Define constants
WIDTH, HEIGHT = 600, 600
BLACK = (0, 0, 0)
FPS = 60

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create environment and graphics
environment = BreakThrough(State())
graphics = Graphics()

def switch_players(player, state:State,p1,p2):
    state.player = state.player* -1 
    if player == p1:
        return p2
    else:
        return p1


def game(p1, p2):
    run = True
    global player1, player2
    player1 = p1
    player2 = p2
    environment.state.player = 1
    player = player1
    graphics.draw(environment.state)
    while run:
        action = player.get_action(environment.state)

        if action:
            print(action)
            environment.move(action)
            graphics.draw_pieces(environment.state)
            pygame.display.flip()
            player = switch_players(player, environment.state,p1,p2)
            player.LST = []
        graphics.draw(environment.state)
        pygame.display.update()
        if environment.is_end_of_game(environment.state):
            print(environment.is_end_of_game(environment.state))
            run = False
        
        graphics.draw_pieces(environment.state)
        clock.tick(FPS)

def main():
    global player1, player2
    player1 = human_agent(player=1, graphics=graphics, env=environment)
    player2 = human_agent(player=2, graphics=graphics, env=environment)

    colors = [['gray', 'gray', 'gray', 'gray','gray'], ['gray', 'gray', 'gray', 'gray','gray']]
    player1_chosen = 0
    player2_chosen = 0
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 200 < pos[0] < 400 and 500 < pos[1] < 540:
                    game(player1, player2)
                if 10 < pos[0] < 210 and 200 < pos[1] < 240:
                    player1 = human_agent(player=1, graphics=graphics, env=environment)
                    player1_chosen = 0
                if 400 < pos[0] < 600 and 200 < pos[1] < 240:
                    player2 = human_agent(player=-1, graphics=graphics, env=environment)
                    player2_chosen = 0
                if 10 < pos[0] < 210 and 250 < pos[1] < 290:
                    player1 = minMax_agent(player=1, depth=2, env=environment)
                    player1_chosen = 1
                if 400 < pos[0] < 600 and 250 < pos[1] < 290:
                    player2 = minMax_agent(player=-1, depth=2, env=environment)
                    player2_chosen = 1
                if 10 < pos[0] < 210 and 300 < pos[1] < 340:
                    player1 = AlphaBeta_agent(player=1, depth=1, env=environment)
                    player1_chosen = 2
                if 400 < pos[0] < 600 and 300 < pos[1] < 340:
                    player2 = AlphaBeta_agent(player=-1, depth=1, env=environment)
                    player2_chosen = 2
                if 10 < pos[0] < 210 and 350 < pos[1] < 390:
                    player1 = DQN_Agent(player=1,parametes_path='', train=False, env=environment)
                    player1_chosen = 3
                if 400 < pos[0] < 600 and 350 < pos[1] < 390:
                    player2 = DQN_Agent(player=-1,parametes_path='',train=False, env=environment)
                    player2_chosen = 3
                if 10 < pos[0] < 210 and 400 < pos[1] < 440:
                    player1 = random_agent(player=1, env=environment)
                    player1_chosen = 4
                if 400 < pos[0] < 600 and 400 < pos[1] < 440:
                    player2 = random_agent(player=-1, env=environment)
                    player2_chosen = 4


        colors = [['gray', 'gray', 'gray', 'gray','gray'], ['gray', 'gray', 'gray', 'gray','gray']]
        colors[0][player1_chosen] = 'blue'
        colors[1][player2_chosen] = 'blue'

        win.fill('LightGray')
        write(win, "BreakThrough", pos=(200, 50), color=BLACK)

        write(win, 'Player 1', (30, 150), color=BLACK)
        pygame.draw.rect(win, colors[0][0], (10, 200, 200, 40))
        write(win, 'Human', (30, 200), color=BLACK)
        pygame.draw.rect(win, colors[0][1], (10, 250, 200, 40))
        write(win, 'Min_Max', (30, 250), color=BLACK)
        pygame.draw.rect(win, colors[0][2], (10, 300, 200, 40))
        write(win, 'Alpha_Beta', (30, 300), color=BLACK)
        pygame.draw.rect(win, colors[0][3], (10, 350, 200, 40))
        write(win, 'DQN', (30, 350), color=BLACK)
        pygame.draw.rect(win, colors[0][4], (10, 400, 200, 40))
        write(win, 'random', (30, 400), color=BLACK)

        write(win, 'Player 2', (450, 150), color=BLACK)
        pygame.draw.rect(win, colors[1][0], (400, 200, 200, 40))
        write(win, 'Human', (420, 200), color=BLACK)
        pygame.draw.rect(win, colors[1][1], (400, 250, 200, 40))
        write(win, 'Min_Max', (420, 250), color=BLACK)
        pygame.draw.rect(win, colors[1][2], (400, 300, 200, 40))
        write(win, 'Alpha_Beta', (420, 300), color=BLACK)
        pygame.draw.rect(win, colors[1][3], (400, 350, 200, 40))
        write(win, 'DQN', (420, 350), color=BLACK)
        pygame.draw.rect(win, colors[1][4], (400, 400, 200, 40))
        write(win, 'random', (420, 400), color=BLACK)

        pygame.draw.rect(win, 'gray', (200, 500, 200, 40))
        write(win, 'Play', (250, 500), color=BLACK)

        pygame.display.update()

    pygame.quit()

def write(surface, text, pos=(50, 20), color=BLACK, background_color=None):
    font = pygame.font.SysFont("arial", 36)
    text_surface = font.render(text, True, color, background_color)
    surface.blit(text_surface, pos)

if __name__ == '__main__':
    main()
