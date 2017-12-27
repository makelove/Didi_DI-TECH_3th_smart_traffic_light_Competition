# -*- coding: utf-8 -*-
# @Time    : 2017/12/25 21:57
# @Author  : play4fun
# @File    : Cross_Car_Queue.py
# @Software: PyCharm

"""
Cross_Car_Queue.py:
"""


class Cross_Car_Queue:
    def __init__(self, cross_id,signal):
        self.cross_id = cross_id
        self.signal=signal #信号灯
        self.length=434#TODO 长度
        self.start=xx#起始
        self.end=xx#重点


        #
        self.queue_straight=queue #直行
        self.queue_left=queue #左转


        pass
    def update_signal(self,signal):

        self.signal=signal

        pass

    def queue_update(self,direction,car):
        queue=None
        if direction=='straight':
            queue=self.queue_straight
        if direction == 'left':
            queue = self.queue_left

        #TODO 更新车的位置,排序
        queue.update(car)

