import batch_word_text
import batch_word_table


def enter_choice():
    optional = ('1', '2')
    while True:
        try:
            print("功能选择:\n1、批量写入文本形式\n2、批量写入表格形式\n请选择:(1/2):")
            choice = input()
            if choice not in optional:
                raise ValueError('请输入"1"或"2"')
            break
        except Exception as err:
            print(err)
    return choice

def main():
    choice = enter_choice()
    if choice == '1':  # 批量写入文本形式
        while True:
            print("请输入模板文件绝对路径:")
            formatpath = input()
            try:
                batch_word_text.main(formatpath)
                break
            except Exception as err:
                print(err)
                print("请检查文件路径是否正确")
    elif choice == '2':  # 批量写入表格形式
        while True:
            print("请输入模板文件绝对路径:")
            formatpath = input()
            try:
                batch_word_table.main(formatpath)
                break
            except Exception as err:
                print(err)
                print("请检查文件路径是否正确")


if __name__ == "__main__":
    choice = enter_choice()
    if choice == '1':  # 批量写入文本形式
        formatpath = 'template_text.docx'
        batch_word_text.main(formatpath)
    elif choice == '2':  # 批量写入表格形式
        formatpath = 'template_table.docx'
        batch_word_table.main(formatpath)

