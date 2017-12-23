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
# 双向直行
phase_双向直行_南北 = [NS北南, SN南北]  # ||⬆️⬇️
phase_双向直行_东西 = [EW东西, WE西东]  # == ⏩️️⬅️

# 单向直行+左转
phase_单向直行_左转_南 = [SW南西, SN南北]  # 7|
phase_单向直行_左转_北 = [NS北南, NE北东]  # |L
phase_单向直行_左转_西 = [WN西北, WE西东]  # ➡️➡️⬆️⏩

# 双向左转
phase_双向左转_南北 = [SW南西, NE北东]  # 7L
phase_双向左转_东西 = [WN西北, ES东南]  # ┘┌

# 双向直行+左转
phase_双向直行_左转_东西 = [EW东西, ES东南, WN西北, WE西东]
phase_双向直行_左转_南北 = [NS北南, NE北东, SW南西, SN南北]

# 十字路口信号相位
cross1 = [{'phase': phase_双向直行_南北, 'time': 111, 'min': 35},
          {'phase': phase_单向直行_左转_南, 'time': 9, 'min': 8},
          {'phase': phase_双向左转_南北, 'time': 43, 'min': 10},
          {'phase': phase_双向直行_左转_东西, 'time': 37, 'min': 35}
          ]
cross2 = [{'phase': phase_单向直行_左转_南, 'time': 28, 'min': 8},
          {'phase': phase_双向直行_左转_南北, 'time': 121, 'min': 35},
          {'phase': phase_单向直行_左转_北, 'time': 13, 'min': 8},
          {'phase': phase_双向直行_左转_东西, 'time': 38, 'min': 35}
          ]
cross3 = [{'phase': phase_双向左转_南北, 'time': 28, 'min': 10},
          {'phase': phase_双向直行_南北, 'time': 134, 'min': 35},
          {'phase': phase_双向直行_左转_东西, 'time': 38, 'min': 35}
          ]

cross4 = [{'phase': phase_双向左转_南北, 'time': 34, 'min': 10},
          {'phase': phase_双向直行_南北, 'time': 75, 'min': 35},
          {'phase': phase_双向左转_东西, 'time': 31, 'min': 10},
          {'phase': phase_单向直行_左转_西, 'time': 19, 'min': 8},
          {'phase': phase_双向直行_东西, 'time': 41, 'min': 35}
          ]

cross5 = [{'phase': phase_双向左转_南北, 'time': 48, 'min': 10},
          {'phase': phase_双向直行_南北, 'time': 89, 'min': 35},
          {'phase': phase_双向直行_左转_东西, 'time': 63, 'min': 35}
          ]

cross6 = [{'phase': phase_双向左转_南北, 'time': 35, 'min': 10},
          {'phase': phase_双向直行_南北, 'time': 67, 'min': 35},
          {'phase': phase_双向左转_东西, 'time': 52, 'min': 10},
          {'phase': phase_双向直行_东西, 'time': 46, 'min': 35}
          ]

cross7 = [{'phase': phase_双向左转_南北, 'time': 30, 'min': 10},
          {'phase': phase_双向直行_南北, 'time': 96, 'min': 35},
          {'phase': phase_双向直行_左转_东西, 'time': 74, 'min': 35}
          ]
