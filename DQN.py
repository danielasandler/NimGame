import torch
import torch.nn as nn
import torch.nn.functional as F
import copy
from Constant import ROWS, COLS

# Parameters
input_size = ROWS * COLS + 2 # state: board = 5 * 7 = 35 + action (2) = 37
layer1 = 64
# layer2 = 64
output_size = 1 # Q(state, action)
gamma = 0.90 


class DQN (nn.Module):
    def __init__(self, device = torch.device('cpu')) -> None:
        super().__init__()
        self.device = device
        self.linear1 = nn.Linear(input_size, layer1)
        # self.linear2 = nn.Linear(layer1, layer2)
        self.output = nn.Linear(layer1, output_size)
        self.MSELoss = nn.MSELoss()

    def forward (self, x):
        x = self.linear1(x)
        x = F.leaky_relu(x)
        # x = self.linear2(x)
        # x = F.leaky_relu(x)
        x = self.output(x)
        return x
    
    def loss (self, Q_value, rewards, Q_next_Values, Dones ):
        Q_new = rewards + gamma * Q_next_Values * (1- Dones)
        return self.MSELoss(Q_value, Q_new)
    
    def load_params(self, path):
        self.load_state_dict(torch.load(path))

    def save_params(self, path):
        torch.save(self.state_dict(), path)

    def copy (self):
        return copy.deepcopy(self)

    def __call__(self, states, actions):
        states[states==-1]=0
        state_action = torch.cat((states,actions), dim=1)
        return self.forward(state_action)