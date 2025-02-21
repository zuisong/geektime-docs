SQL可以帮我们进行数据处理，总的来说可以分成OLTP和OLAP两种方式。

OLTP称之为联机事务处理，我们之前讲解的对数据进行增删改查，SQL查询优化，事务处理等就属于OLTP的范畴。它对实时性要求高，需要将用户的数据有效地存储到数据库中，同时有时候针对互联网应用的需求，我们还需要设置数据库的主从架构保证数据库的高并发和高可用性。

OLAP称之为联机分析处理，它是对已经存储在数据库中的数据进行分析，帮我们得出报表，指导业务。它对数据的实时性要求不高，但数据量往往很大，存储在数据库（数据仓库）中的数据可能还存在数据质量的问题，比如数据重复、数据中有缺失值，或者单位不统一等，因此在进行数据分析之前，首要任务就是对收集的数据进行清洗，从而保证数据质量。

对于数据分析工作来说，好的数据质量才是至关重要的，它决定了后期数据分析和挖掘的结果上限。数据挖掘模型选择得再好，也只能最大化地将数据特征挖掘出来。

高质量的数据清洗，才有高质量的数据。今天我们就来看下，如何用SQL对数据进行清洗。

1. 想要进行数据清洗有怎样的准则呢？
2. 如何使用SQL对数据进行清洗？
3. 如何对清洗之后的数据进行可视化？

## 数据清洗的准则

我在《数据分析实战45讲》里专门讲到过数据清洗的原则，这里为了方便你理解，我用一个数据集实例讲一遍。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（13） 💬（1）<div># Mac只能用Python了
import pandas as pd
import matplotlib.pyplot as plt

# 读入清洗好的数据
df = pd.read_csv(&#39;.&#47;titanic_train.csv&#39;)

# 数据透视表用到的数据 df_temp
df_temp = df[[&#39;Embarked&#39;, &#39;Survived&#39;]]

# 生成数据透视表
## 方法1 
table = pd.pivot_table(df_temp, index=[&#39;Embarked&#39;], columns=[&#39;Survived&#39;], aggfunc=len)
table = pd.pivot_table(df_temp, index=[&#39;Embarked&#39;], columns=[&#39;Survived&#39;], aggfunc=len)
## 方法2 数据交叉表
table = pd.crosstab(df.Embarked, df.Survived)

# 画图
table.plot(kind=&#39;bar&#39;)
plt.show()

----------------分割线 上面是code------------------
talbe
# 输出结果
Survived	0	1
Embarked		
C	75	93
Q	47	30
S	427	219
</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/a6/4e331ef4.jpg" width="30px"><span>骑行的掌柜J</span> 👍（10） 💬（3）<div>陈老师 我对这一节的操作全部用MySQL进行了一个实操 中间遇到一些问题 我也全部做了一个整理补充 放到了我的博客里面：https:&#47;&#47;blog.csdn.net&#47;weixin_41013322&#47;article&#47;details&#47;103616783  希望对后面学习的朋友有帮助 谢谢</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（4） 💬（1）<div>WPS同样可以使用,这种方式很方便.所需下载的文件我放到网盘了，地址: 链接: https:&#47;&#47;pan.baidu.com&#47;s&#47;1Wrq7VcypQiofKp70YaQLBA 提取码: 2avt

看了这一课，忽然想去买数据分析的课学习一下.</div>2019-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（3） 💬（1）<div>仅对某一列缺失值处理
时序数据：线性插值
频谱数据：重采样
……</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/b2/3d3d8e05.jpg" width="30px"><span>哈66</span> 👍（2） 💬（1）<div>老是想问一下收集过来的数据为什么需要清洗啊，能具体举一些使用场景嘛？</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/f5/fd386689.jpg" width="30px"><span>Venom</span> 👍（2） 💬（2）<div>找不到数据集的人，这里能下，我也是刚找到。https:&#47;&#47;download.csdn.net&#47;download&#47;qq_44851287&#47;11142360</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/b6/17103195.jpg" width="30px"><span>Elliot</span> 👍（2） 💬（2）<div>https:&#47;&#47;www.kaggle.com&#47;c&#47;titanic&#47;data 这个属于github的吗？</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（2） 💬（1）<div>我的Python代码github地址
https:&#47;&#47;github.com&#47;LearningChanging&#47;sql_must_konw&#47;tree&#47;master&#47;45-%E6%95%B0%E6%8D%AE%E6%B8%85%E6%B4%97%EF%BC%9A%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8SQL%E5%AF%B9%E6%95%B0%E6%8D%AE%E8%BF%9B%E8%A1%8C%E6%B8%85%E6%B4%97%EF%BC%9F</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e6/68/1871d6ba.jpg" width="30px"><span>海洋</span> 👍（6） 💬（0）<div>检查全面性修改字段类型时，直接使用Navicat的设计表格功能修改，更快，只不过不利于新手锻炼SQL代码能力，同时可视化这块，一般清洗后，直接导出，然后使用Python或者BI软件进行进一步分析可视化</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（2） 💬（0）<div>可以用 LOAD DATA 导入，但是要注意，在默认的严格模式下，如果设置 age 列为 numeric 的类型，将会报错无法读取，原因是空字符段无法读取。
即使调整为非严格模式读取成功，Age 和 cabin 空的部分，本来该是NULL，但是在SQL读取后，分别是 0 和 空字符串，并非NULL。
先创建表格：
CREATE TABLE titanic_train(
	passenger_id INT(3) PRIMARY KEY,
	survived INT(1),
	pcalss INT(1),
	name VARCHAR(255),
	sex VARCHAR(6),
	age DECIMAL(4,2),
	sibsp INT(1),
	parch INT(1),
	ticket VARCHAR(20),
	fare DECIMAL(7,4),
	cabin VARCHAR(5),
	embarked CHAR(1)
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
再导入数据：
LOAD DATA INFILE &#39;文件位置&#47;train.csv&#39; 
  INTO TABLE titanic_train
  FIELDS TERMINATED BY &#39;,&#39; OPTIONALLY ENCLOSED BY &#39;&quot;&#39; ESCAPED BY &#39;&quot;&#39;
  LINES TERMINATED BY &#39;\n&#39;
  IGNORE 1 LINES
  (passenger_id, survived, pcalss, name, sex, @age, sibsp, parch, ticket, fare, @cabin, embarked)
  SET age = NULLIF(@age,&#39;&#39;), cabin = NULLIF(@cabin,&#39;&#39;);</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（1） 💬（0）<div>mport pandas as pd
import matplotlib.pyplot as plt

# Python导入数据
titanic_train1 = pd.read_csv(&#39;train.csv&#39;)
# 大致看下数据，注意到空值可以正常读取为NaN，如果直接用MySQL客户端中LOAD DATA，会出现很多问题
titanic_train1.head(8)

# 完整性
titanic_train1.isnull().sum()

# 简单查看数据
titanic_train1.describe()

# Age 列均值填充
titanic_train1.Age.fillna(titanic_train1.Age.mean(), inplace = True)

# Cabin 列的不重复取值有多少个
titanic_train1.Cabin.nunique()
# Cabin 列一共有多少个非空取值
titanic_train1.Cabin.count()
# 上述两步只用一步就可以得出
titanic_train1.Cabin.describe()
# 只有三种取值
titanic_train1.Embarked.describe()
# 统计离散的登录港口变量，每个港口的个数统计
titanic_train1.Embarked.value_counts()
# 采用高频方式填充控制
titanic_train1.Embarked.fillna(&#39;S&#39;, inplace = True)

# MySQL导入清洗好的数据

# -*- coding: UTF-8 -*-
import mysql.connector
# 打开数据库连接
db = mysql.connector.connect(
       host=&quot;localhost&quot;,
       user=&quot;root&quot;,
       passwd=&quot;***********&quot;, # 写上你的数据库密码
       database=&#39;XXX, 
       auth_plugin=&#39;mysql_native_password&#39;
)
# 获取操作游标 
cursor = db.cursor()
# 执行SQL语句
cursor.execute(&quot;SELECT GROUP_CONCAT(column_name SEPARATOR &#39;, &#39;) FROM information_schema.COLUMNS WHERE table_name = &#39;titanic_train&#39;&quot;)
# 获取一条数据：列名
data = cursor.fetchone()
print(&quot;列名: %s &quot; % data)

cursor.execute(&quot;SELECT * FROM titanic_train&quot;)
# 获取一条数据
data = cursor.fetchall()
titanic_train2 = pd.DataFrame(data, 
                              columns = [&quot;passenger_id&quot;, &quot;Survived&quot;, &quot;pcalss&quot;, &quot;name&quot;, &quot;sex&quot;, &quot;Age&quot;, &quot;Sibsp&quot;, &quot;parch&quot;, &quot;ticket&quot;, &quot;Fare&quot;, &quot;cabin&quot;, &quot;embarked&quot; ])

# 数据可视化

# 数据透视表
table = pd.crosstab(titanic_train1.Embarked, titanic_train1.Survived)
print(table)

# 用得到的数据透视表作数据透视图
table.plot(kind=&#39;bar&#39;, ylabel = &#39;Frequency&#39;)
plt.show()

# 法二直接画图
import seaborn as sns
ax = sns.countplot(x=&quot;Embarked&quot;, hue=&quot;Survived&quot;, data=titanic_train1)</div>2021-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（1） 💬（0）<div>LOAD DATA 导入数据 （二）
下面就来解决这个问题：
很容易想到方法一，但是觉得在数据量很大的时候，方法一还要在扫一遍表，而方法二只需要在读取扫描的时候，顺带加一个判断就行了，觉得这样的话，方法一消耗了一些不必要的资源。

**方法一**：导入数据后进行修改（利用 UPDATE）

**方法二**：读取数据时进行判断
参考：【解决Mysql导入csv中空值变为0的问题：导入数据时设定格式】
https:&#47;&#47;blog.csdn.net&#47;duckyamd&#47;article&#47;details&#47;53143639

先获得所有列名，用逗号 &#39;,&#39; 分隔，这样方便我们之后写“读取数据时进行判断”的 LOAD DATA 的代码：

SELECT GROUP_CONCAT(column_name SEPARATOR &#39;, &#39;) FROM information_schema.COLUMNS WHERE table_name = &#39;titanic_train&#39;;
+---------------------------------------------------------------------------------------------+
| GROUP_CONCAT(column_name SEPARATOR &#39;, &#39;)                                                    |
+---------------------------------------------------------------------------------------------+
| passenger_id, survived, pcalss, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked |
+---------------------------------------------------------------------------------------------+
1 row in set (0.02 sec)
参考：GROUP_CONCAT 的官方文档说明：https:&#47;&#47;dev.mysql.com&#47;doc&#47;refman&#47;8.0&#47;en&#47;aggregate-functions.html#function_group-concat

passenger_id, survived, pcalss, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked

# 删除表格数据
DELETE FROM titanic_train

-- 加载数据的时候进行判断
LOAD DATA INFILE &#39;C:&#47;Users&#47;ASUS&#47;Documents&#47;Python Scripts&#47;sql&#47;train_ansi.csv&#39;
  INTO TABLE titanic_train
  FIELDS TERMINATED BY &#39;,&#39; OPTIONALLY ENCLOSED BY &#39;&quot;&#39; ESCAPED BY &#39;&quot;&#39;
  LINES TERMINATED BY &#39;\n&#39;
  IGNORE 1 LINES
  (passenger_id, survived, pcalss, name, sex, @age, sibsp, parch, ticket, fare, @cabin, embarked)
  SET age = NULLIF(@age,&#39;&#39;), cabin = NULLIF(@cabin,&#39;&#39;);
Query OK, 891 rows affected (0.05 sec)
Records: 891  Deleted: 0  Skipped: 0  Warnings: 0
可以看到相应空字符的位置是 null 而不是 0 了
NULLIF 的文档：意思就是如果这个变量是空字符就设置为null
https:&#47;&#47;dev.mysql.com&#47;doc&#47;refman&#47;8.0&#47;en&#47;flow-control-functions.html#function_nullif</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（1） 💬（0）<div>LOAD DATA 导入数据（没有Navicat）（一）：
CREATE TABLE titanic_train(
	passenger_id INT(3) PRIMARY KEY,
	survived INT(1),
	pcalss INT(1),
	name VARCHAR(255),
	sex VARCHAR(6),
	age DECIMAL(4,2),
	sibsp INT(1),
	parch INT(1),
	ticket VARCHAR(20),
	fare DECIMAL(7,4),
	cabin VARCHAR(5),
	embarked CHAR(1)
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

ALTER TABLE titanic_train MODIFY name VARCHAR(255);
ALTER TABLE titanic_train MODIFY sex VARCHAR(6);
ALTER TABLE titanic_train MODIFY age INT(2) DEFAULT NULL;
ALTER TABLE titanic_train MODIFY fare DECIMAL(7,4);
ALTER TABLE titanic_train MODIFY cabin VARCHAR(255);

SET SESSION sql_mode = &#39;&#39;; -- 严格模式下会报错：Incorrect integer value: &#39;&#39; for column &#39;出错的column&#39; at row 出错的行数
-- 这里将session 的 sql_mode 置为空，就不是严格模式了
-- 另外 这里Setting the SESSION variable affects only the current client. Each client can change its session sql_mode value at any time. 
-- 参考：SQL mode  网址：https:&#47;&#47;dev.mysql.com&#47;doc&#47;refman&#47;8.0&#47;en&#47;sql-mode.html#sqlmode_strict_trans_tables

LOAD DATA INFILE &#39;C:&#47;Users&#47;ASUS&#47;Documents&#47;Python Scripts&#47;sql&#47;train_ansi.csv&#39; 
  INTO TABLE titanic_train
  FIELDS TERMINATED BY &#39;,&#39; OPTIONALLY ENCLOSED BY &#39;&quot;&#39; ESCAPED BY &#39;&quot;&#39;
  LINES TERMINATED BY &#39;\n&#39;
  IGNORE 1 LINES;

SHOW warnings;
-- 在非严格模式下，很多严格模式下的错误会退化为 warnings，此时一定要查看 warnings，发现需要改正的问题。理论上讲，除了要忽略的问题（比如这里空字符无法导入int类型）之外，没有其他问题的时候，用严格模式来忽略这些问题；但是通常我们可能还有其它应该避免、不应该忽略的问题，最好查看一下非严格模式下的warnings.

-- 官方文档和很多资料里，都是 LINES TERMINATED BY &#39;\r\n&#39;，但是我只有用 \n 才能插入成功
-- 发现空字符串不能被正常读取为（数据库中的）NULL，cabin就算了（空字符和NULL的区别可能影响不大），但是age空字符串在非严格模式下（在严格模式下根本无法导入数据，会报错：Incorrect integer value: &#39;&#39; for column &#39;出错的column&#39; at row 出错的行数），空字符导入后就变成了0，但是那些乘客显然不是零岁啊（我的数据里面出错的是 Age 一列）
【mysql 导入csv空值_如何处理csv中的空值】https:&#47;&#47;blog.csdn.net&#47;weixin_29969209&#47;article&#47;details&#47;114795753 这篇文章也提到了这个问题，主要讲了讲可能会带来那些衍生的问题，并且讨论了Python和 mysql 数据交互时，空字符串读取的情况，但是并没有解决问题。
</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/85/2e/92c506ce.jpg" width="30px"><span>ClaireToffler</span> 👍（1） 💬（0）<div>LTP 称之为联机事务处理，我们之前讲解的对数据进行增删改查，SQL 查询优化，事务处理等就属于 OLTP 的范畴。它对实时性要求高，需要将用户的数据有效地存储到数据库中，同时有时候针对互联网应用的需求，我们还需要设置数据库的主从架构保证数据库的高并发和高可用性。 忽然感觉平时好像只接触了这个领域</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/25/70634e86.jpg" width="30px"><span>阿飛</span> 👍（1） 💬（0）<div>有没有oracle for excel
</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/d1/5e/2b7e685a.jpg" width="30px"><span>Wry</span> 👍（0） 💬（0）<div>老师，看了这个我对sum和count的使用有些懵，多个字段查询是否有null值的情况的时候为什么这里SELECT 
SUM((CASE WHEN Age IS NULL THEN 1 ELSE 0 END)) AS age_null_num, 
SUM((CASE WHEN Cabin IS NULL THEN 1 ELSE 0 END)) AS cabin_null_num
FROM titanic_train使用sum而不用count呢？如果不用存储过程还有其他方法可以查多个字段null值情况吗？</div>2021-11-12</li><br/>
</ul>