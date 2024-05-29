from Nim import Nim
from State import State
import numpy as np
MAXSCORE = 5

class MinMaxAgent:
    def __init__(self, player, depth = 1, environment: Nim = None):
        self.player = player
        if self.player == 1:
            self.opponent = 2
        else:
            self.opponent = 1
        self.depth = depth
        self.env : Nim = environment


    def evaluate(self,state):
        zero_counts = np.sum(state.board == 0, axis=0)
        result = np.bitwise_xor.reduce(zero_counts)
        if self.player == state.player:
            if result == 0:
                return -1
            else:
                return 1
        else:
            if result == 0:
                return 1
            else:
                return -1
    
    def get_Action(self, event, graphics, state: State, env):
        value, bestAction = self.minMax(state)
        return bestAction

    def minMax(self, state:State):
        visited = {}
        depth = 0
        return self.max_value(state, visited, depth)
        
    def max_value (self, state:State, visited:set, depth):
        
        value = -MAXSCORE

        # stop state
        if depth == self.depth or self.env.is_over(state):
            value = self.evaluate(state)
            return value, state.action
        
        # start recursion
        bestAction = None
        legal_actions = self.env.getLegalActions(state)
        for action in legal_actions:
            newState = self.env.get_next_state(action, state)
            if newState not in visited:
                newValue, newAction = self.min_value(newState, visited,  depth + 1)
                visited[newState] = newValue
            else:
                newValue = visited[newState]
            if newValue > value:
                value = newValue
                bestAction = action

        return value, bestAction 

    def min_value (self, state:State, visited:set, depth):
        
        value = MAXSCORE

        # stop state
        if depth == self.depth or self.env.is_over(state):
            value = self.evaluate(state)
            return value, state.action
        
        # start recursion
        bestAction = None
        legal_actions = self.env.getLegalActions(state)
        for action in legal_actions:
            newState = self.env.get_next_state(action, state)
            if newState not in visited:
                newValue, newAction = self.max_value(newState, visited,  depth + 1)
                visited[newState] = newValue

            else:
                newValue = visited[newState]
                
            if newValue < value:
                value = newValue
                bestAction = action


        return value, bestAction 



