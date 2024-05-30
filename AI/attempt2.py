from BreakThrough import BreakThrough
from state import State
from DQN_agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from agents.Random_agent import random_agent
from agents.alphaBeta_agent import AlphaBeta_agent

import torch
from Tester import Tester

epochs = 2000000
start_epoch = 0
C = 30
learning_rate = 0.1
batch_size = 64
env = BreakThrough(State())
MIN_Buffer = 4000

File_Num = 1
path_load = None
# path_load= f'data\params_1.pth'
path_Save=f'Data/params_{File_Num}.pth'
path_best = f'Data/best_params_{File_Num}.pth'
buffer_path = f'Data/buffer_{File_Num}.pth'
results_path=f'Data/results_{File_Num}.pth'
random_results_path = f'Data/random_results_{File_Num}.pth'
path_best_random = f'Data/best_random_params_{File_Num}.pth'



def main ():
    
    player1 = DQN_Agent(player=1, env=env,parametes_path=path_load)
    player_hat = DQN_Agent(player=1, env=env, train=False)
    Q = player1.DQN
    Q_hat = Q.copy()
    Q_hat.train = False
    player_hat.DQN = Q_hat
    check = True
    # player2 = Fix_Agent(player=-1, env=env, train=True, random=0)   #0.1
    player2 = AlphaBeta_agent(player=-1, depth=3   , env=env)   
    buffer = ReplayBuffer(path=None) # None
    
    results_file = torch.load(results_path)
    results = results_file['results'] # []
    avgLosses = results_file['avglosses']     #[]
    avgLoss = avgLosses[-1] #0
    loss = 0
    res = 0
    game = 0
    best_res = -200
    loss_count = 0
    # tester = Tester(player1=player1, player2=random_agent(player=-1, env=env), env=env)
    # tester_fix = Tester(player1=player1, player2=player2, env=env)
    random_results = [] #torch.load(random_results_path)   # []
    best_random = 0 #max(random_results)
    
    
    # init optimizer
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optim,100000*30, gamma=0.99)
    # scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[30*50000, 30*100000, 30*250000, 30*500000], gamma=0.5)
    
    for epoch in range(start_epoch, epochs):
        print(f'epoch = {epoch}', end='\r')
        state = State()
        step = 0
        fliped = 1
        
        while  not env.is_end_of_game(state):
            # Sample Environement
            # print(state.board)
            
            step +=0.5
            action = player1.get_action(state, epoch=epoch)
            after_state = env.next_state(state=state, action=action)
            # reward, end_of_game = env.reward(after_state)
            rewardA = Reward(step=step,state=after_state)
            reward,end = rewardA
            if end:
                
                res += reward
                game += 1
                buffer.push(state, action, reward, after_state, True)
                break
            
            
            # print(action_1)
            buffer.push(state, action, reward*fliped, after_state, False)
            state = after_state.flip()
            fliped *= -1
            

            if len(buffer) < 2000: #MIN_Buffer:
                continue
            
            # Train NN
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = Q(states, actions)
            next_actions = player_hat.get_Actions(next_states, dones) 
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_states, next_actions) 

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
        #         if best_res > 75 and tester_fix(1) == (1,0):
        #             player1.save_param(path_best)
            res = 0
            game = 0

        # if (epoch+1) % 1000 == 0:
        #     test = tester(100)
        #     test_score = test[0]-test[1]
        #     if best_random < test_score and tester_fix(1) == (1,0):
        #         best_random = test_score
        #         player1.save_param(path_best_random)
        #     print(test)
        #     random_results.append(test_score)

        if (epoch+1) % 5000 == 0:
            torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
            torch.save(buffer, buffer_path)
            player1.save_param(path_Save)
            torch.save(random_results, random_results_path)
        
        print (f'epoch={epoch} step={step} loss={loss:.5f} avgloss={avgLoss:.5f}', end=" ")
        print (f'learning rate={scheduler.get_last_lr()[0]} path={path_Save} res= {res} game= {game} best_res = {best_res}')

    torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
    torch.save(buffer, buffer_path)
    torch.save(random_results, random_results_path)

def Reward(step, state:State):
    
    if env.is_end_of_game(state=state):
                if (step/0.5)%2:
                    return -1,True
                else:
                    return 1,True
    else:
         countW,countB = 0,0
         for i in range(8):
              for h in range(8):
                    if state.board[i,h] == 1:
                        countW += evaluate(state=state,row=i,col=h)
                    elif state.board[i,h] == -1:
                        countB += evaluate(state=state,row=i,col=h)
    if countW - countB == 0:
        return 0 
    else:
        return (0.0001 / (countW-countB)),False
                   
                
def evaluate (state: State,row,col):
        if state.board[row,col] == 1:
            return (7-row)*0.5
        elif state.board[row,col] == -1:
            return row*0.5                
        else:
            return 0
                
if __name__ == '__main__':
    main()