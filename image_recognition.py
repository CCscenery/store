import requests
import json
import base64
import numpy as np
import matplotlib.pyplot as plt
import pickle
import imageio

def get_jsonstr(url):
    url = "http://47.102.118.1:8089/api/problem?stuid=031804104"
    response = requests.get(url)
    jsonstr = json.loads(response.text)
    return jsonstr

def split_image(img):  # 输入为图像矩阵np
    '''分割图像'''
    imgs = []
    for i in range(0,900,300):
        for j in range(0,900,300):
            imgs.append(img[i:i+300,j:j+300].tolist())
    return (imgs)  # 返回值是九块图像矩阵的列表

def encode_image(title_image,store_image):
    '''图像编码为数字'''
    current_table = []  # 图像对应的表数字编码
    ans_type = list(range(1,10))  # 答案类型
    for ls_title in title_image:
        try:
            pos_code = store_image.index(ls_title)+1
            current_table.append(pos_code)
            ans_type.remove(pos_code)
        except:
            current_table.append(0)  # IndexError:空格匹配不到
    return current_table,ans_type[0]  # 返回表编码和答案类型

def main(json_image):
    # 读取无框字符分割成9份后的图像列表
    save_name = 'ls_img.pkl'
    pkl_file = open(save_name, 'rb')
    store_images = pickle.load(pkl_file)
    pkl_file.close()

    # 获取题给图像
    bs64_img = base64.b64decode(json_image)  # 图像是base64编码
    np_img = imageio.imread(bs64_img)
    title_image = split_image(np_img)

    for ls_store in store_images:  # 遍历存储的所有无框字符
        count = 0
        for ls_title in title_image:  # 遍历题给图像块
            if (np.array(ls_title) == 255).all() == True:  # 被挖去的空白
                continue  # 跳过
            if ls_title in ls_store:  # 该图块在无框字符中
                count += 1
            else:
                break
            if count == 8:  # 除空白块外都相同，则判就是该无框字符，对题给图块进行编码
                current_table, ans_type = encode_image(title_image, ls_store)
                return current_table,ans_type

if __name__ == "__main__":

    # 读取无框字符分割成9份后的图像列表
    save_name = 'ls_img.pkl'
    pkl_file = open(save_name,'rb')
    store_images = pickle.load(pkl_file)
    pkl_file.close()

    # 获取题给图像
    url = "http://47.102.118.1:8089/api/problem?stuid=031804104"
    response = requests.get(url)
    jsonstr = json.loads(response.text)
    bs64_img = base64.b64decode(jsonstr['img']) #图像是base64编码
    np_img = imageio.imread(bs64_img)
    title_image = split_image(np_img)
    plt.imshow(np_img)
    plt.show()

    for ls_store in store_images: #遍历存储的所存储的无框字符
        count = 0
        for ls_title in title_image: #遍历题给图像块
            if (np.array(ls_title) == 255).all() == True:  # 被挖去的空白
                continue  # 跳过
            if ls_title in ls_store:  # 该图块在无框字符中
                count += 1
            else:
                break
            if count == 8:  # 除空白块外都相同，则判就是该无框字符，对题给图块进行编码
                current_table,ans_type = encode_image(title_image,ls_store)
                print(current_table, ans_type)
                ls = [331,332,333,334,335,336,337,338,339]
                for i in range(9):
                    plt.subplot(ls[i])
                    plt.imshow(np.array(ls_store[i]))
                plt.show()
                for i in range(9):
                    plt.subplot(ls[i])
                    plt.imshow(np.array(title_image[i]))
                plt.show()
                break



