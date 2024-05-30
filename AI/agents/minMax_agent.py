from BreakThrough import BreakThrough
from state import State
class minMax_agent:
    def __init__(self, player, depth = 2, env: BreakThrough = None):
        self.player = player
        if self.player == 1:
            self.opponent = -1
        else:
            self.opponent = 1
        self.depth = depth
        self.env : BreakThrough = env
    def evaluate(self, state: State, row, col):
        """
        Evaluates the value of a pawn based on its position on the board.
        """
        if state.board[row, col] == 1:
            return (7 - row) * 0.5
        elif state.board[row, col] == -1:
            return row * 0.5
        return 0

    def eval_state(self, state: State, player):
        """
        Evaluates the overall state of the board for the given player.
        """
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
        """
        Evaluates the safety of a pawn by checking if it is protected by another pawn.
        """
        directions = [(-1, -1), (-1, 1)] if player == 1 else [(1, -1), (1, 1)]
        safety_value = 0.5
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and state.board[r, c] == player:
                return safety_value
        return 0

    def pawn_mobility(self, state: State, row, col, player):
        """
        Evaluates the mobility of a pawn by counting its possible moves.
        """
        directions = [(-1, 0), (-1, -1), (-1, 1)] if player == 1 else [(1, 0), (1, -1), (1, 1)]
        mobility_value = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and state.board[r, c] == 0:
                mobility_value += 0.1
        return mobility_value

    def central_control(self, row, col):
        """
        Evaluates the control of central squares.
        """
        central_rows = [3, 4]
        central_cols = [3, 4]
        if row in central_rows and col in central_cols:
            return 0.2
        return 0
                    
                
    def get_action(self, state: State):
        value, bestAction = self.minMax(state)
        return bestAction

    def minMax(self, state:State):
        visited = set()
        depth = 0
        return self.max_value(state, visited, depth)
        
    def max_value (self, state:State, visited:set, depth):
        
        value = -1000

        # stop state
        if depth == self.depth or self.env.is_end_of_game(state):
            value = self.eval_state(state,state.player)
            return value, state.action
        
        # start recursion
        bestAction = None
        legal_actions = self.env.all_legal_moves(state,state.player)
        for action in legal_actions:
            newState = self.env.next_state(state,action)
            if newState not in visited:
                visited.add(newState)
                newState.action = action
                newValue, newAction = self.min_value(newState, visited,  depth + 1)
                if newValue > value:
                    value = newValue
                    bestAction = action

        return value, bestAction 

    def min_value (self, state:State, visited:set, depth):
        
        value = 1000

        # stop state
        if depth == self.depth or self.env.is_end_of_game(state):
            value = self.eval_state(state,state.player)
            return value, state.action
        
        # start recursion
        bestAction = None
        legal_actions = self.env.all_legal_moves(state,state.player)
        for action in legal_actions:
            newState = self.env.next_state(state,action)
            if newState not in visited:
                visited.add(newState)
                newState.action = action
                newValue, newAction = self.max_value(newState, visited,  depth + 1)
                if newValue < value:
                    value = newValue
                    bestAction = action

        return value, bestAction 

