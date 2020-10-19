import numpy as np
import os
import skimage
import pickle
import imageio
import matplotlib.pyplot as plt

def split_image(img): #输入为图像矩阵np
    imgs = []
    for i in range(0,900,300):
        for j in range(0,900,300):
            imgs.append(img[i:i+300,j:j+300].tolist()) #嵌套列表，方便后续处理
    return (imgs) #返回值是九块图像矩阵的列表

def walk_file(path): #遍历文件夹下所有文件（可嵌套文件夹）
    # root 表示当前正在访问的文件夹路径
    # dirs 表示该文件夹下的子目录名list
    # files 表示该文件夹下的文件list
    file_list = []
    for root, dirs, files in os.walk(path):
        for f in files:
            file_list.append(os.path.join(root, f))
    return file_list


one_imgs = []
path = r"C:\Users\csx\Desktop\无框字符"
file_list = walk_file(path)
for file in file_list: #共36个图像文件
    # np_img = skimage.io.imread(file)
    np_img = imageio.imread(file)
    # plt.imshow(np_img)
    # plt.show()
    # np_img[np_img<100],np_img[np_img>200] = 0,255 #图像二值化（黑白）
    img = split_image(np_img)
    one_imgs.append(img)


# save_name = 'ls_img.pkl'
# pkl_file = open(save_name, 'wb')
# pickle.dump(one_imgs, pkl_file)
# print('pkl already save')
# pkl_file.close()
