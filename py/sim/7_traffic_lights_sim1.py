# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 17:08
# @Author  : play4fun
# @File    : 7_traffic_lights_sim1.py
# @Software: PyCharm

"""
7_traffic_lights_sim1.py:
模拟7个信号灯🚥
"""

import simpy

fp='../../比赛/模板方案.txt'
with open(fp) as f:
    lines=f.readlines()
# print(lines)#['0,111,9,43,37;10,28,121,13,38;10,28,134,38;10,34,75,31,19,41;134,48,89,63;105,35,67,52,46;52,30,96,74']
lights_plan=lines[0].split(';')
print(lights_plan)

if __name__ == '__main__':

    pass
