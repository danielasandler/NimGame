from Random_Agent import Random_Agent
from Random_Agent import Random_Agent
from Nim import Nim
from Constant import *

class Tester:
    def __init__(self, env, player1, player2) -> None:
        self.env = env
        self.player1 = player1
        self.player2 = player2
        

    def test (self, games_num):
        env = self.env
        player = self.player1
        player1_win = 0
        player2_win = 0
        games = 0
        while games < games_num:
            action = player.get_Action(env=env,state=env.state, train = False)
            env.move(action, env.state)
            player = self.switchPlayers(player)
            if env.is_over(env.state):
                reward = env.reward(state=env.state)
                # score = env.state.score()
                if reward[0] > 0:
                    player1_win += 1
                elif reward[0] < 0:
                    player2_win += 1
                env.state = env.get_init_state((ROWS,COLS))
                games += 1
                player = self.player1
        return player1_win, player2_win        

    def switchPlayers(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def __call__(self, games_num):
        return self.test(games_num)

if __name__ == '__main__':
    env = Nim()
    player1 = Random_Agent(player=1, env=env)
    player2 = Random_Agent(player=2,env=env)
    test = Tester(env,player1, player2)
    print(test.test(100))
    player1 = Random_Agent(player=1,env=env)
    player2 = Random_Agent(player=2,env=env)
    test = Tester(env,player1, player2)
    print(test.test(100))