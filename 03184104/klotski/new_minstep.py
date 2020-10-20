import pickle

def judge_limit(index):
    return (index>=0 and index<=8)

def remove_same(state,ways,exist_table):
    orgin_state = state[:]
    orgin_ways = ways[:]
    for i in range(len(orgin_state)):
        if orgin_state[i] in exist_table:
            state.remove(orgin_state[i])
            ways.remove(orgin_ways[i])

    return state,ways

def store_exist(layer):
    try:
        layer_type = type(layer[0]) #该层的第一个元素
    except:
        print('layer maybe empty')
        return
    if layer_type == type(1): #该层只有一个表
        exist_table.append(layer)
    else:
        for table in layer:
            exist_table.append(table)

def move(layer): #传入为9个数值元素编码的列表
    state, way = [], []
    try:
        layer_type = type(layer[0])
    except:
        print('layer maybe empty')
        return state,way
    if(layer_type==type(1)): #该层只有一个状态
        # print("the k {}".format(k))
        table = layer[:]
        ways = []
        orgin_table = table[:]
        index = orgin_table.index(0)
        # up,down,left,right = index-3,index+3,index-1,index+1
        if index % 3 == 0:
            direction = [index - 3, index + 3, index + 1]
        elif index % 3 == 2:
            direction = [index - 3, index + 3, index-1]
        else:
            direction = [index - 3, index + 3, index - 1, index + 1]
        for go in direction:  # 上下左右
            if (judge_limit(go)):  # 可移动的位置下标
                table = orgin_table[:]  # 原始表交换!,若没有[:]只是复制引用
                table[index], table[go] = table[go], table[index]  # 交换
                state.append(table)
                way_method = dic[str(orgin_table)][:]
                way_method.append(go + 1)
                ways.append(way_method)

    else:  # 该层有多个状态，是列表的列表
        ways = []
        for table in layer:  # table是其中一个状态，类型为列表
            orgin_table = table[:]
            index = orgin_table.index(0)
            #up,down,left,right = index-3,index+3,index-1,index+1
            if index % 3 == 0:
                direction = [index - 3, index + 3, index + 1]
            elif index % 3 == 2:
                direction = [index - 3, index + 3, index - 1]
            else:
                direction = [index - 3, index + 3, index - 1, index + 1]
            for go in direction: #上下左右
                if(judge_limit(go)):#可移动的位置下标
                    table = orgin_table[:]  # 原始表交换!,若没有[:]只是复制引用
                    table[index],table[go] = table[go],table[index] #交换
                    if table not in state:
                        state.append(table)
                        way_method = dic[str(orgin_table)][:]
                        way_method.append(go + 1)
                        ways.append(way_method)
    return state,ways

def bulid_dic(layer,ways):
    for i in range(len(layer)): #len(layer)==len(way)
        dic[str(layer[i])] = ways[i]
    return

'''1、识别图块（遍历）对应编码为0-8
'''
'''2、初始化状态层数表'''
if __name__ == "__main__":
    for i in range(9):  # 最终答案空格可能出现位置
        layer0 = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # answer状态对应0层
        layer0[i] = 0 #空格所在位置
        layers = [layer0]
        exist_table = [layer0]
        k = 0  # 层数
        # way_method = [9]
        dic = {str(layer0):[i+1]}

        while True:
            state,ways = move(layers[k])
            k += 1  # 移动完层数+1
            layer,ways = remove_same(state, ways,exist_table)
            store_exist(layer)
            bulid_dic(layer, ways)
            if len(layer) == 0:
                print('The deepest layer is layer {}'.format(k-1))
                save_name = 'dic'+str(i+1)+'.pkl'
                pkl_file = open(save_name, 'wb')
                pickle.dump(dic, pkl_file)
                pkl_file.close()
                print("dic has already saved in default path")
                break
            layers.append(layer)
            print(k)
            print('len {}'.format(len(layer)))




