import matplotlib.pyplot as plt
import numpy as np
import os

def read_file(file_path):
    id_dict={}
    with open(file_path,'r') as f:
        row_temp = f.readline().strip().split(',')
        x_list,y_list = [],[]
        for line in f:
            row=line.strip().split(',')
            coordinate=[]
            if row[0] != row_temp[0]:
                id_dict[row_temp[0]] = [x_list,y_list]
                x_list = []
                y_list = []
            x_list.append(float(row[3]))
            y_list.append(float(row[4]))
            row_temp = row
        id_dict[row_temp[0]] = [x_list, y_list]
    return id_dict

def show(id_dict):
    #show intersection
    inter_x=[521677,521580,521520,521452,521433,521411,521400]
    inter_y=[58109,57466,57059,56668,55855,54822,53998]
    intersection=[inter_x,inter_y]
    
    colors = np.array([0.38 for i in range(len(inter_x))] ) # 随机产生50个0~1之间的颜色值
    area = np.array( [250 for i in range(len(inter_x))] ) # 点的半径范围:0~10

    plt.scatter(inter_x,inter_y, s=area, c=colors, alpha=0.5, marker=(9, 3, 30))
    
    for key in id_dict:
        item_x=id_dict[key][0]
        item_y=id_dict[key][1]
        plt.plot(item_x,item_y)
    plt.show()
        

            


if __name__=="__main__":
    dir_path = '2017-05-04_cross7/7_turn/'
    file_list = os.listdir(dir_path)
    for file in file_list:
        id_dict=read_file(dir_path+file)
        print(file)
        show(id_dict)
    inter_x=[521677,521580,521520,521452,521433,521411,521400]
    inter_y=[58109,57466,57059,56668,55855,54822,53998]
    intersection=[inter_x,inter_y]
