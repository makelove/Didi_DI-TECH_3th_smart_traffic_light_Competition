# -*- coding: utf-8 -*-
# @Time    : 2017/12/29 19:20
# @Author  : play4fun
# @File    : 统计车的途经哪些路口.py
# @Software: PyCharm

"""
统计车的途经哪些路口.py:
"""

import time, pickle
import pandas as pd
import numpy as np

from config import cross_cord

cx = [];
cy = []
for z in range(1, 8):
    #     print(z)
    cx.append(cross_cord[str(z)]['x'])
    cy.append(cross_cord[str(z)]['y'])


# print(cx,cy)
def dist(x1, x2, y1, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


from math import radians, cos, sin, asin, sqrt, degrees, atan2


# 求两个经纬点的方位角，P0(latA, lonA), P1(latB, lonB)
def getDegree(latA, lonA, latB, lonB):
    """
    Args:
        point p1(latA, lonA)
        point p2(latB, lonB)
    Returns:
        bearing between the two GPS points,
        default: the basis of heading direction is north
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng
    """
    真方位角 (True bearing)
    所有角度以正北方设为000°，顺时针转一圈后的角度为360°。
    因此：
    正北方：000°或360°
    正东方：090°
    正南方：180°
    正西方：270°
    """


# def cal(dfxxx:pd.DataFrame):
def cal(dfxxx):
    car_track = []
    counter = 0
    for vid, row in dfxxx.groupby('vehicle-id'):
        d1 = dict()
        d1['vehicle-id'] = vid
        l1 = car_passby_cross(row)
        d1['track_list'] = l1

        car_track.append(d1)


        # if counter>5:
        #     break
        # else:
        #     counter+=1

    # 一条新轨迹
    #

    '''
    vehicle-id:
        轨迹列表:[
            {
                开始时间
                开始GPS
                [(红绿灯ID,方向)...]
            }
            ]
    '''
    return car_track  # 返回一个列表


from statistics import mean, median


# def car_passby_cross(dfxxx:pd.DataFrame):
def car_passby_cross(dfxxx):
    # 轨迹列表
    track_list = []

    first = 0
    last = 0
    angle_list = []
    tmp_list = []
    near = False
    cha_list = []
    cha_tangle_list = []
    direction_list = []

    min_distence = 188.43449800878878
    x = list(dfxxx['x-coordinate'])
    y = list(dfxxx['y-coordinate'])
    cargps = [(a, b) for a, b in zip(x, y)]
    # cargps=cargps[0]+cargps
    time_list = list(dfxxx['time'])

    # 车辆的方位角,序列
    counter = 0
    for (a, b), (c, d), time2 in zip(cargps[:-1], cargps[1:], time_list):
        #
        degre = getDegree(a, b, c, d)

        #
        dist_list = [dist(a, cx1, b, cy1) for cx1, cy1 in zip(cx, cy)]
        dist_min = min(dist_list)
        if dist_min < min_distence - 20:
            print('方位角:', degre, end='\t')
            near = True
            #             meet_cross_list.append(dist_list.index(dist_min))
            cross_id = dist_list.index(dist_min)  # 附近的十字路口
            print('cross_id:', cross_id, end='\t')
            #
            c_c_d = dist(a, cx[cross_id], b, cy[cross_id])  # 到十字路口的距离
            print('到十字路口的距离', c_c_d)

            #
            tmp_list.append(degre)
        else:
            print('方位角:', degre)
            if near is True:

                cha = abs(mean(tmp_list) - median(tmp_list))
                print('平均-中位数:', cha)
                cha_list.append(cha)
                print('--------')
                tmp_list = [tm for tm in tmp_list if tm != 0]
                if len(tmp_list) < 5:
                    continue
                try:
                    tangle = abs(tmp_list[1] - tmp_list[-2])
                except:
                    continue
                cha_tangle_list.append(tangle)
                dire = '直行' if tangle < 25 else '左转'
                direction_list.append((cross_id, dire))
                print(dire, tangle)
                print(tmp_list)
                print('--------')

                tmp_list = []
            near = False

        #
        d22 = dist(a, c, b, d)  # 两个gps的距离
        #     if d22>100:#min_distence:
        if d22 > min_distence or counter == 0:
            print('又一条轨迹!两个gps的距离:', d22)
            if near is False:
                if counter == 0:
                    st = time_list[0]
                    counter += 1
                    sg = cargps[0]
                else:
                    st = time2
                    sg = (a, b)
                xxxx = {
                    'start_time': st,
                    'start_gps': sg,
                    'cross_id_dire': direction_list,
                }
                track_list.append(xxxx)

    #
    if near is True:
        cha = abs(mean(tmp_list) - median(tmp_list))
        print('平均-中位数:', cha)
        cha_list.append(cha)
        print('--------')
        tmp_list = [tm for tm in tmp_list if tm != 0]
        try:
            tangle = abs(tmp_list[1] - tmp_list[-2])
            cha_tangle_list.append(tangle)
            dire = '直行' if tangle < 25 else '左转'
            direction_list.append((cross_id, dire))
            print(dire, tangle)
            print(tmp_list)
            print('--------')
        except:
            pass


        #
        if counter == 0:
            st = time_list[0]
            counter += 1
            sg = cargps[0]
        else:
            st = time2
            sg = (a, b)
        xxxx = {
            'start_time': st,
            'start_gps': sg,
            'cross_id_dire': direction_list,
        }
        track_list.append(xxxx)

        tmp_list = []
    print(cha_list, '\n', cha_tangle_list, '\n', direction_list)

    return track_list

    # 0.0表示静止状态,堵车?
    '''
    5	157.927388185	141.68166002238866
    5	113.135056128	150.5074276567322
    5	86.6421889901	148.11033352604363
    5	54.7037493351	102.2993303749206
    5	21.705958244	105.46753118381855
    5	12.3020975421	0.0
    5	12.3020975421	107.74716368621074
    5	52.4721135016	0.0
    5	52.4721135016	106.62866338892826
    5	95.3297287634	108.8042985890936
    5	143.545458496	111.21532988788897
    #转弯,转了141-111=30度
    '''


if __name__ == '__main__':
    with open('df', 'rb') as f:
        df = pickle.load(f)
    df2 = df[['vehicle-id', 'time', 'x-coordinate', 'y-coordinate']]
    # df21 = df[df['vehicle-id'] == '4c0c4745067197be22182d262b44f48a']
    # df22 = df[df['vehicle-id'] == 'aa7c4004477b1e8147166e93aaa6ab0a']
    # df23 = df[df['vehicle-id'] == 'f3bc6bd1462edd25f7ae844143e8f65d']
    # df24 = df21.append(df22).append(df23)

    car_track = cal(df2)

    print('-----------------------------')
    print(car_track)

    import pickle

    # 写
    with open('car_track', 'wb') as f:
        pickle.dump(car_track, f)  # 序列化
