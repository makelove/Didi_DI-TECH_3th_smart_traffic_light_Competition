# -*- coding: utf-8 -*-
# @Time    : 2017/12/24 12:53
# @Author  : play4fun
# @File    : simpy_main.py
# @Software: PyCharm

"""
simpy_main.py:仿真主程序

# 先模拟一个路口

"""
import simpy, time
import pandas as pd
import numpy as np
from collections import deque

# 队列,一个路口,车道-直行-左转


from config import *


def setup():
    fpath = '../比赛/轨迹数据.txt'
    df0 = pd.read_csv(fpath)
    df = df0.sort_values(by='time')
    df2 = df[df['vehicle-id'] == 'f3bc6bd1462edd25f7ae844143e8f65d']  # 某辆车


def Cross(index, env):
    cross = corss_list[index - 1]
    queue = deque(cross)
    while True:
        # phase_tmp=cross.pop()
        phase_tmp = queue.popleft()
        phase = phase_tmp['phase']
        time0 = phase_tmp['time']
        min0 = phase_tmp['min']

        print(env.now, f'\t路口{index}:', phase)
        # print('现在开始:',phase,cross)
        yield env.timeout(time0)

        queue.append(phase_tmp)

    # 信号灯,变换
    # while True:
    #     print("Light turned GRN绿 at t= " + str(env.now))
    #     yield env.timeout(30)
    #     print("Light turned YEL黄 at t= " + str(env.now))
    #     yield env.timeout(5)
    #     print("Light turned RED红 at t= " + str(env.now))
    #     yield env.timeout(20)

    # 8个队列

    pass


if __name__ == '__main__':
    # 初始化并开始仿真
    print('十字路口,开始仿真')
    # 创建一个环境并开始仿真
    env = simpy.Environment()
    # env.process(setup(env, NUM_MACHINES, WASHTIME, T_INTER))

    # 初始化7个十字路口
    for i in range(1, 8):
        env.process(Cross(i, env))
    # env.process(Cross(6, env))#第6个交叉口

    # 开始执行!
    # env.run(until=420)
    env.run(until=1130389)#最后的时间点
