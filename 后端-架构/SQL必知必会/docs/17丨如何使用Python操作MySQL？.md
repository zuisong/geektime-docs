我们之前都是直接在DBMS里面进行SQL的操作，实际上我们还可以通过后端语言对DBMS进行访问以及进行相应的操作，这样更具有灵活性，可以实现一些较为复杂的操作。作为一个后端开发人员，掌握一些SQL技术是必须的；作为一个数据库管理人员，了解后端语言如何开发和管理数据库也是很有必要的。

今天我以Python为例，讲解下如何对MySQL数据库进行操作。你需要掌握以下几个方面的内容：

1. Python的DB API规范是什么，遵守这个规范有什么用？
2. 基于DB API，MySQL官方提供了驱动器mysql-connector，如何使用它来完成对数据库管理系统的操作？
3. CRUD是最常见的数据库的操作，分别对应数据的增加、读取、修改和删除。在掌握了mysql-connector的使用方法之后，如何完成对数据表的CRUD操作？

## Python DB API规范

Python可以支持非常多的数据库管理系统，比如MySQL、Oracle、SQL Server和PostgreSQL等。为了实现对这些DBMS的统一访问，Python需要遵守一个规范，这就是DB API规范。我在下图中列出了DB API规范的作用，这个规范给我们提供了数据库对象连接、对象交互和异常处理的方式，为各种DBMS提供了统一的访问接口。这样做的好处就是如果项目需要切换数据库，Python层的代码移植会比较简单。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（42） 💬（3）<div>import json
import traceback
import mysql.connector

# 读取数据库链接配置文件
with open(&#39;mysql.json&#39;, encoding=&#39;utf-8&#39;) as con_json:
    con_dict = json.load(con_json)

# 打开数据库链接
db = mysql.connector.connect(
    host=con_dict[&#39;host&#39;],
    user=con_dict[&#39;user&#39;],
    passwd=con_dict[&#39;passwd&#39;],
    database=con_dict[&#39;database&#39;],
    auth_plugin=con_dict[&#39;auth_plugin&#39;],
)

# 获取操作游标
cursor = db.cursor()
try:
    sql = &#39;SELECT id, name, hp_max FROM heros WHERE hp_max&gt;6000&#39;
    cursor.execute(sql)
    data = cursor.fetchall()
    print(cursor.rowcount, &#39;查询成功。&#39;)
    for each_hero in data:
        print(each_hero)
except Exception as e:
    # 打印异常信息
    traceback.print_exc()
finally:
    cursor.close()
    db.close()
# 建议吧数据库链接信息写到配置文件里，防止密码泄露。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/45/b88a1794.jpg" width="30px"><span>一叶知秋</span> 👍（9） 💬（1）<div>sqlalchemy用习惯了。。。献丑来一段Python代码吧
```Python
# -*- coding:utf-8 -*-
from sqlalchemy import and_
from sqlalchemy import Column, INT, FLOAT, VARCHAR
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Test_db:
    def __init__(self):
        &quot;&quot;&quot;此处填上自己的连接配置&quot;&quot;&quot;
        self.engine = create_engine(
            &#39;mysql+pymysql:&#47;&#47;username:password@host:port&#47;db_name?charset=utf8&#39;)
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def query_all(self, target_class, query_filter):
        result_list = self.session.query(target_class).filter(query_filter).all()
        self.session.close()
        return result_list


class Heros(Base):
    &quot;&quot;&quot;定义表结构&quot;&quot;&quot;
    __tablename__ = &#39;heros&#39;
    id = Column(INT(), primary_key=True)
    name = Column(VARCHAR(255))
    hp_max = Column(FLOAT())
    mp_max = Column(FLOAT())

    def __init__(self, id, name, hp_max, mp_max):
        self.id = id
        self.name = name
        self.hp_max = hp_max
        self.mp_max = mp_max


if __name__ == &#39;__main__&#39;:
    db_obj = Test_db()
    query_filter = and_(Heros.hp_max &gt; 6000)
    heros = db_obj.query_all(Heros, query_filter)
    for hero_info in heros:
        print(&quot;id:{}, name:{}, hp_max:{}, mp_max:{}&quot;.format(hero_info.id, hero_info.name,
                                                            hero_info.hp_max, hero_info.mp_max))
```
id:10000, name:夏侯惇, hp_max:7350.0, mp_max:1746.0
id:10046, name:钟馗, hp_max:6280.0, mp_max:1988.0
id:10048, name:鬼谷子, hp_max:7107.0, mp_max:1808.0
id:10051, name:赵云, hp_max:6732.0, mp_max:1760.0
id:10052, name:橘石京, hp_max:7000.0, mp_max:0.0
id:10055, name:杨戬, hp_max:7420.0, mp_max:1694.0
id:10056, name:达摩, hp_max:7140.0, mp_max:1694.0
id:10057, name:孙悟空, hp_max:6585.0, mp_max:1760.0
id:10058, name:刘备, hp_max:6900.0, mp_max:1742.0
.....执行结果有点多字数限制了
Process finished with exit code 0</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（6） 💬（1）<div># -*- coding: UTF-8 -*-
import mysql.connector
import traceback

# 打开数据库连接
db = mysql.connector.connect(
    host=&quot;localhost&quot;,
    user=&quot;root&quot;,
    passwd=&quot;123456&quot;,  # 写上你的数据库密码
    database=&#39;nba&#39;,
    auth_plugin=&#39;mysql_native_password&#39;
)

# 获取操作游标
cursor = db.cursor()

try:

    # 查询heros 表中最大生命值大于 6000 的英雄进行查询，并且输出相应的属性值。
    sql = &#39;SELECT name, hp_max FROM heros WHERE hp_max &gt; %s ORDER BY hp_max DESC&#39;
    val = (6000,)
    cursor.execute(sql, val)
    data = cursor.fetchall()
    for each_player in data:
        print(each_player)
except Exception as e:
  # 打印异常信息
  traceback.print_exc()
  # 回滚
  db.rollback()
finally:
  # 关闭游标 &amp; 数据库连接
  cursor.close()
  db.close()

输出：

(&#39;廉颇&#39;, 9328.0)
(&#39;白起&#39;, 8638.0)
(&#39;程咬金&#39;, 8611.0)
(&#39;刘禅&#39;, 8581.0)
(&#39;牛魔&#39;, 8476.0)
(&#39;张飞&#39;, 8341.0)
(&#39;庄周&#39;, 8149.0)
(&#39;刘邦&#39;, 8073.0)
(&#39;项羽&#39;, 8057.0)
(&#39;亚瑟&#39;, 8050.0)
(&#39;东皇太一&#39;, 7669.0)
(&#39;典韦&#39;, 7516.0)
(&#39;曹操&#39;, 7473.0)
(&#39;杨戬&#39;, 7420.0)
(&#39;夏侯惇&#39;, 7350.0)
(&#39;吕布&#39;, 7344.0)
(&#39;哪吒&#39;, 7268.0)
(&#39;墨子&#39;, 7176.0)
(&#39;老夫子&#39;, 7155.0)
(&#39;达摩&#39;, 7140.0)
(&#39;鬼谷子&#39;, 7107.0)
(&#39;关羽&#39;, 7107.0)
(&#39;钟无艳&#39;, 7000.0)
(&#39;橘石京&#39;, 7000.0)
(&#39;刘备&#39;, 6900.0)
(&#39;太乙真人&#39;, 6835.0)
(&#39;孙膑&#39;, 6811.0)
(&#39;赵云&#39;, 6732.0)
(&#39;扁鹊&#39;, 6703.0)
(&#39;铠&#39;, 6700.0)
(&#39;露娜&#39;, 6612.0)
(&#39;孙悟空&#39;, 6585.0)
(&#39;钟馗&#39;, 6280.0)
(&#39;雅典娜&#39;, 6264.0)
(&#39;兰陵王&#39;, 6232.0)
(&#39;宫本武藏&#39;, 6210.0)
(&#39;娜可露露&#39;, 6205.0)
(&#39;高渐离&#39;, 6165.0)
(&#39;芈月&#39;, 6164.0)
(&#39;不知火舞&#39;, 6014.0)
(&#39;孙尚香&#39;, 6014.0)

Process finished with exit code 0</div>2019-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3hZfficKPGCq2kjFBu9SgaMjibJTEl7iaW1ta6pZNyiaWP8XEsNpunlnsiaOtBpWTXfT5BvRP3qNByml6p9rtBvqewg/132" width="30px"><span>夜路破晓</span> 👍（5） 💬（2）<div>auth_plugin=&#39;mysql_native_password&#39;
哪位亲给解释下这个参数</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/c7/ec18673b.jpg" width="30px"><span>大斌</span> 👍（4） 💬（3）<div>核心代码：
cursor = db.cursor()

sql = &quot;select name,hp_max from heros where hp_max &gt; %s&quot;
val = (6000,)
cursor.execute(sql,val)
data = cursor.fetchall()
注意：val里面的元素后面必须要加英文逗号，不加或者中文逗号都会报错</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/f0/a73607b3.jpg" width="30px"><span>victor666</span> 👍（2） 💬（1）<div>Python直接写SQL比Java方便多了</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（2） 💬（3）<div>当一些听着很虚的理论用于实战时，其威力是巨大的，例如信息的正交性。</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（1） 💬（1）<div>import pymysql
import pymysql.cursors


cfg = {
    &quot;host&quot;: &quot;127.0.0.1&quot;,
    &quot;user&quot;: &quot;root&quot;,
    &quot;passwd&quot;: &quot;toor&quot;,
    &quot;database&quot;: &quot;test&quot;,
    &quot;charset&quot;: &quot;utf8mb4&quot;,
    &quot;autocommit&quot;: True,
    &#39;cursorclass&#39;:pymysql.cursors.DictCursor
}

db_con = pymysql.connect(**cfg)

try:
    with db_con.cursor() as cur:
        cur.execute(&quot;SELECT id,name,hp_max FROM heros WHERE hp_max &gt; 6000 &quot;)
        res = cur.fetchall()

    for i in res:
        print(i)
finally:
    db_con.close()

</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a7/f0/e3212f18.jpg" width="30px"><span>胡</span> 👍（0） 💬（1）<div>__author__ = &#39;Administrator&#39;

# -*- coding: UTF-8 -*-
import traceback
import json
import mysql.connector
# 打开数据库连接
db = mysql.connector.connect(
       host=&quot;localhost&quot;,
       user=&quot;root&quot;,
       passwd=&quot;hjf@2019&quot;, # 写上你的数据库密码
       database=&#39;nba&#39;,
       auth_plugin=&#39;mysql_native_password&#39;
)
# 获取操作游标
cursor = db.cursor()
# 执行 SQL 语句
#cursor.execute(&quot;SELECT VERSION()&quot;)
# 获取一条数据
#data = cursor.fetchone()
#print(&quot;MySQL 版本: %s &quot; % data)
# 关闭游标 &amp; 数据库连接



# 插入新球员

sql = &quot;INSERT INTO player (team_id,player_id,player_name,height) VALUES (%s, %s, %s,%s)&quot;
val = (1003, 10038,&quot; 约翰 - 科林斯 &quot;, 2.08)
cursor.execute(sql,val)
db.commit()
print(cursor.rowcount, &quot; 记录插入成功。&quot;)

cursor.close()
db.close()</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a7/f0/e3212f18.jpg" width="30px"><span>胡</span> 👍（0） 💬（1）<div>老师在插入数据的时候，漏掉了 player_id ?</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8c/2a/49e0547d.jpg" width="30px"><span>发条</span> 👍（0） 💬（1）<div>使用8.0以上版本mysql的同学，在连接数据库的时候可能会受到quth_plugin不支持mysql_native_password的报错，
可以用ALTER USER &#39;root&#39;@&#39;localhost&#39; IDENTIFIED WITH mysql_native_password BY &#39;root&#39;;语句把auth_plugin改掉</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（0） 💬（1）<div># -*- coding: UTF-8 -*-

import mysql.connector
# 打开数据库连接
db = mysql.connector.connect(
       host=&quot;localhost&quot;,
       user=&quot;root&quot;,
       passwd=&quot;root&quot;, # 写上你的数据库密码
       database=&#39;test&#39;, 
       auth_plugin=&#39;mysql_native_password&#39;
)
# 获取操作游标 
cursor = db.cursor()
sql = &#39;SELECT * FROM heros WHERE hp_max&gt;=6000&#39;
cursor.execute(sql)
data = cursor.fetchall()
for each_hero in data:
  print(each_hero)
cursor.close()
db.close()</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（0） 💬（1）<div>python print语句出来的中文是乱码要怎么处理？python程序第一行加过 # -*- coding: UTF-8 -*-
(10003, u&#39;\u5b89\u5fb7\u70c8-\u5fb7\u62c9\u8499\u5fb7&#39;, 2.11)</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/02/2864e0f2.jpg" width="30px"><span>华夏</span> 👍（0） 💬（1）<div>pip install mysql-connector之后连接数据库会报错，更新到最新版还是一样报错，pip install mysql-connector-python之后可以正常运行。大家如果有遇到这个问题的可以参考@林彦-广州-数据分析师 这个办法。</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/d9/4feb4006.jpg" width="30px"><span>lmingzhi</span> 👍（0） 💬（1）<div>老师，你好，我一般使用SQLAlchemy连接数据库:
from sqlalchemy import create_engine
db = create_engine(&#39;mysql:&#47;&#47;root@localhost&#47;test_database&#39;)
一般如你在文中提到的话如果使用结束后，不想再浪费资源，需要执行什么操作？</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（0） 💬（1）<div>执行结果:


(&#39;夏侯&#39;, 7350.0)
(&#39;钟无艳&#39;, 7000.0)
(&#39;张飞&#39;, 8341.0)
(&#39;牛魔&#39;, 8476.0)
(&#39;吕布&#39;, 7344.0)
(&#39;亚瑟&#39;, 8050.0)
(&#39;芈月&#39;, 6164.0)
(&#39;程咬金&#39;, 8611.0)
(&#39;廉颇&#39;, 9328.0)
(&#39;东皇太一&#39;, 7669.0)
(&#39;庄周&#39;, 8149.0)
(&#39;太乙真人&#39;, 6835.0)
(&#39;白起&#39;, 8638.0)
(&#39;雅典娜&#39;, 6264.0)
(&#39;刘邦&#39;, 8073.0)
(&#39;刘禅&#39;, 8581.0)
(&#39;墨子&#39;, 7176.0)
(&#39;项羽&#39;, 8057.0)
(&#39;关羽&#39;, 7107.0)
(&#39;孙尚香&#39;, 6014.0)
(&#39;露娜&#39;, 6612.0)
(&#39;不知火舞&#39;, 6014.0)
(&#39;孙膑&#39;, 6811.0)
(&#39;高渐离&#39;, 6165.0)
(&#39;扁鹊&#39;, 6703.0)
(&#39;钟馗&#39;, 6280.0)
(&#39;鬼谷子&#39;, 7107.0)
(&#39;赵云&#39;, 6732.0)
(&#39;橘石京&#39;, 7000.0)
(&#39;杨戬&#39;, 7420.0)
(&#39;达摩&#39;, 7140.0)
(&#39;孙悟空&#39;, 6585.0)
(&#39;刘备&#39;, 6900.0)
(&#39;曹操&#39;, 7473.0)
(&#39;典韦&#39;, 7516.0)
(&#39;宫本武藏&#39;, 6210.0)
(&#39;老夫子&#39;, 7155.0)
(&#39;哪吒&#39;, 7268.0)
(&#39;娜可露露&#39;, 6205.0)
(&#39;兰陵王&#39;, 6232.0)
(&#39;铠&#39;, 6700.0)</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（0） 💬（1）<div>练习答案:


# -*- coding: UTF-8 -*-
import mysql.connector

db = mysql.connector.connect(
       host=&quot;localhost&quot;,
       user=&quot;root&quot;,
       passwd=&quot;123456&quot;, 
       database=&#39;geektime-sql&#39;, 
       auth_plugin=&#39;mysql_native_password&#39;
)

cursor = db.cursor()
try:
  sql = &#39;SELECT  name,hp_max from heros where hp_max&gt;6000;&#39;
  cursor.execute(sql)
  data = cursor.fetchall()
  for each_player in data:
    print(each_player)
finally:
  cursor.close()
  db.close()</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/3d/7f5c1b37.jpg" width="30px"><span>谷径</span> 👍（0） 💬（1）<div>auth_plugin=&#39;mysql_native_password&#39; 这句报错，是什么意思呢？</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/02/2864e0f2.jpg" width="30px"><span>华夏</span> 👍（0） 💬（1）<div>(&#39;夏侯惇&#39;, 7350.0, 1746.0, 321.0, 397.0)
(&#39;钟无艳&#39;, 7000.0, 1760.0, 318.0, 409.0)
(&#39;张飞&#39;, 8341.0, 100.0, 301.0, 504.0)
(&#39;牛魔&#39;, 8476.0, 1926.0, 273.0, 394.0)
(&#39;吕布&#39;, 7344.0, 0.0, 343.0, 390.0)
(&#39;亚瑟&#39;, 8050.0, 0.0, 346.0, 400.0)
(&#39;芈月&#39;, 6164.0, 100.0, 289.0, 361.0)
(&#39;程咬金&#39;, 8611.0, 0.0, 316.0, 504.0)
(&#39;廉颇&#39;, 9328.0, 1708.0, 286.0, 514.0)
(&#39;东皇太一&#39;, 7669.0, 1926.0, 286.0, 360.0)
(&#39;庄周&#39;, 8149.0, 1694.0, 297.0, 497.0)
(&#39;太乙真人&#39;, 6835.0, 1680.0, 284.0, 396.0)
(&#39;白起&#39;, 8638.0, 1666.0, 288.0, 430.0)
(&#39;雅典娜&#39;, 6264.0, 1732.0, 327.0, 418.0)
(&#39;刘邦&#39;, 8073.0, 1940.0, 302.0, 504.0)
(&#39;刘禅&#39;, 8581.0, 1694.0, 295.0, 459.0)
(&#39;墨子&#39;, 7176.0, 1722.0, 328.0, 475.0)
(&#39;项羽&#39;, 8057.0, 1694.0, 306.0, 494.0)
(&#39;关羽&#39;, 7107.0, 10.0, 343.0, 386.0)
(&#39;孙尚香&#39;, 6014.0, 1756.0, 411.0, 346.0)
(&#39;露娜&#39;, 6612.0, 1836.0, 335.0, 375.0)
(&#39;不知火舞&#39;, 6014.0, 200.0, 293.0, 336.0)
(&#39;孙膑&#39;, 6811.0, 1926.0, 328.0, 413.0)
(&#39;高渐离&#39;, 6165.0, 1988.0, 290.0, 343.0)
(&#39;扁鹊&#39;, 6703.0, 2016.0, 309.0, 374.0)
(&#39;钟馗&#39;, 6280.0, 1988.0, 278.0, 390.0)
(&#39;鬼谷子&#39;, 7107.0, 1808.0, 297.0, 394.0)
(&#39;赵云&#39;, 6732.0, 1760.0, 380.0, 394.0)
(&#39;橘石京&#39;, 7000.0, 0.0, 347.0, 392.0)
(&#39;杨戬&#39;, 7420.0, 1694.0, 325.0, 428.0)
(&#39;达摩&#39;, 7140.0, 1694.0, 355.0, 415.0)
(&#39;孙悟空&#39;, 6585.0, 1760.0, 349.0, 385.0)
(&#39;刘备&#39;, 6900.0, 1742.0, 363.0, 381.0)
(&#39;曹操&#39;, 7473.0, 0.0, 361.0, 371.0)
(&#39;典韦&#39;, 7516.0, 1774.0, 345.0, 402.0)
(&#39;宫本武藏&#39;, 6210.0, 0.0, 330.0, 391.0)
(&#39;老夫子&#39;, 7155.0, 5.0, 329.0, 409.0)
(&#39;哪吒&#39;, 7268.0, 1808.0, 320.0, 408.0)
(&#39;娜可露露&#39;, 6205.0, 1808.0, 385.0, 359.0)
(&#39;兰陵王&#39;, 6232.0, 1822.0, 388.0, 342.0)
(&#39;铠&#39;, 6700.0, 1784.0, 328.0, 388.0)
41  查询成功。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（2）<div>老师你好，我觉得这一节讲得有点太浅了。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fc/90/c9df0459.jpg" width="30px"><span>ack</span> 👍（0） 💬（1）<div># -*- coding: UTF-8 -*-
import mysql.connector

# 打开数据库连接
db = mysql.connector.connect(
    host=&quot;localhost&quot;,
    user=&quot;user&quot;,
    passwd=&quot;12345&quot;,
    database=&#39;test&#39;,
    auth_plugin=&#39;mysql_native_password&#39;
)
# 获取操作游标
cursor = db.cursor()
# 执行 SQL 语句
cursor.execute(&quot;SELECT * FROM heros WHERE hp_max&gt;6000&quot;)
attr = cursor.description
attrNum = len(attr)
for i in range(attrNum):
    print attr[i][0],
print  &quot;\n&quot;
# 获取数据
data = cursor.fetchall()
for row in data:
    for col in row:
        print col,
    print &quot;\n&quot;
# 关闭游标 &amp; 数据库连接
cursor.close()
db.close()</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（4） 💬（4）<div>sql = &#39;DELETE FROM player WHERE name = %s&#39;
val = (&quot; 约翰 - 科林斯 &quot;)
cursor.execute(sql)
db.commit()
print(cursor.rowcount, &quot; 记录删除成功。&quot;)
这里写错了哇，这样写才不会报错：
sql = &#39;DELETE FROM player WHERE player_name = %s&#39;
val = (&quot; 约翰 - 科林斯 &quot;, )
cursor.execute(sql, val)
db.commit()
print(cursor.rowcount, &quot; 记录删除成功。&quot;)

</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/a7/5e66d331.jpg" width="30px"><span>林彦</span> 👍（2） 💬（0）<div>try...except...那部分代码没有关闭游标的语句。关闭数据库连接的语句执行时一般都会先隐式关闭并释放当前的游标吗？</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（0）<div>看目录，我以为到 SQL刷题了。。。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/74/9e/31872e2c.jpg" width="30px"><span>bahao</span> 👍（1） 💬（0）<div>看来要补习python了 执行sql太方便了</div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/c7/ec18673b.jpg" width="30px"><span>大斌</span> 👍（1） 💬（0）<div>python连接mysql时报错【mysql.connector.errors.NotSupportedError: Authentication plugin &#39;caching_sha2_password&#39; is not support】。
原因是：mysql8.0.11使用了Use Strong Password Encryption for Authentication即强密码加密。
通常的处理方法是：重装mysql【装更低版本的或者将Use Strong Password Encryption for Authentication改为Use Legacy Authentication Method(在Authentication Method中改)】
还有一种更好的方案，那就是使用【pymysql】库来连接，代码如下：
    db_host = &quot;localhost&quot;
    db_username = &quot;root&quot;
    db_password = &quot;123456&quot;
    db_name = &quot;database_name&quot;
    conn = pymysql.connect(
        host=db_host,
        user=db_username,
        passwd=db_password,
        database=db_name,
    )</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（1） 💬（0）<div>sql = &#39;DELETE FROM player WHERE player_name = &quot; 约翰-科林斯 &quot;&#39;</div>2019-07-19</li><br/><li><img src="" width="30px"><span>极客酱</span> 👍（1） 💬（0）<div>删除约翰·科林斯这个球员的数据代码里面，excute那个函数缺少了val的参数吧？</div>2019-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLIuRQaZX70dsBg6khub2VPM1eQAP9IWRWxgOFed3ia4kXyNJInFRicWJ0ibf2YmLsOvJa1sGygGpmJg/132" width="30px"><span>胖子</span> 👍（0） 💬（0）<div>与上一遍提到的游标有何不同？</div>2024-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>比JAVA简单多了，后面善后，可以试试</div>2024-08-21</li><br/>
</ul>