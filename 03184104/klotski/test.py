##import time
##import numpy as np
###
### dt = "2018-06-07 20:28"
### dt2 = "2018-06-09 20:27"
### x = '2017/11/1 1:00'
###转换成时间数组
### timeArray = time.strptime(dt, "%Y-%m-%d %H:%M")
### timeArray2 = time.strptime(dt2, "%Y-%m-%d %H:%M")
### #转换成时间戳
### timestamp = time.mktime(timeArray)
### timestamp2 = time.mktime(time.strptime(x, "%Y/%m/%d %H:%M"))
### value = sum(ord(dt2[i])*(len(dt)-i) for i in range(len(dt)))
##x = '0'
##y = '2017/11/1 1:40'
##print(y.index('/'))
##import pickle
##data = {1:2,3:4}
##file = open('data.pkl','rb')
### pickle.dump(data,file)
##data1 = pickle.load(file)
##file.close()
##print(data1)
##from skimage import io
##import numpy as np
##path = r"C:\Users\csx\Desktop\无框字符\A_ (2).jpg"
##img = io.imread(path)
##imgs = np.hsplit(img,3)
### print((imgs[1]==(img[300:600,300:600])).all())
### print(type(imgs))
###
##io.imshow(img[300:600,300:600])
##io.show()
# url = "http://5.push2.eastmoney.com/api/qt/clist/get?\
# cb=jQuery1124036593126956865385_1602050928386&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&\
# fs=m:0+t:6,m:0+t:13,m:0+t:80&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1602050928421"
# print(url)
import requests


def issue_topic():
    '''
    利用相应网络接口发布题目
    填写字段:letter,exclude,challenge,step,swap
    '''
    url = "http://47.102.118.1:8089/api/challenge/create"
    title = {
        "teamid":52 ,
        "data": {
            "letter": "M",
            "exclude": 9,
            "challenge": [
                [1, 7, 3],
                [0, 6, 8],
                [5, 4, 2]
            ],
            "step": 15,
            "swap": [2,7]
        },
        "token": "3585feb4-f430-4e99-b80d-99f952c41798"
    }

    r = requests.post(url,json=title)
    print(r.text)
