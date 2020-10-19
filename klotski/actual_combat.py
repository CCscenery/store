import base64

import image_recognition
import numpy as np
import pickle
from image_recognition import get_jsonstr
import json
import sys
from math import ceil
from random import randint
import requests

# current_table,anstype = image_recognition.main()  # 返回列表和int类型
# target_file = 'dic' + str(anstype) + '.pkl'
# pkl_file = open(target_file,'rb')  # 图像识别挖去的是第几块
# dic = pickle.load(pkl_file)
# pkl_file.close()

# pkl_file = open('dic9.pkl','rb') #图像识别挖去的是第几块
# dic = pickle.load(pkl_file)
# pkl_file.close()
# current_table = [8, 7, 6, 5, 4, 3, 2, 1, 0]

# print(dic)
# print(dic['[1, 2, 3, 4, 5, 6, 7, 8, 0]'])

# def get_stepnum(table):
#     return len(dic[str(table)])-1

def show_table(table):
    '''表状态的可视化'''
    for i in range(0,9,3):
        print(table[i:i+3])
    print()

def move_onestep(table):
    '''输入为一个表状态,返回为所有走一步可到达的表状态列表和走法列表'''
    store_table = table[:]  #存储原始表信息
    onestep_tables = []
    onestep_moves = []
    index = table.index(0)
    if index % 3 == 0:
        direction = [index - 3, index + 3, index + 1]
        move_str = ['w', 's', 'd']
    elif index % 3 == 2:
        direction = [index - 3, index + 3, index - 1]
        move_str = ['w', 's', 'a']
    else:
        direction = [index - 3, index + 3, index - 1, index + 1]
        move_str = ['w','s','a','d']
    for i in range(len(direction)):
        go = direction[i]
        if go>=0 and go <=8:  # 这个位置可以走
            table = store_table[:]  # 确保交换之前为原始状态
            table[index],table[go] = table[go],table[index]
            onestep_tables.append(table)
            onestep_moves.append(move_str[i])
    return onestep_tables,onestep_moves


def get_one_moveable(index):
    '''获取当前表随便一个可以移动的位置'''
    optional = [index+1,index-1,index+3,index-3]
    for i in optional:
        if i>=0 and i<=8:
            break
    return i

def get_stepmethod(table):
    '''返回这个表到答案的走法（字符串序列）'''
    return transform_ans(dic[str(table)])
def transform_ans(way_method):
    ans = ''
    for i in range(len(way_method)-1,0,-1):  # 逆序遍历
        now = way_method[i]
        before = way_method[i-1]
        d_value = now-before
        if d_value == 3:
            ans += 'w'
        elif d_value == -3:
            ans += 's'
        elif d_value == 1:
            ans += 'a'
        elif d_value == -1:
            ans += 'd'
    return ans

def get_movedtable(move_process,table):
    '''根据移动序列返回按照移动序列移动后的表'''
    for move in move_process:  # 正序遍历
        index = table.index(0)
        if move == 'a':
            table[index],table[index-1] = table[index-1],table[index]
        elif move == 'd':
            table[index], table[index+1] = table[index+1], table[index]
        elif move == 'w':
            table[index],table[index-3] = table[index-3], table[index]
        elif move == 's':
            table[index], table[index+3] = table[index+3], table[index]
        show_table(table)  # 打印每一步的表状态
    return table

def force_swap(swap,table):
    print("强制交换")
    '''根据交换规则和当前表返回强制交换之后的表'''
    table[swap[0]-1],table[swap[1]-1] = table[swap[1]-1],table[swap[0]-1]
    show_table(table)
    return table

def freedom_swap(table):
    print("自由交换")
    '''根据当前无解表状态,返回最优交换目标表和交换策略'''
    arr_origin = np.array(table)
    for key in dic.keys(): #从layer浅到深进行遍历
        arr_target = np.array(eval(key))
        if len(arr_origin[arr_origin!=arr_target]) == 2:  # 交换完之后可以一样
            break
    (d_index,) = np.where(arr_origin != arr_target)
    d_index += 1 # 下标从0开始，位置从1开始
    show_table(list(arr_target))
    return list(arr_target),list(d_index)

def mincost_match(onestep_tables,swap):
    '''根据所有走一步的可能状态和交换规则返回有解表中的最小代价匹配'''
    global cost
    pos = 0
    notfound = True
    for i in range(len(onestep_tables)):
        table = onestep_tables[i]
        if str(table) in dic_cost:  # 有遍历过的
            if dic_cost[str(table)] == cost:  # 最小代价
                pos = i
                notfound = False
        else:  # 没遍历过的进行遍历
            arr_table = np.array(table)
            for key in dic.keys():
                arr_target = np.array(eval(key))
                if len(arr_table[arr_table!=arr_target]) == 2:
                    (d_index,) = np.where(arr_table != arr_target)
                    d_index += 1
                    d_index = list(d_index)
                    if (d_index[0] == swap[0] and d_index[1] == swap[1]) or (d_index[1] == swap[0] and d_index[0] == swap[1]):
                        dic_cost[str(table)] = len(dic[key]) - 1  # 记录无解表状态cost
                        if  dic_cost[str(table)] < cost:  # 代价更小
                            cost = dic_cost[str(table)]
                            pos = i
                            notfound = False
                            continue  # 无需往下深搜,开始查找下一个表状态
    if notfound:
        pos = randint(0,len(onestep_tables)-1)  # 随机走
    return pos


if __name__ == "__main__":
    # url = "http://47.102.118.1:8089/api/problem?stuid=031804104"
    # jsonstr = get_jsonstr(url)
    # print('成功获取json')
    # step,swap,uuid = jsonstr['step'],jsonstr['swap'],jsonstr['uuid']
    pkl_file = open('dic6.pkl', 'rb')  # 图像识别挖去的是第几块
    dic = pickle.load(pkl_file)
    pkl_file.close()
    step = 20
    swap = [6,4]
    current_table = [1,3,9,0,2,5,8,4,7]
    print('step={}'.format(step))
    print('swap={}'.format(swap))
    # 提交变量初始化
    operations = ''
    free_swap = []

    orgin_table = current_table[:] #图片识别
    table = orgin_table[:]
    # print('anstype={}'.format(anstype))
    show_table(table)

    if str(table) in dic:  # 有解
        move_process = get_stepmethod(table)
        if len(move_process) <= step:  # 可以在强制交换之前走完
            print("可以在强制交换之前走完")
            operations = move_process  # over
            get_movedtable(move_process, table)  # 可视化
            print(operations,len(operations))
            sys.exit()  # 结束程序
        else:  # 强制交换之气那走不完
            print("原图需要走{}步".format(len(move_process)))
            print("无法在强制交换之前走完")
            operations = move_process[:step]
            table = get_movedtable(operations, table)  # 走了step步以后的table
            table = force_swap(swap, table)  # 强制交换完以后的table
            if str(table) in dic:  # 强制交换之后
                move_process = get_stepmethod(table)
                operations += move_process
                get_movedtable(move_process, table)  # 可视化
            else:
                print("无解，自由交换")
                table, free_swap = freedom_swap(table)
                move_process = get_stepmethod(table)
                operations += move_process
                get_movedtable(move_process, table)  # 可视化

    else:  # 无解
        print("原图无解")
        cost = 32  # 根据历史经验cost最大是31
        dic_cost = {}
        for i in range(step):  # 强制交换前走的步数
            onestep_tables, onestep_moves = move_onestep(table)
            pos = mincost_match(onestep_tables,swap)
            table = onestep_tables[pos]  # 更新表状态
            operations += onestep_moves[pos]  # 记录走法
            print(onestep_moves[pos])
            show_table(table)
        table = force_swap(swap, table)  # 强制交换
        if str(table) in dic:
            move_process = get_stepmethod(table)
            operations += move_process
            print("1")
            print(move_process)
            get_movedtable(move_process,table)
        else:  #强制交换之后仍然无解
            table, free_swap = freedom_swap(table)  # 自由交换
            move_process = get_stepmethod(table)
            operations += move_process
            print("2")
            print(move_process)
            get_movedtable(move_process, table)  # 可视化

    print(operations,len(operations),free_swap)



