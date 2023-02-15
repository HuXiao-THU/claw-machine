from ClawMachine import *
import numpy as np

class World():
    def __init__(self):
        self.machines = []
        self.machine_num = 3
        for i in range(self.machine_num):
            self.machines.append(ClawMachine(10, 0.05))
        
        self.time_step = 0
        self.max_time_step = 1e5

        self.occupation_array = []
        self.machine_being_observed = -1
        self.watch_array = []

        self.observation_space = 2 * self.machine_num  # [occupation array, watch array] (2machine_num x 1)
        self.action_space = 2 * self.machine_num  # [play array, watch array] (2machine_num x 1) 

        self.reset()

    def reset(self):
        for m in self.machines:
            m.reset()
        self.time_step = 0

        self.occupation_array = [0 for i in range(self.machine_num)]
        self.machine_being_observed = -1
        self.watch_array = [-1 for i in range(self.machine_num)]

        return self.get_state()

    def get_state(self):
        self.update_occupation_array()
        state = self.occupation_array + self.watch_array
        return np.array(state)

    def step(self, action):
        # action: id of one-hot variable [play array, watch array] (machine_num*2)
        self.time_step += 1
        action_id = action
        if action_id < self.machine_num:
            # play
            # 会忘记之前观察的结果
            self.machine_being_observed = -1
            self.watch_array = [0 for i in range(self.machine_num)]

            if self.occupation_array[action_id] == 1:
                # 插队惩罚
                r = -9999
            else:
                r = self.machines[action_id].play(isAgent = True)

            # 其他玩家玩耍
            for i in range(self.machine_num):
                if i == action_id:
                    continue

                if self.machines[i].occupied:
                    self.machines[i].play(isAgent = False)
                elif random.random() < self.machines[i].occupied_ratio:
                    self.machines[i].play(isAgent = False)

        else:
            # watch
            watch_id = action_id - self.machine_num

            self.machine_being_observed = watch_id
            if watch_id != self.machine_being_observed:
                self.watch_array = [-1 for i in range(self.machine_num)]

            # 其他玩家玩耍
            for i in range(self.machine_num):
                if self.machines[i].occupied:
                    watch_result = self.machines[i].play(isAgent = False)
                elif random.random() < self.machines[i].occupied_ratio:
                    watch_result = self.machines[i].play(isAgent = False)
                else:
                    watch_result = 0

                if i == watch_id:
                    if watch_result > 0:
                        self.watch_array[i] = 0
                    elif watch_result < 0:
                        if self.watch_array[i] == -1:
                            self.watch_array[i] = 1
                        else:
                            self.watch_array[i] += 1
                    
            r = -1
        
        done = True if self.time_step >= self.max_time_step else False
    
        return (self.get_state(), r, done, {})
    
    def update_occupation_array(self):
        for i in range(self.machine_num):
            if self.machines[i].occupied:
                self.occupation_array[i] = 1
            else:
                self.occupation_array[i] = 0