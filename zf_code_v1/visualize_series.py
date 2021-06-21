import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import matplotlib.dates as mdates
import numpy as np

def complete_print():
    pd.set_option('expand_frame_repr',False)  # 不折叠显示
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('max_rows',None)
    pd.set_option('max_columns',None)

def plt_setup():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def missing_solve(x):
    if np.isnan(x):  # nan处理为0
        return 0
    else:
        return int(x)

if __name__ == "__main__":
    data_path = 'datasets/server_res_eth1out_curve_61.csv'
    df = pd.read_csv(data_path)
    time_index_name = 'timestamp'
    # df[time_index_name] = pd.to_datetime(df[time_index_name],unit='s')
    # df.set_index(time_index_name,inplace=True)
    # complete_print()
    # print(df['label'])
    show_length = 2000  # 显示前n条数据
    # time_series = df['timestamp'].iloc[:show_length]
    time_series = range(2100,2400)
    value_series = df['value'].iloc[2100:2400]
    label_series = df['label'].iloc[2100:2400].apply(lambda x:missing_solve(x))
    # print(plt.style.available)
    # plt.style.use('fivethirtyeight')
    # ax = time_series.plot(y=label_series,color='blue',figsize=(10,5),linewidth=1)

    fig,ax = plt.subplots(figsize=(14,7))
    x_major_locator = MultipleLocator(10)  # 把x轴的刻度间隔设置为1
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xticks(rotation=90)  # 横坐标旋转刻度
    # ax.set_xticks(time_series)
    ax.set_title('server_res_2100-2400')
    ax.set_xlabel('timestamp')
    ax.set_ylabel('value')
    # for label in ax.get_xticklabels():
    #     label.set_visible(False)
    # for label in ax.get_xticklabels()[::10]:
    #     label.set_visible(True)
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))  # 设置横坐标日期间隔
    color_list = ["blue","red"]
    color_map = [color_list[i] for i in label_series]
    ax.scatter(x=time_series, y=value_series,s=3,c=color_map)
    plt.xlim(2100,2400)
    plt.grid()
    plt.show()
