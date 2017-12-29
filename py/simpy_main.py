# -*- coding: utf-8 -*-
# @Time    : 2017/12/24 12:53
# @Author  : play4fun
# @File    : simpy_main.py
# @Software: PyCharm

"""
simpy_main.py:仿真主程序

# 先模拟一个路口

"""
import simpy, time, pickle
import pandas as pd
import numpy as np
from collections import deque

# 队列,一个路口,车道-直行-左转


from config import *
from Car import Car


def setup():
    global df
    # fpath = '../比赛/轨迹数据.txt'
    # df0 = pd.read_csv(fpath)
    # df = df0.sort_values(by='time')
    # time_min = df['time'].min()
    # df['time2'] = df['time'] - time_min

    with open('df', 'rb') as f:
        df = pickle.load(f)

        # df2 = df[df['vehicle-id'] == 'f3bc6bd1462edd25f7ae844143e8f65d']  # 某辆车


def car_driver(env):
    car_set = set()
    while True:
        dft = df[df['time2'] == env.now]
        # df 遍历
        for ix, row in dft.iterrows():
            vehicle_id = row['vehicle-id']  # .value
            if vehicle_id not in car_set:
                car_set.add(vehicle_id)
                # TODO
                # car = Car(vehicle_id)
                # road_car_queue.append(car)  # 加入队列

                # df2 = df[df['vehicle-id'] == vehicle_id]  # 某辆车
                print(env.now, f'\t\t\t车辆{vehicle_id}:上路')
                # TODO 加入队列?
                # TODO 需要提前处理车辆数据,1.路径,2.方向,3.车速

        yield env.timeout(1)  # 以1秒为单位


def Cross(index, env):
    # 8个队列
    global road_car_queue
    road_car_queue = deque()

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


if __name__ == '__main__':
    setup()

    # 初始化并开始仿真
    print('十字路口,开始仿真')
    # 创建一个环境并开始仿真
    env = simpy.Environment()
    # env.process(setup(env, NUM_MACHINES, WASHTIME, T_INTER))

    # 初始化7个十字路口
    for i in range(1, 8):
        env.process(Cross(i, env))
    # env.process(Cross(6, env))#第6个交叉口

    # 车辆
    env.process(car_driver(env))

    # 开始执行!
    env.run(until=1000)  # 测试
    # env.run(until=1130389)#最后的时间点
