from ExcelToWord import excel_to_word
from WordToExcel import word_to_excel
from ProcessExcel import process_excel
from WirteBatchWord import batch_word


def enter_choice():
    optional = ('1', '2', '3', '4')
    while True:
        try:
            print("功能选择:\n1、excel导出批量word\n2、批量word归并为excel")
            print("3、excel多到一或一到多的转换\n4、批量写入word")
            choice = input()
            if choice not in optional:
                raise ValueError('请输入"1"、"2"、"3"、"4"中的一个')
            break
        except Exception as err:
            print(err)
    return choice

def enter_whether_quit():
    optional = '是否YNyn'
    sure = '是Yy'
    while True:
        try:
            print("是否退出程序?(是/否)(y/n)")
            choice = input()
            if choice not in optional:
                raise ValueError('请按照提示输入')
            break
        except Exception as err:
            print(err)
    choice = True if choice in sure else False
    return choice

if __name__ == "__main__":
    while True:
        choice = enter_choice()
        if choice == '1':  # excel导出批量word
            excel_to_word.main()
        elif choice == '2':  # 批量word归并为excel
            word_to_excel.main()
        elif choice == '3':
            process_excel.main()
        elif choice == '4':
            batch_word.main()
        choice = enter_whether_quit()
        if choice:
            break