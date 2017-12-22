# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 18:16
# @Author  : play4fun
# @File    : config.py
# @Software: PyCharm

"""
config.py:
"""

# 十字路口坐标
cross_cord = {'1': {'x': 521677, 'y': 58109},
              '2': {'x': 521580, 'y': 57466},
              '3': {'x': 521520, 'y': 57059},
              '4': {'x': 521452, 'y': 56668},
              '5': {'x': 521433, 'y': 55855},
              '6': {'x': 521411, 'y': 54822},
              '7': {'x': 521400, 'y': 53998}
              }

# 行驶方向
NS北南 = 0
NE北东 = 1
EW东西 = 2
ES东南 = 3
SN南北 = 4
SW南西 = 5
WE西东 = 6
WN西北 = 7
# 发动机=3
# print(NS北南,SN南北,SW南西,发动机)#可以用中文

# 相位定义
# 单向直行
phaseA = [NS北南, SN南北]  # ||⬆️⬇️
phaseA = [EW东西, WE西东]  # == ⏩️️⬅️

# 单向直行+左转
phaseB = [SW南西, SN南北]  # 7|
phaseB = [NS北南, NE北东]  # |L

# 双向左转
phaseC = [SW南西, NE北东]  # 7L
phaseC = [WN西北, ES东南]  # ┘┌

# 双向直行+左转
phaseD = [EW东西, ES东南, WN西北, NE北东]
phaseE = [NS北南, NE北东, SW南西, SN南北]

# 十字路口信号相位
cross1 = {'phase1': {}}
