from BreakThrough import BreakThrough
from state import State
from DQN_agent import DQN_Agent
from ReplayBuffer import ReplayBuffer


import torch
from Tester import Tester

epochs = 2000000
start_epoch = 0
C = 500
learning_rate = 0.01
batch_size = 64
env = BreakThrough(State())
MIN_Buffer = 4000

File_Num = 1
path_load= None
path_Save=f'Data/data{1}.pth'
path_best = f'Data/best_params_{File_Num}.pth'
buffer_path = f'Data/buffer{1 }.pth'
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
    # player2 = DQN_Agent(player=-1,     env=env, parametes_path=path_load)   
    buffer = ReplayBuffer(path=None) # None
    
    results_file = [] #torch.load(results_path)
    results = [] #results_file['results'] # []
    avgLosses = [] #results_file['avglosses']     #[]
    avgLoss = 0 #avgLosses[-1] #0
    loss = 0
    res = 0
    best_res = -200
    loss_count = 0
    # tester = Tester(player1=player1, player2=random_agent(player=-1, env=env), env=env)
    # tester_fix = Tester(player1=player1, player2=player2, env=env)
    random_results = [] #torch.load(random_results_path)   # []
    best_random = 0 #max(random_results)
    
    
    # init optimizer
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optim,100000*30, gamma=0.90)
    # scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[30*50000, 30*100000, 30*250000, 30*500000], gamma=0.5)
    
    for epoch in range(start_epoch, epochs):
        print(f'epoch = {epoch}', end='\r')
        state = State()
        step = 0
        while not env.is_end_of_game(state):
            # Sample Environement
            step +=0.5
            action = player1.get_action(state=state,epoch=epoch)
            # if step % 1 == 0:
            #     action = player1.get_action(state=state,epoch=epoch)
            # else:
            #     action = player1.get_action(state=state,epoch=epoch)
            after_state = env.next_state(state=state, action=action)
            reward, end_of_game = env.reward(after_state)
            if end_of_game:
                res += reward
                buffer.push(state, action, reward, after_state, True)
                break
            state = after_state.flip()
            
    
            # print(action_1)
            buffer.push(state, action, reward, after_state, end_of_game)
            state = after_state

            if len(buffer) < 200: #MIN_Buffer:
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

        # if (epoch+1) % 1000 == 0:
        #     test = tester(100)
        #     test_score = test[0]-test[1]
        #     if best_random < test_score and tester_fix(1) == (1,0):
        #         best_random = test_score
        #         player1.save_param(path_best_random)
        #     print(test)
        #     random_results.append(test_score)

        # if (epoch+1) % 5000 == 0:
        #     # torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
        #     # torch.save(buffer, buffer_path)
        #     player1.save_param(path_Save)
        #     # torch.save(random_results, random_results_path)
        
        print (f'epoch={epoch} step={step} loss={loss:.5f} avgloss={avgLoss:.5f}', end=" ")
        print (f'learning rate={scheduler.get_last_lr()[0]} path={path_Save} res= {res} best_res = {best_res}')

    torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
    torch.save(buffer, buffer_path)
    torch.save(random_results, random_results_path)
    

if __name__ == '__main__':
    main()