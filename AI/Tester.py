from agents.Random_agent import random_agent
from BreakThrough import BreakThrough
from state import State 
from graphics import *

class Tester:
    def __init__(self, env:BreakThrough, player1, player2) -> None:
        self.env = env
        self.player1 = player1
        self.player2 = player2
        

    def tester (self, games_num):
        env = self.env
        player = self.player1
        player1_win = 0
        player2_win = 0
        games = 0
        while games < games_num:
            action = player.get_action(env.state)
            if env.is_legal(env.state,action):
                env.move(action)
                player = self.switch_players(player,env.state)
           
            if env.is_end_of_game(env.state):
                score = env.state.player
                if score > 0:
                    player1_win += 1
                elif score < 0:
                    player2_win += 1
                env.state = State()
                games += 1
                player = self.player1
        return player1_win, player2_win        

    def switch_players(self,player, state:State):
        state.player = state.player* -1 
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def __call__(self, games_num):
        return self.tester(games_num)

if __name__ == '__main__':
    brah = BreakThrough(State())
    player1 = random_agent(  1, brah , graphics=None)
    player2 = random_agent( -1, brah, graphics=None)
    test = Tester(brah,player1, player2)
    print(test.tester(1))
    # player1 = Fix_Agent(env, player=1)
    # player2 = Random_Agent(env, player=-1)
    # test = Tester(env,player1, player2)
    # print(test.test(100))