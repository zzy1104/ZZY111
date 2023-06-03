# 数据清洗 提供了高性能、易于使用的数据结构和数据分析工具、帮助我们操作csv、excel等等格式的数据
import pandas as pd
# 正则
import re
import time

# 先读取数据文件
data = pd.read_csv('D:/prog/book.csv')
# DataFrame格式
result = pd.DataFrame(data)

# dropna是将无效数据删除，axis=0是按行删除，axis=1是按列删除，‘any’是（带缺失值就删除）缺失值的所有行/列 ，如果吧any改成all——就是一整行缺失才删掉
a = result.dropna(axis=0, how='any')
# 控制显示选项，填NONe就是不省略
pd.set_option('display.max_rows', None)  # 输出全部行，不省略

b = u'数据'
number = 1

b1 = '1981-8'
li1 = a['出版社']
for i in range(0, len(li1)):
    try:
        if b1 in li1[i]:
            # print(number,li1[i])
            number += 1
            # 将li1中 为1981-8的这一行删掉
            # n=a['书名'][i]
            a = a.drop(i, axis=0)
    except:
        pass

b2 = '中国基督'
# a['出版时间'] = a['出版时间'].str[0: 5]
a['出版时间'] = a['出版时间'].str.replace('年', '-').str.replace('月', '.')
a['出版时间'] = pd.to_datetime(a['出版时间']).dt.strftime('%Y/%m')
# a['出版时间'] = a['出版时间'].apply(lambda x: re.sub(r'(\d{4})[.-](\d{1,2})', r'\g<1>/\g<2>', x))

li2 = a.loc[:, '出版时间'].copy()
for i in range(0, len(li2)):
    try:
        # li2[i] = li2[i].replace('.', '-')
        # li2[i] = li2[i].replace('年', '-').replace('月', '')
        if b2 in li2[i]:
            # print(number,li2[i])
            number += 1
            a = a.drop(i, axis=0)
    except:
        pass
a.loc[:, '出版时间'] = li2


b3 = ' NT$350'
b31= ' CNY 20.00'
# 其中 .loc[] 方法用于选择特定的行和列，这里选择所有行和 价格 列，并用 copy() 方法创建一个副本，避免由于直接平移数据集而出现错误。
# 将这个副本命名为 li3，接下来按照您之前的代码修改 li3 中的数据，并将修改后的 li3 再次分配回原始 DataFrame 中的 价格 列
li3 = a.loc[:, '价格'].copy()
for i in range(0, len(li3)):
    try:

        if b3 in li3[i]:
            print(i)
            li3[i] = li3[i].replace(' NT$350', '')
        if b31 in li3[i]:
            print(i)
            li3[i] = li3[i].replace(' CNY 20.00', '')

    except:
        pass
a.loc[:, '价格'] = li3

b41 = '清'
b42 = '明'
li4 = a.loc[:, '国家'].copy()
l14 = li4.str.replace("国", "")
for i in range(0, len(li4)):
    try:
        if b41 in li4[i]:
            li4[i]=li4[i].replace('清', '中')
        if b42 in li4[i]:
            li4[i] = li4[i].replace('明', '中')
    except:
        pass
a.loc[:, '国家']=li4
# time.sleep(3)
# index=False 参数可以控制是否将行索引写入到输出文件中，True 表示写入行索引，False 表示不写入。
# a.to_csv('D:/prog/newbook.csv', index=False)
import os

# 设置文件路径和文件名
file_path = 'D:/prog'
file_name = 'newbook.csv'

# 判断文件是否存在，如果存在则删除
if os.path.isfile(os.path.join(file_path, file_name)):
    os.remove(os.path.join(file_path, file_name))

# 生成新的 CSV 文件
a.to_csv(os.path.join(file_path, file_name), index=False)