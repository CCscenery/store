import re
import jieba.analyse
import os
from sklearn.metrics.pairwise import cosine_similarity
import timeit
import sys


def read_file(filepath): #读取文件
    with open(filepath,encoding='utf-8') as f:
        content = f.read()
    return content

def get_filenames(path):
    filenames = []
    for root, dirs, files in os.walk(path):
        for name in files:
            filenames.append(os.path.join(root, name))
    return filenames


def wirte_file(filepath,ans):
    with open(filepath,'w') as f:
        f.write(str(ans))
    print("The answer has been written on the {}".format(filepath))


class Similarity():

    def one_hot(word_dict, keywords):  # oneHot编码
        # cut_code = [word_dict[word] for word in keywords]
        cut_code = [0]*len(word_dict) #初始化
        for word in keywords:
            cut_code[word_dict[word]] += 1
        return cut_code

    def get_dict(words):
        word_dict = {}
        i = 0
        for word in union:
            word_dict[word] = i
            i += 1
        return word_dict

    def pretreatment(content): #预处理掉无关符号(空格、换行符、标点)
        punctuation = '!,;:?"\' '
        content = re.sub(r'[{}]+'.format(punctuation),'',content)
        return content.replace("\n","") #换行符

    def rank_keyword(content):
        textrank = jieba.analyse.textrank
        keywords = textrank(content)
        return ','.join(keywords)

    def extract_keyword(content):
        topnum = 100 #设置关键词数
        keywords = jieba.analyse.extract_tags(content,topK=topnum)
        return keywords

    def get_cos(encode):
        return cosine_similarity(encode)[1][0]


if __name__ == "__main__":
    starttime = timeit.default_timer() #开始计时

    root = os.getcwd() #与测试文件在同一目录下
    filename = get_filenames(root)
    orgin_file = filename[0] #原文件路径
    content = read_file(orgin_file)
    orgin_content = Similarity.pretreatment(content)
    orgin_keywords = Similarity.extract_keyword(orgin_content)

    for i in range(1,len(filename)):
        copy_file = filename[i]#抄袭文件路径
        content = read_file(copy_file)
        copy_content = Similarity.pretreatment(content)
        copy_keywords = Similarity.extract_keyword(copy_content)

        union = set(orgin_keywords).union(set(copy_keywords)) #关键词并集
        word_dict = Similarity.get_dict(union)
        orgin_encode = Similarity.one_hot(word_dict,orgin_keywords) #原文件关键词对应one_hot编码
        copy_encode = Similarity.one_hot(word_dict,copy_keywords) #抄袭文件关键词对应one_hot编码
        sample = [orgin_encode,copy_encode]

        same_rate = Similarity.get_cos(sample)
        ans = '%.2f' % same_rate #答案为浮点型，精确到小数点后两位
        print('{}和{}的重复率为{}'.format(orgin_file,copy_file,ans))

    endtime = timeit.default_timer() #计时结束
    print('Running time: {:.2f} Seconds'.format(endtime-starttime))





