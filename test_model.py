from World import *

player = 'human'

env = World()






if player == 'human':
    print("*******************")
    print("Welcome to 好好娃娃机, We have {:d} claw machines here.".format(env.machine_num))
    score = 0
    while env.time_step <= 30:
        s = env.get_state()
        print("*******************")
        print("Current time: {:d}, current score: {:.1f}".format(env.time_step, score))
        print("machine\t\t0\t1\t2")
        print("occupation\t{:d}\t{:d}\t{:d}".format(s[0],s[1], s[2]))
        print("input w[x] to watch machine [x], or p[x] to play on machine [x], such as 'w1' or 'p0'")
        a = input()
        while (a[0] != 'w' and a[0] != 'p') or (int(a[1:]) < 0 and int(a[1:]) >= env.machine_num):
            print("wrong input, try again")
            a = input()
        
        action = [0 for i in range(env.machine_num * 2)]
        if a[0] == 'p':
            action[int(a[1:])] = 1
        if a[0] == 'w':
            action[int(a[1:]) + env.machine_num] = 1
        action = np.argmax(action)

        next_state, r, done, _  = env.step(action)
        score += r
        if r == -9999:
            print("别人在玩这台机器，请不要插队！惩罚-9999分")
        elif r == -2:
            print("没抓到...扣2分")
        elif r == 30:
            print("抓到啦！加30分")
        elif r == -1:
            watch_result = env.watch_array[int(a[1:])]
            if watch_result == -1:
                print("这台机器目前没人玩，不知道他的状态")
            elif watch_result == 0:
                print("刚才一个娃娃在这个机器里被抓到了，之后还没人来尝试过")
            elif watch_result > 0:
                print("目前观察到这台机器已经连续失败{:d}次了".format(watch_result))
        
        if done:
            break

    print("Game Over! you get {:d} score within 100 rounds!".format(score))