import numpy as np
from State import State
from Graphics import *

class Nim:
    def __init__(self, state:State = None) -> None:
        if state == None:
            self.state = self.get_init_state((ROWS, COLS))
        else:
            self.state = state

    def get_init_state(self, Rows_Cols):
        rows, cols = Rows_Cols
        board = np.zeros([rows, cols],int)
        for i in range(cols):
            board[0][i] = 1
        for i in range(cols):
            board[rows-1][i] = 2
        

        return State (board, 1)

    # def is_free(self, row_col: tuple[int, int], state: State):
    #     row, col = row_col
    #     return state.board[row, col] == 0

    def is_legal(self,action,state:State):
        row,col = action
        if state.board[row, col] != 0:
            return False
        return True
        
    def get_next_state (self, action, state):
        next_state = state.copy()
        self.move(action,next_state)
        return next_state

    def move (self, action, state:State):
        row,col=action
        if not self.is_legal(action,state):
            return False
        for i in range(ROWS):
            if state.board[i][col]==state.player:
                state.board[i][col] = 0
                break
        state.board[action] = state.player
        for i in range(ROWS):
            if state.board[i][col]==1:
                p1_row, p1_col = i, col
            if state.board[i][col]==2:
                p2_row,p2_col = i,col
        for i in range(ROWS):
            if i<p1_row or i>p2_row:
                state.board[i][col]=-1
        if state.player==1:
            state.player= 2
        else:
            state.player = 1
        return True

    def is_over(self,state:State): #מי שעושה את המהלך האחרון מנצח
        legal_actions = self.getLegalActions(state)
        if len(legal_actions) == 0:
            return True
        return False
    
    def getLegalActions(self, state:State):
        zeros = np.where(state.board == 0)
        legal_actions = list(zip(zeros[0], zeros[1]))
        return legal_actions
    
    def getDifferentCols(self, state:State):
        pass
    
    # def freeInCols(self, state:State):#לבדוק
    #     board = state.board
    #     free = np.count_nonzero(board == 0, axis=0)
    #     print (np.unique(free, return_index=True))
    #     difPossibilities,difColsIndex = np.unique(free, return_index=True)
    #     return difPossibilities,difColsIndex
    
    def reward (self, state : State, action = None) -> tuple:
        if action:
            next_state = self.get_next_state(action, state)
        else:
            next_state = state
        if (self.is_over(next_state)):
            if next_state.player==1:
                return -1, True
            else:  #self.state.player!=state.player
                return 1, True
        return 0, False
        
        