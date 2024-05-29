import pygame
from Graphics import *
from Nim import Nim
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from MinMaxAgent import MinMaxAgent
from AlphaBetaAgent import AlphaBetaAgent
from DQN_Agent import DQN_Agent
import time

FPS = 60

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Nim')
env = Nim()


graphics = Graphics(win, board = env.state.board)
# player2 = Human_Agent(player=2)
player1 = Human_Agent(player=1)
# player1 = Random_Agent(player=1)
player2 = Random_Agent(player=2)

# player2 = MinMaxAgent(player=2,environment=env,depth=4)
# player1 = MinMaxAgent(player=1,environment=env,depth=4)
# player1 = DQN_Agent(player=1,env=env, train=False,parametes_path='Data\params_104.pth')
# player2 = DQN_Agent(player=2,env=env, train=False,parametes_path='Data\params_104.pth')

# player1 = AlphaBetaAgent(player=1,environment=env, depth = 3)
# player2 = AlphaBetaAgent(player=2,environment=env, depth = 1)
def main ():
    start = time.time()
    run = True
    clock = pygame.time.Clock()
    graphics.draw()
    player = player1
    
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
        
        action = player.get_Action(event=event, graphics= graphics,state = env.state, env=env)
        if action:
            if env.move(action,env.state):
                player=switchPlayers(player,env)
                #env.freeInCols(env.state)
                #print(env.getLegalActions(env.state))
                # pygame.time.delay(200)
                
        graphics.draw()
        pygame.display.update()
        if env.is_over(env.state):
    # time.sleep(2)
            pygame.quit()
            print("End of game")
            print("Winner: ", env.state.get_opponent())
            # score1, score2 = env.state.score()
            # print ("player 1: score = ", score1)
            # print ("player 2: score = ", score2)
            print (time.time() - start)
            run = False


def switchPlayers(player,env:Nim):
    if player == player1:
    #    env.state.player=2
       return player2
    else:
        # env.state.player=1
        return player1

if __name__ == '__main__':
    main()
    
