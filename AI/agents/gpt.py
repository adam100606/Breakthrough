from BreakThrough import BreakThrough
from state import State

class MinMaxAgentGPT:
    def __init__(self, player, depth=2, env=None):
        self.player = player
        self.opponent = -player
        self.depth = depth
        self.env = env
    
    def evaluate(self, state, row, col):
        if state.board[row, col] == 1:
            return (7 - row) * 0.5
        elif state.board[row, col] == -1:
            return row * 0.5
        return 0
    
    def eval_state(self, state, player):
        countF = 0
        countA = 0
        end = self.env.is_end_of_game(state)
        if end:
            if (end == 'white won' and player == 1) or (end == 'black won' and player == -1):
                return 100000
            else:
                return -100000
        for row in range(8):
            for col in range(8):
                if state.board[row, col] == player:
                    countF += self.evaluate(state, row, col)
                elif state.board[row, col] == -player:
                    countA += self.evaluate(state, row, col)
        return countF - countA
    
    def get_action(self, state):
        value, best_action = self.minMax(state)
        return best_action
    
    def minMax(self, state):
        visited = set()
        depth = 0
        return self.max_value(state, visited, depth)
    
    def max_value(self, state, visited, depth):
        if depth == self.depth or self.env.is_end_of_game(state):
            return self.eval_state(state, self.player), None
        
        value = float('-inf')
        best_action = None
        legal_actions = self.env.all_legal_moves(state, self.player)
        
        for action in legal_actions:
            new_state = self.env.next_state(state, action)
            if new_state not in visited:
                visited.add(new_state)
                new_value, _ = self.min_value(new_state, visited, depth )
                if new_value > value:
                    value = new_value
                    best_action = action

        return value, best_action
    
    def min_value(self, state, visited, depth):
        if depth == self.depth or self.env.is_end_of_game(state):
            return self.eval_state(state, self.player), None
        
        value = float('inf')
        best_action = None
        legal_actions = self.env.all_legal_moves(state, self.opponent)
        
        for action in legal_actions:
            new_state = self.env.next_state(state, action)
            if new_state not in visited:
                visited.add(new_state)
                new_value, _ = self.max_value(new_state, visited, depth + 1)
                if new_value < value:
                    value = new_value
                    best_action = action

        return value, best_action
