from Nim import Nim
from DQN_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from Random_Agent import Random_Agent
# from Fix_Agent import Fix_Agent
import torch
from Tester import Tester
from Constant import * 
from AlphaBetaAgent import AlphaBetaAgent
import os
# import wandb


# File_Num = '4'
# path_load= None
# path_Save=f'Data/params_{File_Num}.pth'
# path_best = f'Data/best_params_{File_Num}.pth'
# buffer_path = f'Data/buffer_{File_Num}.pth'
# results_path=f'Data/results_{File_Num}.pth'
# random_results_path = f'Data/random_results_{File_Num}.pth'
# path_best_random = f'Data/best_random_params_{File_Num}.pth'


def main ():
    
    epochs = 2000000
    start_epoch = 0
    C = 100
    learning_rate = 0.001
    batch_size = 64
    env = Nim()
    MIN_Buffer = 4000

    player1 = DQN_Agent(player=1, env=env)
    player_hat = DQN_Agent(player=1, env=env, train=False)
    Q = player1.DQN
    Q_hat = Q.copy()
    player_hat.DQN = Q_hat

    player2 = DQN_Agent(player=2, env=env)
    player2.DQN = Q

    buffer = ReplayBuffer(path=None) # None
        
    results, avgLosses = [], [] 
    avgLoss, loss, loss_count = 0, 0, 0
    res, best_res = 0, -100
       
    tester1 = Tester(env=env, player1=player1, player2=Random_Agent(player=2, env=env))
    tester2 = Tester(env=env, player1=Random_Agent(player=1, env=env), player2= player2)

    # init optimizer
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optim,100000*30, gamma=0.90)
    # scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[30*50000, 30*100000, 30*250000, 30*500000], gamma=0.5)



    ######### checkpoint Load ############
    num = 300
    checkpoint_path = f"Data/checkpoint{num}.pth"
    buffer_path = f"Data/buffer{num}.pth"
    resume = False
    if os.path.exists(checkpoint_path):
        resume = True
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch']+1
        player1.DQN.load_state_dict(checkpoint['model_state_dict'])
        player2.DQN.load_state_dict(checkpoint['model_state_dict'])
        player_hat.DQN.load_state_dict(checkpoint['model_state_dict'])
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        buffer = torch.load(buffer_path)
        results = checkpoint['results']
        avgLosses = checkpoint['avglosses']
    player1.DQN.train()
    player_hat.DQN.eval()


    
    for epoch in range(start_epoch, epochs):
        print(f'epoch = {epoch}', end='\r')
        state_1 = env.get_init_state((ROWS,COLS))
        step = 0
        state_2 = None
        while not env.is_over(state_1):
            step += 1
            # Sample Environement
            action_1 = player1.get_Action(state_1, epoch=epoch,env = env)
            after_state_1 = env.get_next_state(state=state_1, action=action_1)
            reward_1, end_of_game_1 = env.reward(after_state_1)
            if state_2:
                buffer.push(state_2, action_2, -reward_1, after_state_1, end_of_game_1)
            if end_of_game_1:
                res += reward_1
                buffer.push(state_1, action_1, reward_1, after_state_1, True)
                break
            state_2 = after_state_1
            action_2 = player2.get_Action(state=state_2,env=env)
            after_state_2 = env.get_next_state(state=state_2, action=action_2)
            reward_2, end_of_game_2 = env.reward(state=after_state_2)
            if end_of_game_2:
                res += reward_2
                buffer.push(state_2, action_2, -reward_2, after_state_2, True)
            buffer.push(state_1, action_1, reward_2, after_state_2, end_of_game_2)
            
            state_1 = after_state_2
 
            if len(buffer) < MIN_Buffer:
                continue
            
            # Train NN
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = Q(states, actions)
            next_actions = player_hat.get_Actions(next_states, dones) #fixed bug
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_states, next_actions) #todo: use the values calculated in get_Actions

            loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            
            scheduler.step()
            if loss_count <= 1000:
                avgLoss = (avgLoss * loss_count + loss.item()) / (loss_count + 1)
                loss_count += 1
            else:
                avgLoss += (loss.item()-avgLoss)* 0.00001 
            
        if epoch % C == 0:
                Q_hat.load_state_dict(Q.state_dict())

        if (epoch+1) % 100 == 0:
            print(f'\nres= {res}')
            avgLosses.append(avgLoss)
            results.append(res)
            if best_res < res:      
                best_res = res
            res = 0

        if (epoch+1) % 500 == 0:
            print(f'tester1: {tester1(100)} tester2:{tester2(100)}')


        if (epoch+1) % 2000 == 0:
            # torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player1.DQN.state_dict(),
                'optimizer_state_dict': optim.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'results': results,
                'avglosses': avgLosses
            }
            torch.save(buffer, buffer_path)
            torch.save(checkpoint, checkpoint_path)
            # player1.save_param(path_Save)

        
        print (f'epoch={epoch} step={step} loss={loss:.5f} avgloss={avgLoss:.5f}', end=" ")
        print (f'learning rate={scheduler.get_last_lr()[0]} path={checkpoint_path} res= {res} best_res = {best_res}')

    # torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
    torch.save(checkpoint, checkpoint_path)
    torch.save(buffer, buffer_path)


if __name__ == '__main__':
    main()


