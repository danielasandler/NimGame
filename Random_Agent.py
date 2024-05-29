import numpy as np
from State import State
from Graphics import *
from Nim import Nim
import random

class Random_Agent:
    def __init__(self, player: int, env: Nim=None) -> None:
        self.player = player
    
    def get_Action(self, event = None, graphics= None, state : State= None, env:Nim = None, train= None):
        action = random.choice(env.getLegalActions(state))
        return action

