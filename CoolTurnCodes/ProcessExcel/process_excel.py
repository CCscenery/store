import pandas as pd
import os


def get_filelist(dir_path):
    filelist = []
    for file in os.scandir(dir_path):
        filelist.append(file.path)
    return filelist

def get_excellist(filelist):
    excellist = []
    for file in filelist:
        excellist.append(pd.read_excel(file))
    return excellist

def excel_simple_merge(dir_path,save_name='result.xlsx'):
    filelist = get_filelist(dir_path)
    excellist = get_excellist(filelist)
    try:
        pd.concat(excellist).to_excel(save_name,index=False)
        print("当前路径是{}".format(os.getcwd()))
        print("{} 存储成功".format(save_name))
    except Exception as err:
        print(err)
        print("存储失败")

def combine_data(df_merged):
    ls_colname = df_merged.columns.values
    ls_data = ['NaN']*len(ls_colname)  # 初始化行数据
    row_num,col_num = df_merged.shape[0],df_merged.shape[1]
    for col_index in range(col_num):
        for row_index in range(row_num):
            data = df_merged.iloc[row_index][col_index]
            if pd.notnull(data):  # 该数据不为NaN
                ls_data[col_index] = data
                break  # 不为NaN则选定该值,不再向下查找
    dic = {}  # 初始化字典,效率高于dict()
    for index in range(len(ls_colname)):
        dic[ls_colname[index]] = [ls_data[index]]
    df_combined = pd.DataFrame(dic)
    return df_combined

def merge_excellist(excellist):
    while len(excellist) > 1:
        length = len(excellist)
        for i in range(0,length,2):
            if i+1<length:
                excellist.append(
                    pd.merge(left=excellist[i], right=excellist[i+1], how='outer')
                )
            else:
                excellist.append(excellist[i])
        excellist = excellist[length:]
    return excellist[0]

def excel_merge(dir_path):
    filelist = get_filelist(dir_path)
    excellist = get_excellist(filelist)
    df_merged = merge_excellist(excellist)
    return df_merged

def excel_connect_combine(df_merged, connect_columns, save_name='result.xlsx'):
    df_combined = df_merged.groupby(connect_columns,as_index=False).apply(combine_data)
    df_result = df_combined.reset_index(drop=True)
    try:
        df_result.to_excel(save_name,index=False)
        print("当前路径是{}".format(os.getcwd()))
        print("{} 存储成功".format(save_name))
    except Exception as err:
        print(err)
        print("存储失败")

def excel_split(df_total, split_columns, save_dir='split_result'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    groups = df_total.groupby(split_columns, as_index=False)
    for group in groups:
        basis = group[0]
        df = group[1]
        if isinstance(basis,tuple):
            try:
                save_name = '_'.join(basis)  # 用'_'来连接分割依据值作为文件名
            except TypeError:  # 元素中有非字符串类型
                basis = list(basis)
                basis = [str(element) for element in basis]
                save_name = '_'.join(basis)
        else:  # 只有一个元素
            save_name = str(basis)

        save_path = save_dir + '\\' + save_name + '.xlsx'
        try:
            df.to_excel(save_path, index=False)
            print("当前路径是{}".format(os.getcwd()))
            print("{} 存储成功".format(save_path))
        except Exception as err:
            print(err)
            print("存储失败")

def enter_choice():
    optional = ('1', '2', '3')
    while True:
        try:
            print("功能选择:\n1、简单合并\n2、连接合并\n3、文件分割")
            choice = input()
            if choice not in optional:
                raise ValueError('请输入"1"或"2"或"3"')
            break
        except Exception as err:
            print(err)
    return choice

def enter_connect_columns(df_merged):
    optional_columns = set(list(df_merged))
    while True:
        print("请输入用来连接的列名(多个字段之间以空格分隔)")
        connect_columns = input().split()  # 列名列表
        if optional_columns >= set(connect_columns):  # 如果指定的连接列名包含在可选列名中
            break
        else:
            print("可选列名有:{}\n请重新输入".format(optional_columns))
    return connect_columns

def enter_split_columns(df_total):
    optional_columns = set(list(df_total))
    while True:
        print("请输入用来分割的列名(多个字段之间以空格分隔)")
        split_columns = input().split()  # 列名列表
        if optional_columns >= set(split_columns):  # 如果指定的分割列名包含在可选列名中
            break
        else:
            print("可选列名有:{}\n请重新输入".format(optional_columns))
    return split_columns

def main():
    choice = enter_choice()
    if choice == '1':  # 简单合并
        while True:
            print("请输入用来简单合并的文件夹路径:")
            dir_path = input().replace('"','')
            try:
                excel_simple_merge(dir_path, save_name='result.xlsx')
                break
            except Exception as err:
                print(err)
                print("请检查输入的文件夹路径")
    elif choice == '2':  # 连接合并
        while True:
            print("请输入用来连接合并的文件夹路径:")
            dir_path = input().replace('"','')
            try:
                df_merged = excel_merge(dir_path)
                connect_columns = enter_connect_columns(df_merged)
                excel_connect_combine(df_merged, connect_columns, save_name='result.xlsx')
                break
            except Exception as err:
                print(err)
                print("请检查输入的文件夹路径")
    elif choice == '3':  # 文件分割
        while True:
            print("请输入用来分割的excel文件路径:")
            filepath = input().replace('"','')
            try:
                df_total = pd.read_excel(filepath)
                split_columns = enter_split_columns(df_total)
                excel_split(df_total, split_columns, save_dir='split_result')
                break
            except Exception as err:
                print(err)
                print("请检查输入的文件路径")


if __name__ == "__main__":
    choice = enter_choice()
    if choice == '1':  # 简单合并
        dir_path = 'simple_connect_example'
        excel_simple_merge(dir_path, save_name='result.xlsx')
    elif choice == '2':  # 连接合并
        dir_path = 'connect_merge_example'
        df_merged = excel_merge(dir_path)
        connect_columns = enter_connect_columns(df_merged)
        excel_connect_combine(df_merged, connect_columns, save_name='result.xlsx')
    elif choice == '3':  # 文件分割
        filepath = 'split_example' + '\\' + 'ex.xlsx'
        df_total = pd.read_excel(filepath)
        split_columns = enter_split_columns(df_total)
        excel_split(df_total, split_columns, save_dir='split_result')

