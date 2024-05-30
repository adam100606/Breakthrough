from BreakThrough import BreakThrough
from state import State
class AlphaBeta_agent:

    
    def __init__(self, player, depth=2, env: BreakThrough = None):
        self.player = player
        self.opponent = player*-1
        self.depth = depth
        self.env: BreakThrough = env
    
    def evaluate(self, state: State, row, col):
       
        if state.board[row, col] == 1:
            return (7 - row) * 0.5
        elif state.board[row, col] == -1:
            return row * 0.5
        return 0

    def eval_state(self, state: State, player):
        
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
                    countF += self.pawn_safety(state, row, col, player)
                    countF += self.pawn_mobility(state, row, col, player)
                    countF += self.central_control(row, col)
                elif state.board[row, col] == -player:
                    countA += self.evaluate(state, row, col)
                    countA += self.pawn_safety(state, row, col, -player)
                    countA += self.pawn_mobility(state, row, col, -player)
                    countA += self.central_control(row, col)
        
        return countF - countA

    def pawn_safety(self, state: State, row, col, player):
       
        directions = [(-1, -1), (-1, 1)] if player == 1 else [(1, -1), (1, 1)]
        safety_value = 0.5
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and state.board[r, c] == player:
                return safety_value
        return 0

    def pawn_mobility(self, state: State, row, col, player):
       
        directions = [(-1, 0), (-1, -1), (-1, 1)] if player == 1 else [(1, 0), (1, -1), (1, 1)]
        mobility_value = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and state.board[r, c] == 0:
                mobility_value += 0.1
        return mobility_value

    def central_control(self, row, col):
        
        central_rows = [3, 4]
        central_cols = [3, 4]
        if row in central_rows and col in central_cols:
            return 0.2
        return 0

    def get_action(self, state: State):
        value, best_action = self.minMax(state, 0, float('-inf'), float('inf'))
        return best_action

    def minMax(self, state: State, depth, alpha, beta):
        return self.max_value(state, depth, alpha, beta)
    
    def max_value(self, state: State, depth, alpha, beta):
        if depth == self.depth or self.env.is_end_of_game(state):
            return self.eval_state(state, self.player), None
        
        value = float('-inf')
        best_action = None
        legal_actions = self.env.all_legal_moves(state, self.player)
        
        for action in legal_actions:
            new_state = self.env.next_state(state, action)
            new_value, _ = self.min_value(new_state, depth , alpha, beta)
            if new_value > value:
                value = new_value
                best_action = action
            if value >= beta:
                break
            alpha = max(alpha, value)

        return value, best_action

    def min_value(self, state: State, depth, alpha, beta):
        if depth == self.depth or self.env.is_end_of_game(state):
            return self.eval_state(state, self.player), None
        
        value = float('inf')
        best_action = None
        legal_actions = self.env.all_legal_moves(state, self.opponent)
        
        for action in legal_actions:
            new_state = self.env.next_state(state, action)
            new_value, _ = self.max_value(new_state, depth + 1, alpha, beta)
            if new_value < value:
                value = new_value
                best_action = action
            if value <= alpha:
                break
            beta = min(beta, value)

        return value, best_action

