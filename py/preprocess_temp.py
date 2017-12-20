import os
import sys
import math
import datetime
import matplotlib.pyplot as plt
import math

InSecs_pos = {0:(600000, 60000), 1:(521677, 58109), 2:(521580, 57466), 3:(521520, 57059), 4:(521452, 56668), \
              5:(521433, 55855), 6:(521411, 54822), 7:(521400, 53998), 8:(500000, 50000)}

def nearest_sec(x, y):
    min_dis = 10000
    for i in range(1, 8):
        dis2 = ((InSecs_pos[i][0] - x) ** 2 + (InSecs_pos[i][1] - y) ** 2) ** 0.5
        # print(dis2)
        if dis2 < min_dis:
            min_dis = dis2
            sec = i
    return sec

def judge(sec, x, y):
    x_diff = InSecs_pos[sec][0] - x
    y_diff = InSecs_pos[sec][1] - y
    if abs(x_diff) > abs(y_diff):
        if x_diff > 0:
            return 'west'
        else:
            return 'east'
    else:
        if y_diff > 0:
            return 'south'
        else:
            return 'north'


def turn(x1, y1, x2, y2, sec, dire):
    vec1 = (InSecs_pos[sec][0] - x1, InSecs_pos[sec][1] - y1)
    vec2 = (x2 - InSecs_pos[sec][1], y2 - InSecs_pos[sec][1])

    if dire == 'south':
        turn_dire = 'left' if vec2[0] < 0 else 'right'
    if dire == 'north':
        turn_dire = 'left' if vec2[0] > 0 else 'right'
    if dire == 'east':
        turn_dire = 'left' if vec2[1] < 0 else 'right'
    if dire == 'west':
        turn_dire = 'left' if vec2[1] > 0 else 'right'
    if vec1[0] * vec2[0] > 0 and vec1[1] * vec2[1] > 0:
        turn_dire = 'straight'
    return turn_dire

def traj_deal(date_dir, file_name):
    if file_name[-3:] != 'txt':
        return {}
    f = open(date_dir + '/' + file_name, 'r')
    ln = 0
    car_traj = []
    sec_traj = {}
    traj_id = 1
    for line in f:
        ln += 1
        row = line.strip().split(',')
        if ln == 1:
            continue
        x, y = float(row[3]), float(row[4])
        if ln == 2:
            row_temp = row
            sec_temp = nearest_sec(x, y)
            y_temp = y
            x_temp = x
            sec_dis_temp = get_dis(sec_temp, x, y)

        if ln > 2:
            sec_dis = get_dis(sec_temp, x, y)
            if sec_dis <= sec_dis_temp and sec_dis < 200:
                sec_entry = sec_temp
            elif y > y_temp and sec_dis > 200:
                sec_entry = sec_temp - 1 if sec_temp > 1 else 1
                sec_dis = get_dis(sec_entry, x, y)
            elif y < y_temp and sec_dis > 200:
                sec_entry = sec_temp + 1 if sec_temp < 7 else 7
                sec_dis = get_dis(sec_entry, x, y)
            if sec_dis < 200:
                row.append(str(sec_dis)[:5])
                car_traj.append(row)
            else:
                if len(car_traj) <= 5:
                    continue
                else:
                    start_pos = (int(car_traj[0][3]), int(car_traj[0][4]))
                    end_pos = (int(car_traj[-1][3]), int(car_traj[-1][4]))
                    entry_dire = judge(sec_entry, start_pos[0], start_pos[1])
                    turn_dire = turn(start_pos[0], start_pos[1], end_pos[0], end_pos[1], sec_entry, entry_dire)
                    key = str(sec_entry) + '-' + entry_dire + '-' + turn_dire
                    sec_traj[key] = car_traj
                    car_traj = []
                    sec_temp = nearest_sec(x, y)
            sec_dis_temp = sec_dis
            x_temp, y_temp = x, y
    return sec_traj


def generate_traj(date_dir):
    # date_dir = '2017-05-04/'
    all_sec_traj = {}
    for file_name in os.listdir(date_dir):
        sec_traj = traj_deal(date_dir, file_name)
        for key in sec_traj:
            try:
                if all_sec_traj[key]:
                    all_sec_traj[key] += sec_traj[key]
            except:
                all_sec_traj[key] = sec_traj[key]
    return all_sec_traj

def traj_sort(traj_path):
    f = open(traj_path, 'r')
    ln = 0
    car_traj = []
    traj_id = 1
    for line in f:
        ln += 1
        row = line.strip().split(',')
        if ln == 1:
            continue
        if ln == 2:
            time_temp = datetime.datetime.fromtimestamp(float(row[1]))
            date_temp = time_temp.date().strftime("%Y-%m-%d")
            car_id_temp = ''.join(row[0][0:4] + row[0][-4:])
            row_temp = row
            sec_temp = nearest_sec(float(row[2]), float(row[3]))
            # print(date_temp)
        # print(row)
        car_id = ''.join(row[0][0:4] + row[0][-4:])
        # print(type(car_id))
        time_stamp = datetime.datetime.fromtimestamp(float(row[1]))
        date_str = time_stamp.date().strftime("%Y-%m-%d")
        time_str = time_stamp.time().strftime("%H:%M:%S")
        # sec = nearest_sec(float(row[2]), float(row[3]))

        traj_info = []
        traj_info.append(str(ln - 1))
        traj_info.append(car_id)
        traj_info.append(time_str)
        traj_info.append(row[2].split('.')[0])
        traj_info.append(row[3].split('.')[0])
        traj_info.append(row[4])
        if not os.path.exists(date_str):
            os.mkdir(date_str)
        #print(type((time_stamp - time_temp).total_seconds))
        if date_temp == date_str and car_id == car_id_temp and (time_stamp - time_temp) < datetime.timedelta(10):
            car_traj.append(traj_info)
        else:
            # print(date_temp)
            print('::::')
            file_path = date_temp + '/' + car_id_temp +'_'+str(traj_id)+ '.txt'
            with open(file_path, 'w') as fw:
                for rec in car_traj:
                    # print(rec)
                    fw.write(','.join(rec) + '\n')
            fw.close()
            if car_id == car_id_temp:
                traj_id += 1
            else:
                traj_id = 1
            car_traj = [traj_info]
        date_temp = date_str
        car_id_temp = car_id
        time_temp = time_stamp
        sec_temp = nearest_sec(float(row[2]), float(row[3]))
        row_temp = row
    file_path = date_temp + '/' + car_id_temp +'_'+str(traj_id)+ '.txt'
    print(car_id)
    with open(file_path, 'w') as fw:
        for rec in car_traj:
            # print(rec)
            fw.write(','.join(rec) + '\n')
    fw.close()
    return 0