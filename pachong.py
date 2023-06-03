import requests
# 解析HTML/XMLde文档，这个etree就是代表一个DOM树，
from lxml import etree
# 控制时间
from time import sleep
# 操作系统
import os
# 用来数据清洗和数据处理的工具 数据分析
import pandas as pd
# 正则表达式 通过正则搜索想要的内容
import re


BOOKS = []
IMGURLS = []


# 2. 获取网页源代码
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    #     为了防止反爬
    }
    # 异常处理
    try:
        html = requests.get(url, headers=headers)
        # 声明编码方式 整个服务器返回的内容封装在html里面
        html.encoding = html.apparent_encoding
        # 判断
        if html.status_code == 200:
            print('成功获取源代码')
            # print(html.text)
    except Exception as e:
        print('获取源代码失败：%s' % e)
    # 返回html
    return html.text


# 3. 解析网页源代码
def parse_html(html):
    # elements是一种容器，用来操作dom树的，必须含有完整信息的节点才是一个元素
    html = etree.HTML(html)
    # 每个图书信息分别保存在 class="indent" 的div下的 table标签内
    # //表示从当前节点选取子孙节点往下走，@是一个筛选器，//筛选出来的基础上去找下一层下一层是table
    tables = html.xpath("//div[@class='indent']//table")
    # print(len(tables))  # 打印之后如果是25的话就是对的
    books = []
    imgUrls = []

    # 遍历通过xpath得到的li标签列表
    # 因为要获取标题文本，所以xpath表达式要追加 /text(), t.xpath返回的是一个列表，且列表中只有一个元素所以追加一个[0]
    for t in tables:
        # title = t.xpath(".//div[@class='p12']/a/@title")  # 匹配得到的是空的
        # 书名
        # ./一个斜杠指从当前节点里面找，//两个斜杠从当前往下找
        # 【0】是因为xpath 返回的是一个列表
        title = t.xpath(".//td[@valign='top']//a/@title")[0]
        # 链接
        link = t.xpath(".//td[@valign='top']//a/@href")[0]

        # 获取pl标签的字符串
        pl = t.xpath(".//td[@valign='top']//p[1]/text()")[0]

        # 截取国家
        if '['  in pl:
            # 【1】是指[分割以后选择右边部分，【0】是指]分割以后选择左边部分
            country = pl.split('[')[1].split(']')[0]
        elif '【'  in pl:
            country = pl.split('【')[1].split('】')[0]
        elif '（'  in pl:
            country = pl.split('（')[1].split('）')[0]
        else:
            country = '中'  # 没有国家的默认为“中国”

        # 截取作者

        # if '[' in pl:
        #     author = pl.split(']')[1].split('/')[0].replace(" ", "")
        # elif len(pl.split('/')) == 3:
        #     author = '无'
        # elif len(pl.split('/')) == 2:
        #     author = pl.split('/')[0]
        #
        # elif '[' not in pl:
        #     if len(pl.split('/')) == 4:
        #         author = pl.split('/')[-4]
        #     elif len(pl.split('/')) == 5:
        #         author = pl.split('/')[-5]
        #     elif len(pl.split('/')) == 6:
        #         author = pl.split('/')[-6]
        #
        # else:
        #     author = '无'

        if '[' in pl:
            author = pl.split(']')[1].split('/')[0].replace(" ", "")
        elif '【' in pl:
            author = pl.split('】')[1].split('/')[0].replace(" ", "")
        elif '（' in pl:
            author = pl.split('）')[1].split('/')[0].replace(" ", "")
        # elif len(pl.split('/')) == 2:
        #     author = pl.split('/')[0]
        elif len(pl.split('/')) == 3:
            author = '无'
        elif len(pl.split('/')) > 3:
            # If 'pl' has more than 3 '/' characters, extract the author's name using the last 4-6 parts
            author_parts = pl.split('/')
            author = ''
            for i in range(-4, -7, -1):
                if abs(i) > len(author_parts):
                    break
                if author_parts[i].strip():
                    author = author_parts[i].strip()
                    break
        else:
            author = '无'

        # 截取翻译者
        # if len(pl.split('/')) == 3:
        #     translator = ' '
        # elif '[' in pl:
        #     if len(pl.split('/')) == 4:
        #         translator = pl.split('/')[-3]
        #     elif len(pl.split('/')) == 5:
        #         translator = pl.split('/')[-4]
        #     elif len(pl.split('/')) == 6:
        #         translator = pl.split('/')[-5]
        #
        # else:
        #     translator = ' '

        # 截取翻译者
        if len(pl.split('/')) >= 5:
            translator = pl.split('/')[1]
        else:
            translator = ' '

        # 截取出版社
        if len(pl.split('/')) == 2:
            publisher = pl.split('/')[0]
        elif len(pl.split('/')) == 3:
            publisher = pl.split('/')[0]

        elif '[' in pl:
            if len(pl.split('/')) == 4:
                publisher = pl.split('/')[1]
            elif len(pl.split('/')) == 5:
                publisher = pl.split('/')[2]
            elif len(pl.split('/')) == 6:
                publisher = pl.split('/')[-3]
            elif len(pl.split('/')) == 7:
                publisher = pl.split('/')[-4]

        elif '[' not in pl:
            # if len(pl.split('/'))== 3:
            publisher = pl.split('/')[-3]
        # if len(pl.split('/')) == 6:
        #     publisher = pl.split('/')[-3]
        # elif len(pl.split('/')) == 7:
        #      publisher = pl.split('/')[-4]

        # 截取出版时间
        if len(pl.split('/')) == 2:
            time = '不详'
        elif len(pl.split('/')) == 3:
            time = pl.split('/')[-2]
        elif len(pl.split('/')) == 4:
            time = pl.split('/')[-2]
        elif len(pl.split('/')) >= 5 :
            time = pl.split('/')[-2]


        # 截取单价
        # if '元' in pl:
        #     price = pl.split('/')[-1].split('元')[0]
        # else:
        #     price = pl.split('/')[-1]

        if len(pl.split('/')) == 6:
            if '元' in pl:  # 如果价格信息中包含 "元"
            # 如果字符串按照 "/" 分割后的子字符串数量为 6（如"[英] ... / 1981-8 / 53.00元/68.00元"）
            # 则将价格信息提取出来，并将其格式转换为“价格1/价格2”的格式
                price = '/'.join(pl.split('/')[-1:-3:-1]).replace("元", "")
        else:
            # 否则按照之前的代码提取价格信息
            if '元' in pl:
                price = pl.split('/')[-1].split('元')[0]
            else:
                price = pl.split('/')[-1]
        # 获取星级数
        str1 = t.xpath(".//td[@valign='top']//div[@class='star clearfix']/span[1]/@class")[0].replace("allstar", "")
        # 此时获取到的数字其实是字符串类型，不能直接%10，需要把str转化为int
        num = int(str1)
        star = num / 10
        # 获取评分
        score = t.xpath(".//td[@valign='top']//div[@class='star clearfix']/span[2]/text()")[0]
        # 获取评价人数
        pnum = t.xpath(".//td[@valign='top']//div[@class='star clearfix']/span[3]/text()")[0]
        # re是一个正则表达式，\D表示所有非数字的东西，sub是减掉，pnum中的非数字变成空
        people = re.sub("\D", "", pnum)

        # 获取简介
        comments = t.xpath(".//p[@class='quote']/span/text()")
        comment = comments[0] if len(comments) != 0 else "无"

        book = {
            '书名': title,
            '链接': link,
            '国家': country,
            '作者': author,
            '翻译者': translator,
            '出版社': publisher,
            '出版时间': time,
            '价格': price,
            '星级': star,
            '评分': score,
            '评价人数': people,
            '简介': comment
        }

        # 图片
        imgUrl = t.xpath(".//a/img/@src")[0]
        # print(imgUrl)

        books.append(book)
        imgUrls.append(imgUrl)

    return books, imgUrls


# 4. 下载图片保存文件
def downloadimg(url, book):
    # 判断文件夹是否在指定路径下面,建立文件夹并把指定路径移到文件夹下面
    if 'img' in os.listdir(r'D:\prog'):
        pass
    else:
        os.mkdir(r'D:\prog\img')
    # 改变当前工作目录到指定的路径
    os.chdir(r'D:\prog\img')
    # 返回img的二进制流
    img = requests.request('GET', url).content

    with open(book['书名'] + '.jpg', 'wb') as f:
        # print('正在下载: %s' % url)
        f.write(img)


# 5. 数据预处理
# def processData():

if __name__ == '__main__':
    # url = 'https://book.douban.com/top250?start=0'
    # 10页循环遍历
    for i in range(10):
        # 2. 定义url并获取网页源代码
        url = 'https://book.douban.com/top250?start={}'.format(i * 25)
        # print(url)
        # 获得该url页面里的内容
        html = get_html(url)
        # 3. 解析网页源代码
        sleep(1)
        books = parse_html(html)[0]
        imgUrls = parse_html(html)[1]

        BOOKS.extend(books)
        IMGURLS.extend(imgUrls)

    # 4. 下载图片保存文件
    for i in range(250):
        # sleep(1)
        # download_img(folder = 'ooxx',pages = 10):#包含两个参数:目标文件夹;爬取的页面数量
        downloadimg(IMGURLS[i], BOOKS[i])

    os.chdir(r'D:/prog/img')

    # 以csv格式写入本地
    # DataFrame是一个表格，经过排序的列表集
    bookdata = pd.DataFrame(BOOKS)
    bookdata.to_csv('D:/prog/book.csv', index=False)
    print("图书信息写入本地成功")

    # 以txt格式写入本地错误
    # 得到的是字典格式，要想写成txt格式需要先转化成字符串格式
    # for i in range(25):
    #     with open('book.txt', 'a') as f:
    #         f.write(books[i] + '\n')
