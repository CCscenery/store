import excel_to_text
import excel_to_table

def enter_choice():
    optional = ('1', '2')
    while True:
        try:
            print("功能选择:\n1、以文本形式导出批量word\n2、以表格形式导出批量word\n请选择:(1/2):")
            choice = input()
            if choice not in optional:
                raise ValueError('请输入"1"或"2"')
            break
        except Exception as err:
            print(err)
    return choice

def main():
    choice = enter_choice()
    if choice == '1':
        while True:
            print("请输入要处理的excel文件绝对路径:")
            file_path = input()
            print("请输入模板文件绝对路径:")
            formatpath = input()
            try:
                excel_to_text.main(file_path,formatpath)
                break
            except Exception as err:
                print(err)
                print("请检查文件路径是否正确")
    elif choice == '2':
        while True:
            print("请输入要处理的excel文件绝对路径:")
            file_path = input()
            try:
                excel_to_table.main(file_path)
                break
            except Exception as err:
                print(err)
                print("请检查文件路径是否正确")


if __name__ == "__main__":
    choice = enter_choice()
    file_path = '学生信息表.xlsx'  # 要处理的excel文件路径
    if choice == '1':
        formatpath = 'template_text.docx'
        excel_to_text.main(file_path,formatpath)
    elif choice == '2':
        excel_to_table.main(file_path)




