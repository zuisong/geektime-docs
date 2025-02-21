上节课，我介绍了Python DB API规范的作用，以及如何使用MySQL官方的mysql-connector驱动来完成数据库的连接和使用。在项目比较小的时候，我们可以直接使用SQL语句，通过mysql-connector完成与MySQL的交互，但是任何事物都有两面性，随着项目规模的增加，代码会越来越复杂，维护的成本也越来越高，这时mysql-connector就不够用了，我们需要更好的设计模式。

Python还有另一种方式可以与MySQL进行交互，这种方式采用的是ORM框架。我们今天就来讲解如何使用ORM框架操作MySQL，那么今天的课程你需要掌握以下几个方面的内容：

1. 什么是ORM框架，以及为什么要使用ORM框架？
2. Python中的ORM框架都有哪些？
3. 如何使用SQLAlchemy来完成与MySQL的交互？

## 我们为什么要使用ORM框架？

在讲解ORM框架之前，我们需要先了解什么是持久化。如下图所示，持久化层在业务逻辑层和数据库层起到了衔接的作用，它可以将内存中的数据模型转化为存储模型，或者将存储模型转化为内存中的数据模型。

![](https://static001.geekbang.org/resource/image/b9/5b/b9dafd636ec586704bb8488d9b2faa5b.jpg?wh=655%2A506)

你可能会想到，我们在讲事务的4大特性ACID时，提到过持久性。你可以简单地理解为，持久性就是将对象数据永久存储在数据库中。通常我们将数据库的作用理解为永久存储，将内存理解为暂时存储。我们在程序的层面操作数据，其实都是把数据放到内存中进行处理，如果需要数据就会通过持久化层，从数据库中取数据；如果需要保存数据，就是将对象数据通过持久化层存储到数据库中。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/90/4e/efaea936.jpg" width="30px"><span>墨禾</span> 👍（34） 💬（1）<div>以下从ORM的作用，是什么，优缺点以及一些比较流行的ORM的对比的个人总结：

1.ORM的作用
对象关系映射，能够直接将数据库对象进行持久化。

在没有ORM前，我们要自己写数据库连接方法，自己在方法里面嵌入原生的sql语句去访问数据表……

这时问题就来了：
数据库名，数据表名完全暴露在代码中，有脱库的风险；
需要我们自己处理数据表对象，比如说把数据表中取出的数据转化为标准json等，sql语句安全过滤，数据表、字段别名、兼容多种数据库等一系列的数据处理工作；

下面介绍一下ORM到底是啥？

2、ORM是什么？
ORM作为数据库层与业务逻辑层之间的一个抽象，能够将业务逻辑的处理持久化为内存对象，交由数据库去处理。其封装了数据库的连接，数据表的操作细节……在文中我们可以看到ORM将sql语句做了封装，我们可以通过filter实现过滤，而不是写where子句。

ORM真的那么好？

3、优缺点
优点：
安全：因为屏蔽了数据库的具体操作细节以及对sql做了严格的过滤，因此能够保证数据库信息的隐蔽性，同时防止sql注入。
简单：屏蔽了数据层的访问细节，我们只需要集中注意力处理业务逻辑就可以了。

缺点：
性能低：自动化意味着加载很多即使没有必要的关联和映射，牺牲性能。但ORM也采取了一些补救措施：对象懒加载，缓存技术等。

学习成本高：面向对象的封装设计，是的我们必须要去了解对象的处理细节。

难以实现复杂查询：ORM实现的是一些通用的数据处理方法，一些负责的业务处理还是需要自己组装sql。

那么还有哪些比较流行的ORM呢？
hibernate:强调对单条数据的处理
mybits:基于自定义配置的sql操作</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（21） 💬（3）<div>缺少一些代码，可以参考廖雪峰的这个。
https:&#47;&#47;www.liaoxuefeng.com&#47;wiki&#47;1016959663602400&#47;1017803857459008</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/45/b88a1794.jpg" width="30px"><span>一叶知秋</span> 👍（12） 💬（1）<div>日常交作业~~~

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
            &#39;mysql+pymysql:&#47;&#47;UserName:Password@host:port&#47;Db_Name?charset=utf8&#39;)
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def update(self, target_class, query_filter, target_obj):
        &quot;&quot;&quot;
        更新操作通用方法
        :param target_class: 表对象
        :param query_filter: 查询条件
        :param target_obj: 更新目标对象
        :return:
        &quot;&quot;&quot;
        try:
            self.session.query(target_class).filter(query_filter).update(target_obj)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e)


class Player(Base):
    &quot;&quot;&quot;定义表结构&quot;&quot;&quot;
    __tablename__ = &#39;player&#39;
    player_id = Column(INT(), primary_key=True)
    team_id = Column(INT())
    player_name = Column(VARCHAR(255))
    height = Column(FLOAT())

    def __init__(self, player_id, team_id, player_name, height):
        self.player_id = player_id
        self.team_id = team_id
        self.player_name = player_name
        self.height = height


if __name__ == &#39;__main__&#39;:
    db_obj = Test_db()
    query_filter = and_(Player.height == 2.08)
    target_obj = {&#39;height&#39;: 2.09}
    update_result = db_obj.update(Player, query_filter, target_obj)

后续更新数量、更新结果等等判断就略过了...
（小声bb：什么时候极客时间评论也能支持markdown啊。。）</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（9） 💬（1）<div>翻了一下SQLAlchemy的官方文档,看到一个简单的办法,作业如下:

&#39;&#39;&#39;

作业:

使用SQLAlchemy工具查询身高为2.08米的球员,并且将这些球员的身高修改为2.09;


参考:
		
		https:&#47;&#47;docs.sqlalchemy.org&#47;en&#47;13&#47;core&#47;dml.html


&#39;&#39;&#39;

from sqlalchemy import Column, String, Integer, Float,create_engine,update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine(&#39;mysql+mysqlconnector:&#47;&#47;root:123456@localhost:3306&#47;geektime-sql&#39;)


class Player(Base):
    __tablename__ = &#39;player&#39;
 
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    player_name = Column(String(255))
    height = Column(Float(3,2))

def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}

if __name__ == &#39;__main__&#39;:
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	Base.to_dict = to_dict
	print(&quot;更新前:&quot;)
	rows = session.query(Player).filter(Player.height == 2.08).all()
	print([row.to_dict() for row in rows])
	# 参考: https:&#47;&#47;docs.sqlalchemy.org&#47;en&#47;13&#47;core&#47;dml.html#sqlalchemy.sql.expression.update
	stmt = update(Player).where(Player.height == 2.08).values(height=2.09)
	engine.execute(stmt)
	session.commit()
	rows = session.query(Player).filter(Player.height == 2.09).all()
	print(&quot;更新后:&quot;)
	print([row.to_dict() for row in rows])
	session.close()
太长,省略了部分执行结果.自己执行一下,就可以看到完整结果了..

更新前:
[{&#39;player_id&#39;: 10010, &#39;team_id&#39;: 1001, &#39;player_name&#39;: &#39;乔恩-洛伊尔&#39;, &#39;height&#39;: Decimal(&#39;2.0800000000&#39;)}......
更新后:
[{&#39;player_id&#39;: 10010, &#39;team_id&#39;: 1001, &#39;player_name&#39;: &#39;乔恩-洛伊尔&#39;, &#39;height&#39;: Decimal(&#39;2.0900000000&#39;)}......
[Finished in 0.9s]</div>2019-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3hZfficKPGCq2kjFBu9SgaMjibJTEl7iaW1ta6pZNyiaWP8XEsNpunlnsiaOtBpWTXfT5BvRP3qNByml6p9rtBvqewg/132" width="30px"><span>夜路破晓</span> 👍（8） 💬（1）<div>框架对实体的映射不难理解,数据库本身就是对现实世界的映射,借由映射将事实转换为数据.
代码部分有些基础的也不难理解;基础较弱硬钢的亲们,耐心一条条来缕也可以捋顺,都是基础的东西,无非花费时间长短问题.有几个坑这里记录下,供后来人借鉴:
1.关于初始化连接数据库问题.creat_engine的参数这块容易卡壳,可以参考以下文字说明:
create_engine(&quot;数据库类型+数据库驱动:&#47;&#47;数据库用户名:数据库密码@IP地址:端口&#47;数据库&quot;，其他参数)
2.数据库驱动这块,老师的参考代码是用mysqlconnector,沿承得是上篇中导入mysql-connector包;网上一些资料以及参考其他同学的答案有使用pymysql,要用这个需安装pip install pymysql.这两货对于本篇的学习内容在本质上是一样的,任选一个即可.
3.在代码复写过程中,删除操作一直报错.网上查了资料说是跟返回值有关.经过测试,发现问题所在,filter返回结果为None.也就是说没有查询到&quot;约翰-科林斯&quot;.往回倒腾,发现开始新增数据那里,增加的&quot; 约翰-科林斯 &quot;,前后对比后者两侧多了个空格.统一前后,删除操作顺利完成.</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（5） 💬（1）<div>错误解决：
如果报如下错误：Authentication plugin &#39;caching_sha2_password&#39; is not supported
sqlalchemy.exc.NotSupportedError: (mysql.connector.errors.NotSupportedError) Authentication plugin &#39;caching_sha2_password&#39; is not supported (Background on this error at: http:&#47;&#47;sqlalche.me&#47;e&#47;tw8g)
可以参考下面的链接处理：
https:&#47;&#47;stackoverflow.com&#47;questions&#47;51783313&#47;how-do-i-get-sqlalchemy-create-engine-with-mysqlconnector-to-connect-using-mysql</div>2019-07-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（3） 💬（1）<div>老师，我的表中有个时间字段，我想在插入数据时，自动生成时间应怎么设置该字段，是这样吗：
`create_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT &#39;创建时间&#39;,</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（2） 💬（1）<div>from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(&quot;mysql+pymysql:&#47;&#47;root:toor@localhost:3306&#47;test&quot;)

Session = sessionmaker(bind=engine)


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Base.to_dict = to_dict


class Player(Base):
    __tablename__ = &quot;player&quot;

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    player_name = Column(String(255))
    height = Column(Float(3, 2))


session = Session()

rows = session.query(Player).filter(Player.height == 2.08).all()
for row in rows:
    print(row.to_dict())
    row.height = 2.09
session.commit()


# 验证
rows = session.query(Player).filter(Player.height == 2.09).all()
print([row.to_dict() for row in rows])

session.close()


</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/51/c616f95a.jpg" width="30px"><span>阿锋</span> 👍（2） 💬（1）<div>上面那个分组查询，按照分组后数据行数递增的顺序进行排序，怎么结果是[(1001, 20), (1002, 17)]，那不是递减？是不是写错了？</div>2019-07-22</li><br/><li><img src="" width="30px"><span>Geek_5d805b</span> 👍（1） 💬（2）<div>to_dict方法这块看不太懂，base类指的是player类吗，谁给讲讲</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/7c/8ef14715.jpg" width="30px"><span>NIXUS</span> 👍（1） 💬（1）<div>ORM的使用，更多的不都是通过查文档的吗？</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（1） 💬（1）<div>老师好，对于修改数据的事例有一点困惑还请您解答。对于下面这段代码中

row = session.query(Player).filter(Player.player_name==&#39;索恩 - 马克&#39;).first()
row.height = 2.17
session.commit()
session.close()

我理解row是存在于内存中的对象，但是我们在修改后并没有传递到数据库中，如果直接commit可以进行修改的话，这个row是在哪里存放的对象呢？</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/96/78/eb86673c.jpg" width="30px"><span>我在你的视线里</span> 👍（0） 💬（1）<div>session对象是django自带的。还是在项目里创建的。</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/21/cf/f47e092d.jpg" width="30px"><span>咕咕咕</span> 👍（7） 💬（0）<div>代码能不能给完整啊？还说全部跑一遍？不给全给个提示或者文档链接也行吧？还是得看评论的同学补充才知道代码没有给全。</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/f5/fd386689.jpg" width="30px"><span>Venom</span> 👍（5） 💬（0）<div>老师，建议最后能把完整代码给出来。对于我们没用过的人来讲，缺少一条import语句也很苦恼啊</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/dc/ce/03fdeb60.jpg" width="30px"><span>白色纯度</span> 👍（3） 💬（0）<div>我自己总结的博客链接：https:&#47;&#47;blog.csdn.net&#47;weixin_42564710&#47;article&#47;details&#47;103978476 
完整版的代码如下：
# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

# 创建对象的基类:
Base = declarative_base()
# 定义 Player 对象:
class Player(Base):
    # 表的名字:
    __tablename__ = &#39;player&#39;

    # 表的结构:
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    player_name = Column(String(255))
    height = Column(Float(3, 2))
    # 增加 to_dict() 方法到 Base 类中
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    # 将对象可以转化为 dict 类型
    Base.to_dict = to_dict
if __name__==&#39;__main__&#39;:
    engine = create_engine(&#39;mysql+mysqlconnector:&#47;&#47;root:密码@localhost:3306&#47;world&#39;)
    # 创建 DBSession 类型:
    DBSession = sessionmaker(bind=engine)
    # 创建 session 对象:
    session = DBSession()

    # 创建 Player 对象:
    new_player = Player(team_id=1101, player_name=&quot; 约翰 - 雪诺 &quot;, height=2.08)
    # 添加到 session:
    session.add(new_player)
    # 提交即保存到数据库:
    session.commit()
    session.close()
    # 查询身高 &gt;=2.08 的球员有哪些
    rows_1 = session.query(Player).filter(Player.height &gt;= 2.08).all()
    print([row.to_dict() for row in rows_1])

    rows_2 = session.query(Player).filter(or_(Player.height &gt;=2.08, Player.height &lt;=2.10)).all()
    print([row.to_dict() for row in rows_2])
    rows_3 = session.query(Player.team_id, func.count(Player.player_id)).group_by(Player.team_id).having(func.count(Player.player_id)&gt;5).order_by(func.count(Player.player_id).asc()).all()
    print(rows_3)


    row = session.query(Player).filter(Player.player_name==&#39;索恩-马克&#39;).first()
    row.height = 2.19
    session.commit()
    # 关闭 session:
    session.close()

    row = session.query(Player).filter(Player.player_name == &#39; 约翰 - 雪诺 &#39;).first()
    session.delete(ro</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（3） 💬（0）<div>文章中的示例代码.完整可运行.

from sqlalchemy import Column, String, Integer, Float,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
# 初始化数据库连接，修改为你的数据库用户名和密码
engine = create_engine(&#39;mysql+mysqlconnector:&#47;&#47;root:123456@localhost:3306&#47;geektime-sql&#39;)

# 定义 Player 对象:
class Player(Base):
    # 表的名字:
    __tablename__ = &#39;player&#39;
 
    # 表的结构:
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    player_name = Column(String(255))
    height = Column(Float(3,2))


# 增加 to_dict() 方法到 Base 类中
def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}



if __name__ == &#39;__main__&#39;:
	# 创建 DBSession 类型:
	DBSession = sessionmaker(bind=engine)
	# 创建 session 对象:
	session = DBSession()

	# 创建 Player 对象:
	new_player = Player(team_id = 1003, player_name = &quot;约翰 - 科林斯&quot;, height = 2.08)
	# 添加到 session:
	session.add(new_player)
	# 提交即保存到数据库:
	session.commit()
	# 关闭 session:
	session.close()
	# 将对象可以转化为 dict 类型
	Base.to_dict = to_dict
	# 查询身高 &gt;=2.08 的球员有哪些
	# rows = session.query(Player).filter(Player.height &gt;=2.08, Player.height &lt;=2.10).all()
	# from sqlalchemy import or_
	# rows = session.query(Player).filter(or_(Player.height &gt;=2.08, Player.height &lt;=2.10)).all()
	rows = session.query(Player).filter(Player.height &gt;= 2.08).all()
	print([row.to_dict() for row in rows])
	from sqlalchemy import func
	rows = session.query(Player.team_id, func.count(Player.player_id)).group_by(Player.team_id).having(func.count(Player.player_id)&gt;5).order_by(func.count(Player.player_id).asc()).all()
	print(rows)
	row = session.query(Player).filter(Player.player_name==&#39;约翰 - 科林斯&#39;).first()
	session.delete(row)
	session.commit()
	session.close()
	row = session.query(Player).filter(Player.player_name==&#39;索恩-马克&#39;).first()
	row.height = 2.17
	session.commit()
	session.close()


</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（3） 💬（3）<div>老师你好，能否多讲一些ORM框架的缺点，以及为什么互联网项目大多不用ORM的原因？</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（2） 💬（0）<div>rows = session.query(Player).filter(Player.height==2.08).all()
for row in rows:
    row.height = 2.09
session.commit()
session.close()</div>2019-07-22</li><br/><li><img src="" width="30px"><span>Geek_5d805b</span> 👍（1） 💬（0）<div>问一下，我们已经创建过了player表，能说一下对于已有的数据库表，怎么直接将存储模型转换为数据模型吗，而不是再按字段新建</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（1） 💬（0）<div>另外,SQLAlchemy和MyBatis有点像，唯一不同的是MyBatis可以把SQL语句写在XML文件里面(当然也可以写在Java方法上)，SQLAlchemy好像只能用字符串方式(在官网暂时没找到其它方式的示例)来写SQL语句.</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/34/a7/52c4ea60.jpg" width="30px"><span>年少挽滑稽世无双</span> 👍（0） 💬（0）<div>from sphinxcontrib.websupport.storage.sqlalchemy_db import Base
from sqlalchemy import create_engine, or_, func
from sqlalchemy.orm import sessionmaker
from orm.orm1 import Player

# 初始化数据库连接，修改为你的数据库用户名和密码
engine = create_engine(&#39;mysql+mysqlconnector:&#47;&#47;root:password@localhost:3308&#47;nba?auth_plugin=mysql_native_password&#39;)


# 增加to_dict()方法到Base类中
def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}


# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

# 将对象可以转化为dict类型
Base.to_dict = to_dict

# 查询身高为 2.08 米的球员，并且将这些球员的身高修改为 2.09。
rows = session.query(Player).filter(Player.height == 2.08).all()
print(&quot;更新前：&quot;)
print([row.to_dict() for row in rows])
rows = session.query(Player).filter(Player.height == 2.08).update({&quot;height&quot;: &quot;2.09&quot;})
session.commit()
rows2 = session.query(Player).filter(Player.height == 2.09).all()
print(&quot;更新后：&quot;)
print([row2.to_dict() for row2 in rows2])

# 关闭session:
session.close()
</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/e5/f1/880994da.jpg" width="30px"><span>忧伤的胡萝卜</span> 👍（0） 💬（0）<div>有个地方没太明白。rows这个对象为什么会有to_dict()这个方法？</div>2021-06-30</li><br/><li><img src="" width="30px"><span>Geek_2caf97</span> 👍（0） 💬（0）<div>我想的是flink sql这种能算一种orm么，因为他也对业务逻辑封装了，也可以持久化</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2c/4f/be77ceac.jpg" width="30px"><span>H</span> 👍（0） 💬（0）<div>sqlalchemy.exc.InvalidRequestError: SQL expression, column, or mapped entity expected - got &#39;&lt;class &#39;__main__.ones_project&#39;&gt;&#39;
</div>2021-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/0a/81/69fecff9.jpg" width="30px"><span>xiaopi3</span> 👍（0） 💬（0）<div># -*- coding: utf-8 -*-
&quot;&quot;&quot;
Created on Thu Sep  3 20:14:33 2020

@author: PP
&quot;&quot;&quot;

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(&#39;mysql+mysqlconnector:&#47;&#47;root:123456@localhost:3306&#47;ooo&#39;)
Base = declarative_base()

#增加to_dict()方法到Base类中
def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}
#将对象可以转化为dict类型
Base.to_dict = to_dict


class Player(Base):
    __tablename__=&#39;player&#39;
    
    player_id=Column(Integer,primary_key=True)
    player_name=Column(String(255))
    height=Column(Float(3,2))
    
DBSession=sessionmaker(bind=engine)
session=DBSession()

rows=session.query(Player).filter(Player.height==2.08).all()
print(&quot;更新前&quot;)
print([row.to_dict() for row in rows])

rows=session.query(Player).filter(Player.height==2.08).update({&quot;height&quot;:&quot;2.09&quot;})
session.commit()

rows=session.query(Player).filter(Player.height==2.09).all()
print(&quot;更新后&quot;)
print([row.to_dict() for row in rows])</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（0） 💬（0）<div>老师您好：

pip install sqlalchemy
初始化数据库连接
from sqlalchemy import create_engine
# 初始化数据库连接，修改为你的数据库用户名和密码
engine = create_engine(&#39;mysql+mysqlconnector:&#47;&#47;root:password@localhost:3306&#47;wucai&#39;)
这里的代码都是传入的明文的用户名和密码，有什么方法传入密文的用户名和密码吗？</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ac/24/0684a141.jpg" width="30px"><span>彭纪程</span> 👍（0） 💬（0）<div>from sqlalchemy import create_engine
# 初始化数据库连接，修改为你的数据库用户名和密码
engine = create_engine(&#39;mysql+mysqlconnector:&#47;&#47;root:Xlkfems123@localhost:3306&#47;nba&#39;)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float
Base = declarative_base()
class Player(Base):
    # 表的名字:
    __tablename__ = &#39;player&#39;
 
    # 表的结构:
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    player_name = Column(String(255))
    height = Column(Float(3,2))
def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}
#将对象可以转化为dict类型
Base.to_dict = to_dict
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
rows= session.query(Player).filter(Player.height == 2.08).all()
for each in rows:
    each.height = 2.09
session.commit()
results = session.query(Player).order_by(Player.height.desc()).all()

print([row.to_dict() for row in results])
session.close()</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/a6/4e331ef4.jpg" width="30px"><span>骑行的掌柜J</span> 👍（0） 💬（0）<div>陈老师 ，你在增加数据库数据哪里是不是少导入了两个类和一行定义Base的代码？
from sqlalchemy.ext.declarative import declarative_base
#引用基本映射类
from sqlalchemy.orm import sessionmaker
#引用session类操作后面的增删改查

Base = declarative_base()
#建立基本映射类，方便后面真正的映射类Player来继承它</div>2019-09-09</li><br/>
</ul>