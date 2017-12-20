import os
import sys
import math
import datetime
import matplotlib.pyplot as plt
import math
from preprocess_temp import *

InSecs_pos = {0:(600000, 60000), 1:(521677, 58109), 2:(521580, 57466), 3:(521520, 57059), 4:(521452, 56668), \
              5:(521433, 55855), 6:(521411, 54822), 7:(521400, 53998), 8:(500000, 50000)}

def get_dis(sec, x, y):
    return ((InSecs_pos[sec][0] - x) ** 2 + (InSecs_pos[sec][1] - y) ** 2) ** 0.5

def cross_data(sec,dis_range):
    #找到经过某路口的所有数据,dis_range表示路口影响范围
    min_time = '23:59:59'
    max_time = '00:00:00'
    time_range = {}
    f = open('traj_data.txt','r')
    sec_data = {}

    traj_id = 0
    ln = 0
    for line in f:
        ln += 1
        if ln == 1:
            continue
        if ln == 2:
            row_temp = f.readline().strip().split(',')
            time_temp = datetime.datetime.fromtimestamp(float(row_temp[1]))
        row = line.strip().split(',')
        id = ''.join(row[0][0:4]+row[0][-4:])
        #print(row)
        x = int(float(row[2]))
        y = int(float(row[3]))
        time_stamp = datetime.datetime.fromtimestamp(float(row[1]))
        time_str = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        row_date = time_str[:10]
        if row_date in time_range:
            if time_str[-8:] < time_range[row_date][0]:
                time_range[row_date][0] = time_str[-8:]
            if time_str[-8:] > time_range[row_date][1]:
                time_range[row_date][1] = time_str[-8:]
        else:
            time_range[row_date] = [time_str[-8:],max_time]
        dis = get_dis(sec,x,y)
        #print(get_dis(7, x, y))
        if dis < dis_range:
            if row[0] == row_temp[0] and (time_stamp - time_temp) < datetime.timedelta(seconds=60):
                pass
            else:
                traj_id += 1
            if traj_id not in sec_data:
                sec_data[traj_id] = [[id,time_str, str(x), str(y), row[4],str(dis)[:5]]]
            else:
                sec_data[traj_id].append([id,time_str, str(x), str(y), row[4],str(dis)[:5]])
            row_temp = row
            time_temp = time_stamp

    fw = open(str(sec)+'_sec.txt','w')
    for meta_id in sec_data:
        for traj in sec_data[meta_id]:
            fw.write(','.join([str(meta_id)]+traj)+'\n')
    fw.close()
    return time_range,sec_data


def cal_period(date,t1,t2,period):
    utime1 = datetime.datetime.strptime(date+' '+t1, "%Y-%m-%d %H:%M:%S")
    utime2 = datetime.datetime.strptime(date+' '+t2, "%Y-%m-%d %H:%M:%S")
    return (utime2-utime1).total_seconds()/(period*60)

def seperate(date_pre,time_range,period,sec_data,sec):
    #period的单位是min
    min_time,max_time = time_range[date_pre]
    series_num = int(cal_period(date_pre,min_time,max_time,period))+1
    data_period = {}
    for i in range(series_num):
        data_period[i+1] = []

    for meta_id in sec_data:
        for traj in sec_data[meta_id]:
            date = traj[1][:10]
            #print(date)
            time = traj[1][-8:]
            if date == date_pre:
                series = int(cal_period(date,min_time,time,period))+1
                data_period[series].append([str(meta_id)]+traj)
        #break
    for key in data_period:
        dir_name = date_pre+'_cross'+str(sec)+'/'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        if len(data_period[key]) < 5:
            continue
        fw = open(dir_name+str(key)+'.txt','w')
        for rec in data_period[key]:
            fw.write(','.join(rec)+'\n')
        fw.close()
    return data_period

def turn_7(x1, y1, x2, y2, sec,angle_thre):
    vec1 = (InSecs_pos[sec][0] - x1, InSecs_pos[sec][1] - y1)
    vec2 = (x2 - InSecs_pos[sec][0], y2 - InSecs_pos[sec][1])
    if abs(vec1[0]) > abs(vec1[1]):
        if vec1[0] > 0:
            dire = 'west'
        else:
            dire = 'east'
    else:
        if vec1[1] > 0:
            dire = 'south'
        else:
            dire = 'north'
    try:
        angle = 180/math.pi*math.acos((vec1[0]*vec2[0]+vec1[1]*vec2[1])/(get_dis(sec,x1,y1)*get_dis(sec,x2,y2)))
    except:
        angle = 90
    if angle<=angle_thre:
        turn_dire = 'straight'
    elif abs(angle-90)<=angle_thre:
        if dire == 'north' and vec2[0] > 0:
            turn_dire = 'left'
        if dire == 'north' and vec2[0] < 0:
            turn_dire = 'right'
        if dire == 'south' and vec2[0] > 0:
            turn_dire = 'right'
        if dire == 'south' and vec2[0] < 0:
            turn_dire = 'left'
        if dire == 'east' and vec2[1] > 0:
            turn_dire = 'right'
        if dire == 'east' and vec2[1] < 0:
            turn_dire = 'left'
        if dire == 'west' and vec2[1] > 0:
            turn_dire = 'left'
        if dire == 'west' and vec2[1] < 0:
            turn_dire = 'right'
    else:
        print('error_angle',angle)
        turn_dire = 'error'
    return dire,turn_dire

def turn_sep(file_path,sec,dir_path,angle_thre):
    f = open(file_path,'r')
    start = f.readline().strip().split(',')
    print(start)
    row_temp = start
    sep_data = []
    all_sep_data = {}
    for line in f:
        row = line.strip().split(',')
        print(row)
        if start[0] != row[0]:
            print(sep_data)
            try:
                end = sep_data[-1]
            except:
                print(row)

            x1,y1 = float(start[3]),float(start[4])
            x2,y2 = float(end[3]),float(end[4])
            #print(sec)
            dire,turn_dire = turn_7(x1,y1,x2,y2,sec,angle_thre)
            print(sec)
            sep_key = '-'.join([dire,turn_dire])
            if sep_key not in all_sep_data:
                all_sep_data[sep_key] = sep_data
            else:
                all_sep_data[sep_key] += sep_data
            sep_data = []
            start = row
        sep_data.append(row)
        print(sep_data)
        #row_temp = row
    sep_key = '-'.join([dire, turn_dire])
    if sep_key not in all_sep_data:
        all_sep_data[sep_key] = sep_data
    else:
        all_sep_data[sep_key] += sep_data
    for key in all_sep_data:
        if key.split('-')[1] in ('right','error'):
            continue

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        fw = open(dir_path+str(key)+'.txt','w')
        for rec in all_sep_data[key]:
            fw.write(','.join(rec)+'\n')
        fw.close()
    print(dir_path)
    return all_sep_data

def cal_seconds(time):
    hour = int(time[:2])
    minute = int(time[3:5])
    seconds = int(time[-2:])
    total_seconds = hour*3600+minute*60+seconds
    return total_seconds

def show_st(file_path,time_range,period_num):
    plot_dict = {}
    date = file_path[:10]
    start_s = cal_seconds(time_range[date][0])+(period_num-1)*60*15
    f = open(file_path,'r')
    row_temp = f.readline().strip().split(',')
    s_temp = float(row_temp[-1])
    t_list,s_list = [],[]
    for line in f:
        row = line.strip().split(',')
        time = row[2][-8:]
        now_s = cal_seconds(time)
        s = float(row[-1])
        if row[0] != row_temp[0]:
            plot_dict[row_temp[0]] = [t_list,s_list]
            s_temp = s
            t_list,s_list = [],[]
        t_list.append(now_s-start_s)
        s_vec = -s if s <= s_temp else s
        s_list.append(s_vec)
        row_temp = row
        s_temp = float(row[-1])
    plot_dict[row_temp[0]] = [t_list, s_list]
    for key in plot_dict:
        #plt.scatter(plot_dict[key][0],plot_dict[key][1])
        plt.plot(plot_dict[key][0], plot_dict[key][1])
    img_path = file_path[:-4] + '.png'
    plt.savefig(img_path)
    plt.close()
    #plt.show()
    return 0


if __name__ == '__main__':
    #print(cal_period('2017-05-04', '07:00:07','08:59:59', 5))
    #文件路径改为在主函数设置
    data_path = 'traj_data.txt'
    dir_list = os.listdir('./')
    if len(dir_list) < 15:
        traj_sort(data_path)
    sec = 4
    dis_range = 200
    period = 15
    angle_thre = 15
    date_pre = '2017-05-04'
    time_range, sec_data = cross_data(sec,dis_range)
    for i in time_range:
        print(i,':',time_range[i])
    seperate(date_pre, time_range, period, sec_data, sec)
    file_path = date_pre+'_cross'+str(sec)+'/'
    period_list = os.listdir(file_path)
    sorted(period_list,key = lambda x:os.path.getsize(x),reverse=True)
    try:
        turn_path = file_path + period_list[0][0]+'_turn/'
        all_sep_data=turn_sep(file_path+period_list[0], sec,turn_path)
    except:
        turn_path = file_path + period_list[0][1] + '_turn/'
        all_sep_data = turn_sep(file_path + period_list[0], sec, turn_path)
    for file_name in os.listdir(turn_path):
        if file_name[-3:] != 'txt':
            continue
        file_path = turn_path+file_name
        show_st(file_path,time_range,7)


    dir_list = os.listdir('./')
    for dir in dir_list:
        break
        if dir[0:5] == '2017-':
            all_sec_traj = generate_traj(dir)
            write_dir = ''.join(dir.split('-'))
            if not os.path.exists(write_dir):
                os.mkdir(write_dir)
            for key in all_sec_traj:
                fw = open(write_dir + '/' + key + '.txt', 'w')
                for rec in all_sec_traj[key]:
                    fw.write(','.join(rec) + '\n')
                fw.close()


