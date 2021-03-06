import re
import jieba.analyse
import os
from sklearn.metrics.pairwise import cosine_similarity
import timeit
import sys


def read_file(filepath): #读取文件
    content = ''
    try: #文件路径可能有误
        with open(filepath,encoding='utf-8') as f:
            content = f.read()
    except Exception as err:
        print(err)
    return content


def get_filenames(path): #获取path下所有文件路径
    filenames = []
    for root, dirs, files in os.walk(path):
        for name in files:
            filenames.append(os.path.join(root, name))
    return filenames


def wirte_file(filepath,ans): #将答案写入filepath文件
    try: # 写入文件路径可能有误
        with open(filepath,'w') as f:
            f.write(str(ans))
        print("The answer has been written on the {}".format(filepath))
    except Exception as err:
        print(err)


class Similarity():

    def term_frequency(word_dict, keywords):  # 词频tf编码
        cut_code = [0]*len(word_dict) #初始化
        for word in keywords:
            cut_code[word_dict[word]] += 1
        return cut_code

    def get_dict(words): # 初始化词与数据映射的字典
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

    def rank_keyword(content): #提取关键词
        textrank = jieba.analyse.textrank
        keywords = textrank(content)
        return ','.join(keywords)

    def extract_keyword(content): #提取关键词
        topnum = 200 #设置关键词数
        keywords = jieba.analyse.extract_tags(content,topK=topnum)
        return keywords

    def get_cos(encode): #返回余弦相似度
        return cosine_similarity(encode)[1][0]


if __name__ == "__main__":
    starttime = timeit.default_timer()  # 开始计时

    orgin_file = sys.argv[1]  # 原文件路径
    content = read_file(orgin_file)
    orgin_content = Similarity.pretreatment(content)
    orgin_keywords = Similarity.extract_keyword(orgin_content)

    copy_file = sys.argv[2]  # 抄袭文件路径
    content = read_file(copy_file)
    copy_content = Similarity.pretreatment(content)
    copy_keywords = Similarity.extract_keyword(copy_content)

    union = set(orgin_keywords).union(set(copy_keywords))  # 关键词并集
    word_dict = Similarity.get_dict(union)
    orgin_encode = Similarity.term_frequency(word_dict, orgin_keywords)  # 原文件关键词对应tf编码
    copy_encode = Similarity.term_frequency(word_dict, copy_keywords)  # 抄袭文件关键词对应tf编码
    sample = [orgin_encode, copy_encode]

    same_rate = Similarity.get_cos(sample)
    ans = '%.2f' % same_rate  # 答案为浮点型，精确到小数点后两位
    print('两文本重复率为{}'.format(ans))

    endtime = timeit.default_timer()  # 计时结束
    print('Running time: {:.2f} Seconds'.format(endtime - starttime))

    ans_file = sys.argv[3]  # 输出文件路径
    wirte_file(ans_file, str(ans))
    sys.exit(0)  # 程序结束返回0



