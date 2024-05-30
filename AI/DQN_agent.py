import torch
import random
import math
from DQN import DQN
from junk import *
from state import State
from BreakThrough import BreakThrough 
from state import *
class DQN_Agent:
    def __init__(self, player = 1, parametes_path = None, train = True, env:BreakThrough = None):
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.player = player
        self.train = train
        self.setTrainMode()
        self.env= env

    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_action (self, state:State, epoch = 0, events= None, train = True, graphics = None, black_state = None) -> tuple:
        
        actions =  self.env.all_legal_moves(state,state.player)
        if self.train and train:
            epsilon = self.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                return random.choice(actions)
        
        # if self.player == 1:
        #     state_tensor, action_tensor = state.toTensor()
        # elif not black_state:
        #     black_state = state.reverse()
        #     state_tensor, action_tensor = black_state.toTensor()
        # else:
        #     state_tensor, action_tensor = black_state.toTensor()
        state_tensor = state.toTensor()
        actions_list = [[*t[0],t[1]] for t in actions]
        action_tensor = torch.tensor(actions_list,dtype=torch.float32)
        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(action_tensor),1))
        # print(len(expand_state_tensor))
        # print(len(action_tensor))
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, action_tensor)
            
        max_index = torch.argmax(Q_values)
        return actions[max_index]

    def get_Actions (self, states_tensor: State, dones) -> torch.tensor:
        actions = []
        for i, tensor in enumerate(states_tensor):
            if dones[i].item():
                actions.append([0,0,0])
            else:
                state = State.TensorToState(tensor, self.player)
                action = self.get_action(state, train=False)
                actions.append([*action[0], action[1]])
        return torch.tensor(actions)

    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res
    
    def loadModel (self, file):
        self.model = torch.load(file)
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None, state=None):
        return self.get_action(state)