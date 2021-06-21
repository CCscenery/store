import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, Dropout, RepeatVector, TimeDistributed
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score,roc_auc_score,precision_score,recall_score
from tensorflow.python.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.models import load_model
import copy

# 设置完整打印dataframe
def complete_print():
    pd.set_option('expand_frame_repr',False)  # 不折叠显示
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('max_rows',None)
    pd.set_option('max_columns',None)

# plt正常显示中文标签
def plt_setup():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 结合apply方法处理数据中可能缺失的label,将其处理为0：正常
def missing_solve(x):
    if np.isnan(x):  # nan处理为0
        return 0
    else:
        return int(x)

# 构造GRU时间步长序列,剔除含有异常值的序列
def create_train_sequences(df,df_label,window_size=10,n_predict=1):
    x_list,y_list = [],[]
    length = len(df)
    cnt = 0
    for i in range(length - window_size - (n_predict-1)):
        # 如果数据中有异常数据，则剔除该序列
        if 1 in df_label.iloc[i:i+window_size+n_predict].values:
            cnt += 1
            continue
        x_list.append(df.iloc[i:(i+window_size)].values)
        y_list.append(df.iloc[(i+window_size):(i+window_size+n_predict)])
    x_array,y_array = np.array(x_list),np.array(y_list)
    print("剔除了{}个含有异常的序列".format(cnt))
    return x_array,y_array

def create_test_sequences(df,df_label,window_size=10,n_predict=1):
    x_list, y_list, label_list = [], [], []
    length = len(df)
    for i in range(length - window_size - (n_predict - 1)):
        x_list.append(df.iloc[i:(i + window_size)].values)
        y_list.append(df.iloc[(i + window_size):(i + window_size + n_predict)])
        label_list.append(df_label.iloc[(i + window_size):(i + window_size + n_predict)])
    x_array, y_array ,label_array = np.array(x_list), np.array(y_list),np.array(label_list)
    return x_array, y_array, label_array

# 按指定比例划分训练集测试集
def split_train_test(df,train_rate=0.8):
    length = len(df)
    split_index = int(length*train_rate)
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]
    return train_df,test_df

# 打印数据正常异常分布特征
def print_distribution(df):
    data_length = len(df)
    abnormal_length = len(df[df['label'] == 1])
    abnormal_rate = abnormal_length/data_length
    anomaly_index_list = df[df['label'] == 1].index.tolist()
    print("数据长度为：{}".format(data_length))
    print("异常数据个数：{}".format(abnormal_length))
    print("异常数据比例：{}".format(abnormal_rate))
    print("异常数据所在索引：{}".format(anomaly_index_list))

# 神经网络模型构建
def build_model(x_train,n_predict=1):
    model = Sequential()
    model.add(GRU(50, activation='relu', return_sequences=True,
                   input_shape=(x_train.shape[1],x_train.shape[2])))
    model.add(GRU(50, activation='relu',return_sequences=True))
    model.add(GRU(50, activation='relu'))
    model.add(Dense(n_predict))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model


if __name__ == "__main__":
    # np.random.seed(1)
    # tf.random.set_seed(1)
    # 1、读取数据
    data_path = 'datasets/cpu4.csv'
    df = pd.read_csv(data_path)
    # columns:timestamp value label
    # 转换unix时间戳为日期，可发现原数据间隔五分钟记录一次
    df['timestamp'] = pd.to_datetime(df['timestamp'],unit='s',utc=True)
    # print_distribution(df)
    # 2、划分训练集测试集
    train_rate = 0.6
    train_df,test_df = split_train_test(df,train_rate)
    # print_distribution(train_df)
    # print_distribution(test_df)
    # 3、数据标准化
    scaler = StandardScaler()
    scaler = scaler.fit(train_df[['value']])
    # complete_print()
    train_df.loc[:,'value'] = scaler.transform(train_df[['value']])
    test_df.loc[:,'value'] = scaler.transform(test_df[['value']])
    # print(train_df['value'])
    # 4、根据滑动窗口构造对应时间步长的序列，剔除异常数据
    window_size = 18
    n_predict = 1
    feature = 1
    x_train,y_train = create_train_sequences(train_df['value'],train_df['label'],window_size,n_predict)
    x_test, y_test,y_labels = create_test_sequences(test_df['value'],test_df['label'],window_size, n_predict)
    x_train = x_train.reshape(x_train.shape[0],x_train.shape[1],feature)
    x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], feature)
    # 5、模型构建
    model_path = 'GRU_one_series_v1_cpu4.h5'
    training = False
    if training:
        print("building models")
        regressor_model = build_model(x_train,n_predict)
        # regressor_model.summary()
        # 定义一个callback参数,动态调整学习率
        # 模型训练
        reduce_lr = ReduceLROnPlateau(monitor='loss',  # 监测量
                                      mode='min',  # min表示当监控量loss停止下降的时候，学习率将减小
                                      factor=0.1,  # new_lr = lr * factor(默认0.1)
                                      patience=10,  # 容许网络性能不提升的次数(默认为10)
                                      verbose=True,  # 每次更新学习率输出一条消息
                                      min_lr=1e-8  # 学习率的下限
                                      )
        history = regressor_model.fit(x_train, y_train,
                                      epochs=100, batch_size=32,
                                     callbacks=[reduce_lr],
                                     shuffle=True,verbose=2)

    else:  # training:False
        regressor_model = load_model(model_path)  # 加载已有模型
    # 6、模型评估
    scores = regressor_model.evaluate(x=x_test,
                            y=y_test,
                            verbose=0)  # silent
    mae = scores[1]
    print("mae:{}".format(mae))
    # 7、模型预测性能可视化
    # 训练集拟合效果可视化
    plt_setup()
    # show_length = 1000
    # # x_train_predict,y_train_cmp = create_test_sequences(train_df['value'].iloc[:show_length],window_size,n_predict)
    # # x_train_predict = x_train_predict.reshape(x_train_predict.shape[0],x_train_predict.shape[1],feature)
    # # pred_train = regressor_model.predict(x_train_predict)
    # pred_train = regressor_model.predict(x_train)
    # plt.figure(figsize=(12,6))
    # x = range(show_length)
    # # plt.plot(x, pred_train,color='red',label='训练集预测曲线',linewidth=1)
    # # plt.plot(x, y_train_cmp,color='green',label='训练集真实曲线',linewidth=1)
    # plt.scatter(x, pred_train[:show_length], color='red', label='训练集预测', s=2)
    # plt.scatter(x, y_train[:show_length], color='blue', label='训练集真实', s=2)
    # plt.legend()
    # plt.show()
    # # 测试集拟合效果可视化
    # pred_test = regressor_model.predict(x_test)
    # plt.figure(figsize=(12, 6))
    # x = range(show_length)
    # # plt.plot(x, pred_test[:show_length], color='red', label='测试集预测曲线',linewidth=1)
    # # plt.plot(x, y_test[:show_length], color='green', label='测试集真实曲线',linewidth=1)
    # plt.scatter(x, pred_test[:show_length], color='red', label='测试集预测', s=2)
    # plt.scatter(x, y_test[:show_length], color='blue', label='测试集真实', s=2)
    # plt.legend()
    # plt.show()
    # 8、模型保存
    if training:
        regressor_model.save(model_path)
        print("trained model already save:{}".format(model_path))

    # 9、根据重构误差阈值判异常
    x_train_pred = regressor_model.predict(x_train)
    absolute_loss = np.abs(x_train_pred-y_train)
    max_loss = np.max(absolute_loss)
    # print(max_loss)
    mean_loss = np.mean(absolute_loss)
    # print(mean_loss)
    std_loss = np.std(absolute_loss)
    # print(std_loss)
    threshold = (mean_loss + 3 * std_loss + max_loss)/2
    print("重构误差阈值为：{}".format(threshold))
    x_test_pred = regressor_model.predict(x_test)
    test_absolute_loss = np.abs(x_test_pred-y_test)
    pred_test_label = np.where(test_absolute_loss > threshold, 1, 0)
    print(test_absolute_loss[test_absolute_loss>threshold])
    print(len(test_absolute_loss[test_absolute_loss>threshold]))
    print(np.where(test_absolute_loss>threshold))
    print(np.where(y_labels==1))
    print(test_absolute_loss[np.where(y_labels==1)])

    # 10、计算评估指标
    f_score = f1_score(y_labels,pred_test_label)
    precision = precision_score(y_labels,pred_test_label)
    recall = recall_score(y_labels,pred_test_label)
    auc_score = roc_auc_score(y_labels,pred_test_label)
    print("f_score:{}".format(f_score))
    print("precision:{}".format(precision))
    print("recall:{}".format(recall))
    print("auc_score:{}".format(auc_score))




