import numpy as np
import torch
from Constant import ROWS, COLS

class State:
    def __init__(self, board= None, player = 1) -> None:
        self.board = board
        self.player = player
        self.action : tuple[int, int] = None
        self.value=0

    def get_opponent (self):
        if self.player == 1:
            return 2
        else:
            return 1

    def switch_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def score (self, player = 1) -> tuple[int, int]:
        if player == 1:
            opponent = 2
        else:
            opponent = 1

        player_score = np.count_nonzero(self.board == player)
        opponent_score = np.count_nonzero(self.board == opponent)
        return player_score, opponent_score

    def score (self):
        pass

    def __eq__(self, other) ->bool:
        return np.equal(self.board, other.board).all() and self.player == other.player

    def __hash__(self) -> int:
        return hash(repr(self.board) + repr(self.player))
    
    def copy (self):
        newBoard = np.copy(self.board)
        return State(board=newBoard, player=self.player)
    
    def getLegalActions(self):
        zeros = np.where(self.board == 0)
        legal_actions = list(zip(zeros[0], zeros[1]))
        return legal_actions
    
    def toTensor (self, device = torch.device('cpu')) -> tuple:
        board_np = self.board.reshape(-1)
        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        return board_tensor
    
    def tensorToState (state_tensor, player):
        board_tensor = state_tensor
        board = board_tensor.reshape(shape=(ROWS,COLS)).cpu().numpy()
        return State(board, player=player)