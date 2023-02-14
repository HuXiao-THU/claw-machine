import random

class ClawMachine():
    def __init__(self, strong_claw_count, random_success_ratio, occupied_ratio=0.5):
        self.strong_claw_count = strong_claw_count
        self.random_success_ratio = random_success_ratio
        self.occupied_ratio = occupied_ratio # 代表吸引游客和其他玩家坚持游玩的概率

        self.miss_count = 0
        self.occupied = False

    def play(self, isAgent):
        if isAgent:
            self.occupied = False
        else:
            self.occupied = True if random.random() < self.occupied_ratio else False

        if self.miss_count >= self.strong_claw_count:
            self.miss_count = 0
            return 30
        elif random.random() < self.random_success_ratio:
            self.miss_count = 0
            return 30
        else:
            self.miss_count += 1
            return -2
        
    
            