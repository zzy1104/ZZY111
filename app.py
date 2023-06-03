from flask import Flask, render_template #如果要是用render_template返回渲染的模板。请在项目的主目录中加入一个目录templates，jinjia--》用来处理前后端数据交互
# flask是一个web框架，可以结合MVC模式进行开发，包括werk和jinja2两个核心数据库
import pymysql

# 先实例化一个app
app = Flask(__name__)

# app中的route装饰器
@app.route('/')
# 试图函数 在flask中的httpresponse就是直接返回字符串
def index():
    return render_template("index.html")  #render是用来渲染html模板并返回


@app.route('/index')
def home():
    # return render_template("index.html")
    return index()


@app.route('/movie')
def movie():
    datalist = []
    # 连接数据库的代码
    con = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pass111',
        db='pachong',
        charset='utf8'
    )
    # 游标 是数据库中sql语言和高级语言出现交互的时候，相当于一个缓冲区
    cur = con.cursor()
    sql = "select * from books"
    data = cur.execute(sql)
    # 每执行一次游标，往后推一行
    result = cur.fetchall()
    for item in result:
        datalist.append(item)
    cur.close()
    cur.close()
    print(datalist)
    return render_template("movie.html", movies=datalist)


@app.route('/score')
def score():
    score = []  # 评分
    num = []  # 每个评分所统计出的电影数量
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pass111',
        db='pachong',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from book_score_num"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        score.append(str(item[0]))
        num.append(item[1])

    cur.close()
    conn.close()
    return render_template("score.html", score=score, num=num)


@app.route('/country')
def country():
    country = []  # 评分
    num = []  # 每个评分所统计出的电影数量
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pass111',
        db='pachong',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from book_country_num"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        country.append(str(item[0]))
        num.append(item[1])

    cur.close()
    conn.close()
    return render_template("country.html", country=country, num=num)


@app.route('/peopletop10')
def peopletop10():
    people = []  # 评论人数
    title = []  # 书名
    s = []
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pass111',
        db='pachong',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from book_people_title"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        s.append(item)
        people.append(str(item[0]))
        title.append(item[1])

    cur.close()
    conn.close()
    return render_template("peopletop10.html", people=people, title=title)


@app.route('/presstime')
def presstime():
    year = []
    num = []
    s = []
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pass111',
        db='pachong',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from book_presstime_num"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        s.append(item)
        year.append(str(item[0]))
        num.append(item[1])

    cur.close()
    conn.close()
    return render_template("presstime.html", year=year, num=num)


@app.route('/publisher')
def publisher():
    year = []
    num = []
    s = []
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pass111',
        db='pachong',
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from book_publisher_num"
    data = cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        s.append(item)
        year.append(str(item[0]))
        num.append(item[1])

    cur.close()
    conn.close()
    return render_template("publisher.html", year=year, num=num)


@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/team')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    app.run()
