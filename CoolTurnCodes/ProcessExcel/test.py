import os
for i in os.scandir(r"C:\Users\csx\Desktop\ProcessExcel\excel_combine_connect"):
    print(i.name)
    print(i.path)
    print(i.is_dir())
    print(i.is_file())