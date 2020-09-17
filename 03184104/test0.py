from main import Similarity
import unittest

class MyTest(unittest.TestCase):

    def tearDown(self) -> None:
        print("test over!")

    def test_add(self):
        print("orig_0.8_add.txt 重复率")
        similarity = Similarity.("C:\测试文件\orig.txt","C:\测试文件\orig_0.8_add.txt")
    print(similarity)

def test_del(self):
    print("orig_0.8_del.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt","C:\测试文件\orig_0.8_del.txt")
    print(similarity)

def test_dis_1(self):
    print("orig_0.8_dis_1.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt", "C:\测试文件\orig_0.8_dis_1.txt")
    print(similarity)

def test_dis_3(self):
    print("orig_0.8_dis_3.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt", "C:\测试文件\orig_0.8_dis_3.txt")
    print(similarity)

def test_dis_7(self):
    print("orig_0.8_dis_7.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt", "C:\测试文件\orig_0.8_dis_7.txt")
    print(similarity)

def test_dis_10(self):
    print("orig_0.8_dis_10.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt","C:\测试文件\orig_0.8_dis_10.txt")
    print(similarity)

def test_dis_15(self):
    print("orig_0.8_dis_15.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt","C:\测试文件\orig_0.8_dis_15.txt")
    print(similarity)

def test_mix(self):
    print("orig_0.8_mix.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt","C:\测试文件\orig_0.8_mix.txt")
    print(similarity)

def test_rep(self):
    print("orig_0.8_rep.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt","C:\测试文件\orig_0.8_rep.txt")
    print(similarity)

def test_mine1(self):
    print("mine1.txt 重复率")
    similarity = lc2.compare("C:\测试文件\orig.txt","C:\测试文件\mine1.txt")
    print(similarity)
if __name__ == '__main__':
    unittest.main()