上一章中，我们讲了Python的一个重要的第三方库NumPy，今天我来给你介绍Python的另一个工具Pandas。

在数据分析工作中，Pandas的使用频率是很高的，一方面是因为Pandas提供的基础数据结构DataFrame与json的契合度很高，转换起来就很方便。另一方面，如果我们日常的数据清理工作不是很复杂的话，你通常用几句Pandas代码就可以对数据进行规整。

Pandas可以说是基于 NumPy 构建的含有更高级数据结构和分析能力的工具包。在NumPy中数据结构是围绕ndarray展开的，那么在Pandas中的核心数据结构是什么呢？

下面主要给你讲下**Series和 DataFrame这两个核心数据结构**，他们分别代表着一维的序列和二维的表结构。基于这两种数据结构，Pandas可以对数据进行导入、清洗、处理、统计和输出。

## 数据结构：Series和DataFrame

**Series是个定长的字典序列**。说是定长是因为在存储的时候，相当于两个ndarray，这也是和字典结构最大的不同。因为在字典的结构里，元素的个数是不固定的。

**Series**有两个基本属性：index 和 values。在Series结构中，index默认是0,1,2,……递增的整数序列，当然我们也可以自己来指定索引，比如index=\[‘a’, ‘b’, ‘c’, ‘d’]。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/af/a9/e24380a0.jpg" width="30px"><span>何楚</span> 👍（88） 💬（6）<div>#!&#47;usr&#47;bin&#47;env python3
# -*- coding: utf-8 -*-

import pandas as pd

data = {&#39;Chinese&#39;: [66, 95, 93, 90, 80, 80], &#39;English&#39;: [65, 85, 92, 88, 90, 90],
        &#39;Math&#39;: [None, 98, 96, 77, 90, 90]}
df = pd.DataFrame(data, index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;],
                  columns=[&#39;English&#39;, &#39;Math&#39;, &#39;Chinese&#39;])
# 去除重复行
df = df.drop_duplicates()
# 列名重新排序
cols = [&#39;Chinese&#39;, &#39;English&#39;, &#39;Math&#39;]
df = df.filter(cols, axis=1)
# 列名改为中文
df.rename(columns={&#39;Chinese&#39;: &#39;语文&#39;, &#39;English&#39;: &#39;英语&#39;,
                   &#39;Math&#39;: &#39;数学&#39;}, inplace=True)


def total_score(df):
    df[&#39;总分&#39;] = df[&#39;语文&#39;] + df[&#39;英语&#39;] + df[&#39;数学&#39;]
    return df


# 求成绩的和，用老师讲的 apply 方法
df = df.apply(total_score, axis=1)
# 或者可以用这个方法求和
# df[&#39;总分&#39;] = df[&#39;语文&#39;] + df[&#39;英语&#39;] + df[&#39;数学&#39;]
# 按照总分排序，从高到低，此时有缺失值
df.sort_values([&#39;总分&#39;], ascending=[False], inplace=True)
# 打印显示成绩单信息，张飞有空值
print(df.isnull().sum())
print(df.describe())
print(df)

# 使用数学成绩均值填充张飞同学的缺失值
df[&#39;数学&#39;].fillna(df[&#39;数学&#39;].mean(), inplace=True)
# 再次求成绩的和并打印显示成绩单情况
df = df.apply(total_score, axis=1)
print(df.isnull().sum())
print(df.describe())
print(df)
</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6f/20/53cb569d.jpg" width="30px"><span>daydreamer</span> 👍（21） 💬（2）<div>&quot;&quot;&quot;
Pandas中有Series和DataFrame两种重要的数据结构。
    Series：是一个定长的字典序列。有两个基本属性：index，values
    DataFrame：类似于数据库表的一种数据结构。我们甚至可以像操作数据库表那样对DataFrame数据进行
    连接，合并，查询等等
    常用DataFrame进行数据清晰：用到的发方法有:
        去重删除：drop()，drop_duplicates(),rename()
        去空格：strip(),lstrip(),rstrip()
        变换大小写：upper(),lower(),title()
        改变数据格式：astype()
        查找空值：lsnull
        apply


&quot;&quot;&quot;
from pandas import DataFrame

# Scores of students
scores = {&#39;Chinese&#39;: [66, 95, 95, 90, 80, 80],
          &#39;English&#39;: [65, 85, 92, 80, 90, 90],
          &#39;Math&#39;: [None, 98, 96, 77, 90, 90],
          &#39;Total&#39;: [None, None, None, None, None, None]}
df = DataFrame(scores, index=[&#39;Zhang Fei&#39;, &#39;Guan Yu&#39;, &#39;Zhao Yun&#39;, &#39;Huang Zhong&#39;, &#39;Dian Wei&#39;,&#39;Dian Wei&#39;],)

# Data ckeaning.
# remove the duplicated record.
df = df.drop_duplicates()
# print(df)

# Calculate the total scores.
df[&#39;Total&#39;] = df.sum(axis=1)
print(df.describe())</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/61/a8/a0b4d4d2.jpg" width="30px"><span>知悉者也</span> 👍（7） 💬（2）<div>stu_score = pd.DataFrame([[&#39;张飞&#39;, 66, 65, np.nan],
                         [&#39;关羽&#39;, 95, 85, 98],
                         [&#39;赵云&#39;, 95, 92, 96],
                         [&#39;黄忠&#39;, 90, 88, 77],
                         [&#39;典韦&#39;, 80, 90, 90],
                         [&#39;典韦&#39;, 80, 90, 90]],
                        columns = [&#39;姓名&#39;,&#39;语文&#39;, &#39;英语&#39;, &#39;数学&#39;])
stu_score = stu_score.set_index(&#39;姓名&#39;)  # 将某一列作为索引

stu_score = stu_score.fillna(axis=1, method=&#39;ffill&#39;)  # 以左边来填充缺失值
stu_score[&#39;总分&#39;] = stu_score.apply(sum , axis=1)
stu_score</div>2019-11-07</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIc88LLmwU7RU1tGcmo5OZyPibKeXPg31wMxyc2uByEO3g44f6uLcu1bXGNO9AHVgn0PK5hwkcfYZA/132" width="30px"><span>董大琳儿</span> 👍（6） 💬（1）<div>都没听懂，感到淡淡的忧伤~~~</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2b/69/7aace61c.jpg" width="30px"><span>Answer Liu</span> 👍（5） 💬（1）<div>df6 = pd.DataFrame(
    {&quot;语文&quot;: [66, 95, 95, 90, 80, 80], &quot;数学&quot;: [65, 85, 92, 88, 90, 90], &quot;英语&quot;: [np.nan, 98, 96, 77, 90, 90]},
    index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;]
)
# 去重
df7 = df6.drop_duplicates()
# 替换NaN值
df8 = df7.fillna(df7[&#39;英语&#39;].mean())
# 增加一行统计
df8[&#39;sum&#39;] = [df8.loc[name].sum() for name in df8.index]
# 按总分倒序排列
df9 = df8.sort_values(by=&quot;sum&quot;, ascending=False)
print(df9)</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/d0/49b06424.jpg" width="30px"><span>qinggeouye</span> 👍（4） 💬（2）<div>import numpy as np
import pandas as pd

scores = pd.DataFrame(
    {&#39;姓名&#39;: [&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;], &#39;语文&#39;: [66, 95, 95, 90, 80, 80], &#39;英语&#39;: [65, 85, 92, 88, 90, 90],
     &#39;数学&#39;: [np.NaN, 98, 96, 77, 90, 90], })

print(scores)

# 查找空值所在的列
isNaN = scores.isna().any()  # isnull(), isnull().any()
isNaN = isNaN[isNaN == True]
print(scores[isNaN.index])

# 列的平均值填充空值
for col in isNaN.index:
    scores[col].fillna(scores[col].mean(), inplace=True)
print(scores)

# 去除不必要的行（空值）
# scores = scores.drop(index=[0])
# scores = scores.dropna()

# 去除重复行
scores = scores.drop_duplicates()
print(scores)

# 新增一列&#39;总和&#39;
# scores[&#39;总和&#39;] = scores[&#39;语文&#39;] + scores[&#39;数学&#39;] + scores[&#39;英语&#39;]
scores[&#39;总和&#39;] = scores.sum(axis=1)
print(scores)
</div>2019-11-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLricLSQB9ABYhZnndOoX0jItAiaficX3XicbvND1RodB3y62GCwxRvgAfoZggOyRFyHqwqnicicJKvQJ9g/132" width="30px"><span>龟仙人</span> 👍（4） 💬（3）<div>老师你好，你好像没有在哪里明确说明自己的环境是python2.7的，结果大家的使用环境大多数是3.0的，多多少少会引发一些问题。还有请问，微信群怎么加？</div>2019-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a9/32/eb71b457.jpg" width="30px"><span>Grandia_Z</span> 👍（3） 💬（1）<div>照着老师写 df2 = df2.drop(columns=[&#39;Chinese&#39;]) 这行代码后,返回结果是:
TypeError                                 Traceback (most recent call last)
&lt;ipython-input-25-8116650c61ac&gt; in &lt;module&gt;()
----&gt; 1 df2 = df2.drop(columns=[&#39;Chinese&#39;])

TypeError: drop() got an unexpected keyword argument &#39;columns&#39;

这个什么意思
</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/ba/3b30dcde.jpg" width="30px"><span>窝窝头</span> 👍（2） 💬（1）<div>import pandas as pd
data = {&#39;语文&#39;: [66, 95, 93, 90, 80, 80], &#39;英语&#39;: [65, 85, 92, 88, 90, 90],
        &#39;数学&#39;: [None, 98, 96, 77, 90, 90]}
df = pd.DataFrame(data, index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;],
                  columns=[u&#39;英语&#39;, u&#39;数学&#39;, u&#39;语文&#39;])
df=df.dropna()
df = df.drop_duplicates()
df[u&#39;总和&#39;] = df[u&#39;语文&#39;]+df[u&#39;英语&#39;]+df[u&#39;数学&#39;]
df.head()
</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/2b/3ab96998.jpg" width="30px"><span>青石</span> 👍（2） 💬（1）<div>from pandas import DataFrame


def score(df):
    df[&#39;score&#39;] = df[u&#39;Chinese&#39;] + df[u&#39;English&#39;] + df[u&#39;Math&#39;]
    return df

data = {&#39;Chinese&#39;: [66, 95, 95, 90, 80, 80], &#39;English&#39;: [65, 85, 92, 88, 90, 90], &#39;Math&#39;: [None, 98, 96, 77, 90, 90]}
df = DataFrame(data, index=[&#39;ZhangFei&#39;, &#39;GuanYu&#39;, &#39;ZhaoYun&#39;, &#39;HuangZhong&#39;, &#39;DianWei&#39;, &#39;DianWei&#39;], columns=[&#39;Chinese&#39;, &#39;English&#39;, &#39;Math&#39;])
df = df.drop_duplicates().fillna(0)
df = df.apply(score, axis=1)

print(df)</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1f/d0/660502a4.jpg" width="30px"><span>初</span> 👍（2） 💬（1）<div>None竟然是浮点型数据....没想到</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a5/99/db2f6325.jpg" width="30px"><span>lingmacker</span> 👍（2） 💬（1）<div>def exercise():
    # 1. 对于下表的数据，请使用Pandas中的DataFrame进行创建，并对数据进行清洗。
    # 2. 同时新增一列“总和”计算每个人的三科成绩之和。

    # 列名使用了中文，打印需要列对其的话，则需要设置这两个参数
    pd.set_option(&#39;display.unicode.ambiguous_as_wide&#39;, True)
    pd.set_option(&#39;display.unicode.east_asian_width&#39;, True)

    data = {&quot;姓名&quot;: [&quot;张飞&quot;, &quot;关羽&quot;, &quot;赵云&quot;, &quot;黄忠&quot;, &quot;典韦&quot;, &quot;典韦&quot;],
            &quot;语文&quot;: [66, 95, 95, 90, 80, 80],
            &quot;英语&quot;: [65, 85, 92, 88, 90, 90],
            &quot;数学&quot;: [None, 98, 96, 77, 90, 90]}
    
    score_table = pd.DataFrame(data, columns=[&quot;姓名&quot;, &quot;语文&quot;, &quot;英语&quot;, &quot;数学&quot;])
    print(score_table, &quot;\n&quot;)

    # 除去重复行
    score_table.drop_duplicates(inplace=True)
    print(score_table, &quot;\n&quot;)

    # 添加 总分 列
    score_table.fillna(0, inplace=True)  # 将NaN替换为0
    score_table[&quot;总分&quot;] = score_table[&quot;语文&quot;] + score_table[&quot;英语&quot;] + score_table[&quot;数学&quot;]
    print(score_table)</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/28/9c/73e76b19.jpg" width="30px"><span>姜戈</span> 👍（2） 💬（1）<div># -*- coding: utf-8 -*-
import pandas as pd
from pandas import Series, DataFrame

data={&#39;语文&#39;:[66, 95, 95, 90, 80, 80],&#39;英语&#39;:[65, 85, 92, 88, 90,90], &#39;数学&#39;:[&#39;&#39;, 98, 96, 77, 90, 90]}
df1 = DataFrame(data, index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;,&#39;刘备&#39;,&#39;典韦&#39;,&#39;典韦&#39;], columns=[&#39;语文&#39;,&#39;英语&#39;,&#39;数学&#39;])
print df1
df1 = df1.drop_duplicates()
print df1

df = df1.replace(to_replace=&#39;&#39;, value=0)

print df

df[&#39;总计&#39;]=df[&#39;语文&#39;]+df[&#39;英语&#39;]+df[&#39;数学&#39;]
df.replace(to_replace=0, value=&#39;&#39;, inplace=True)
print df</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（2） 💬（1）<div>#!&#47;usr&#47;bin&#47;python
# vim: set fileencoding:utf-8
&#39;&#39;&#39;
1.对于下表的数据，请使用Pandas中的DataFrame进行创建，并对数据进行清洗。
2.同时新增一列“总和”计算每个人的三科成绩之和。
&#39;&#39;&#39;
import pandas as pd
from pandas import DataFrame

# 导入成绩
data = pd.read_excel(u&#39;成绩表.xlsx&#39;)
df = DataFrame(data)
print df


# 求和，并增加一列“总和”
def addtotal(df):
    df[u&#39;总和&#39;] = df[u&#39;语文&#39;] + df[u&#39;英语&#39;] + df[u&#39;数学&#39;]
    return df


# 清洗为空的数据
df1 = df.dropna()

# 清洗重复的数据
df1 = df1.drop_duplicates()

# 生成新数据结构
df1= df1.apply(addtotal, axis=1)
print(df1)</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a9/93/3acddf29.jpg" width="30px"><span>郭 冲</span> 👍（1） 💬（1）<div>#!&#47;usr&#47;bin&#47;env python3
# -*- coding: utf-8 -*-

import pandas as pd

data = {&#39;语文&#39;: [66, 95, 95, 90, 80, 80],
        &#39;英语&#39;: [65, 85, 92, 88, 90, 90],
        &#39;数学&#39;: [None, 98, 96, 77, 90, 90]}

df_hw = DataFrame(data, 
                  index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;], 
                  columns=[&#39;语文&#39;, &#39;英语&#39;, &#39;数学&#39;])

# 1.去除重复的值
df_hw = df_hw.drop_duplicates()

# 2.查找空值
df_hw.isnull()

# 3. 使用数学成绩均值填充张飞同学的缺失值
df_hw[&#39;数学&#39;].fillna(df_hw[&#39;数学&#39;].mean(), inplace=True)

# 4.使用apply函数增加“总和”列
def sum_together(df):
    df[&#39;总和&#39;] = df[&#39;语文&#39;] + df[&#39;英语&#39;] + df[&#39;数学&#39;]
    return df

df_hw = df_hw.apply(sum_together,axis=1)

df_hw</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/40/50/a960f038.jpg" width="30px"><span>Ric</span> 👍（1） 💬（1）<div>Pandas加sql，威力無窮</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ba/6d318c08.jpg" width="30px"><span>GS</span> 👍（1） 💬（1）<div>https:&#47;&#47;github.com&#47;leledada&#47;jupyter&#47;blob&#47;master&#47;PandasTest.ipynb   用Jupter写了一遍。

pandasql  为什么要 import load_meat, load_births ？ 做什么用的？这个我要查一查</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8d/d0/34e6a27d.jpg" width="30px"><span>Dull</span> 👍（1） 💬（1）<div>使用Pyhon3.7+Pycharm编写，最后使用sort_value.()方法对总成绩进行降序排序。
# -*- coding: utf-8 -*-
import pandas as pd
from pandas import Series, DataFrame
data = {&#39;Chinese&#39;: [66, 95, 95, 90,80,80],&#39;English&#39;: [65, 85, 92, 88, 90,90],&#39;Math&#39;: [None, 98, 96, 77, 90,90]}
df = DataFrame(data,index=[&#39;张飞&#39;,&#39;关羽&#39;,&#39;赵云&#39;,&#39;黄忠&#39;,&#39;典韦&#39;,&#39;典韦&#39;],columns=[&#39;Chinese&#39;,&#39;English&#39;,&#39;Math&#39;])
print(df)
df = df.drop_duplicates()
df.rename(columns = {&#39;Chinese&#39;:&#39;语文&#39;,&#39;English&#39;:&#39;英语&#39;,&#39;Math&#39;:&#39;数学&#39;}, inplace = True)
df[&#39;数学&#39;].fillna(df[&#39;数学&#39;].mean(),inplace=True)  #df.fillna(df.mean())好像也可以
def new(df):
	df[&#39;总分&#39;] = (df[&#39;语文&#39;]+df[&#39;数学&#39;]+df[&#39;英语&#39;])
	return df
df = df.apply(new,axis=1)
print(df)
df1 = df.sort_values(by=[&#39;总分&#39;],ascending=False)
print(df1)</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/fe/83/b2e833ff.jpg" width="30px"><span>笨鸟的GPS</span> 👍（0） 💬（1）<div># 创建dataframe
import pandas as pd
from pandas import Series,DataFrame
data = {&#39;chinese&#39;:[66,95,95,90,80,80],&#39;english&#39;:[65,85,92,88,90,90],&#39;math&#39;:[&#39;&#39;,98,96,77,90,90]}
df2 = DataFrame(data,index=[&#39;zhangfei&#39;,&#39;guanyu&#39;,&#39;zhaoyun&#39;,&#39;huangzhong&#39;,&#39;dianwei&#39;,&#39;dianwei&#39;],columns=[&#39;chinese&#39;,&#39;english&#39;,&#39;math&#39;])
# 去重
df2 = df2.drop_duplicates()
# 填充缺失值
df2.loc[&#39;zhangfei&#39;,&#39;math&#39;] = 30
# 新增总和
df2[&#39;total&#39;] = df2[&#39;chinese&#39;] +df2[&#39;english&#39;] + df2[&#39;math&#39;]</div>2021-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a9/cb/a431bde5.jpg" width="30px"><span>木头发芽</span> 👍（0） 💬（1）<div>一通百通,这节的DataFrame跟Spark的DataFrame的各种操作几乎一样,虽然底层实现原理有差别,但用法是一样的. 所以说要做T型人才,当一个方向钻的够深,就能触类旁通.</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/da/58/2c36d211.jpg" width="30px"><span>NLPer</span> 👍（0） 💬（1）<div>老师，我准备做个笔记分享给更多的人😁</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/da/9d/1f825568.jpg" width="30px"><span>拾光</span> 👍（0） 💬（1）<div>import pandas as pd

# 创建DataFrame，列名是：&#39;name&#39;、&#39;gender&#39;、&#39;age&#39;
df = pd.DataFrame([[&#39;Snow&#39;,83,97],
                   [&#39;Tyrion&#39;,78,82,92],
                   [&#39;Sansa&#39;,76,88,98],
                   [&#39;Arya&#39;,95,78,64]], columns=[&#39;姓名&#39;,&#39;语文&#39;,&#39;英语&#39;, &#39;数学&#39;],index=None)

# 清洗数据
df.dropna(axis=0, how=&#39;any&#39;, inplace=True)

df[&#39;总分&#39;] = df[&#39;语文&#39;] + df[&#39;英语&#39;] + df[&#39;数学&#39;]
print(df)</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/87/50/fd4b6d5d.jpg" width="30px"><span>包家欢</span> 👍（0） 💬（1）<div>data1 = {&#39;语文&#39;:[&#39;66&#39;,&#39;95&#39;,&#39;95&#39;,&#39;90&#39;,&#39;80&#39;,&#39;80&#39;],&#39;英语&#39;:[&#39;65&#39;,&#39;85&#39;,&#39;92&#39;,&#39;88&#39;,&#39;90&#39;,&#39;90&#39;],&#39;数学&#39;:[&#39;&#39;,&#39;98&#39;,&#39;96&#39;,&#39;77&#39;,&#39;90&#39;,&#39;90&#39;]}

这种自定义的空字符串用不了fillna()，请问下这块，怎么进行处理？</div>2020-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ae/cf/dad08a72.jpg" width="30px"><span>酱油不好打</span> 👍（0） 💬（1）<div>import pandas as pd
data = {&#39;语文&#39;: [66, 95, 93, 90, 80, 80], &#39;英语&#39;: [65, 85, 92, 88, 90, 90],
        &#39;数学&#39;: [None, 98, 96, 77, 90, 90]}
df = pd.DataFrame(data, index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;],
                  columns=[u&#39;英语&#39;, u&#39;数学&#39;, u&#39;语文&#39;])
df=df.dropna()
df[u&#39;总和&#39;] = df[u&#39;语文&#39;]+df[u&#39;英语&#39;]+df[u&#39;数学&#39;]
df.head()</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8e/1f/f96bd42d.jpg" width="30px"><span>落空</span> 👍（0） 💬（1）<div>#使用Jupyter Notebook编写
#版本：python 3.6
import pandas as pd

#新建DataFrame成绩单
data = {&#39;Chinese&#39;: [66, 95, 93, 90, 80, 80], &#39;English&#39;: [65, 85, 92, 88, 90, 90],
        &#39;Math&#39;: [None, 98, 96, 77, 90, 90]}
df = pd.DataFrame(data, index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;],
                  columns=[&#39;English&#39;, &#39;Math&#39;, &#39;Chinese&#39;])

#查看数据情况
df.info()  #可以查看缺失值等情况
df.describe() #描述性统计常见统计值

#处理缺失值，用均值填充
df[&#39;Math&#39;].fillna(df[&#39;Math&#39;].mean(), inplace=True)
df[&#39;Math&#39;] = df[&#39;Math&#39;].astype(int)
# 去除重复行
df = df.drop_duplicates()
#计算成绩总和
df[&#39;总和&#39;] = df.eval(&quot;English + Math + Chinese&quot;)
#成绩排个序
df = df.sort_values(&#39;总和&#39;,ascending=False)</div>2020-08-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/twibiaV0K4L2f8wTjCjRYp3IFOHg4um1cgj233ibJVicmjF1Qsb7JFib6icBkFu68kT0ueMIA89GcXfv9g3InkGViciaRQ/132" width="30px"><span>liubin</span> 👍（0） 💬（1）<div>ImportError: cannot import name &#39;sqldf&#39;  我安装了sqldf还是报这个错</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/68/90/ca86abe3.jpg" width="30px"><span>CHEN</span> 👍（0） 💬（1）<div>import pandas as pd
import numpy as np

scores = pd.DataFrame(
    {&quot;语文&quot;: [66, 95, 95, 90, 80, 80], &quot;英语&quot;: [65, 85, 92, 88, 90, 90], &quot;数学&quot;: [np.nan, 98, 96, 77, 90, 90]},
    index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;]
)
# 去重
scores = scores.drop_duplicates()
# 替换NaN值
print(scores.isnull().any())  #查看哪一列有空值
scores = scores.fillna(scores[&#39;数学&#39;].mean())
# 增加一行统计
scores[&#39;总分&#39;] = scores.sum(axis=1)
# 按总分倒序排列
scores = scores.sort_values(by=&quot;总分&quot;, ascending=False)
print(scores)

#输出清洗结果到csv文件进行保存
scores.to_csv(&#39;scores.csv&#39;)</div>2020-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0e/3d/ded8bc06.jpg" width="30px"><span>As1m0v</span> 👍（0） 💬（1）<div>练习题解答：
python3

import pandas as pd
from pandas import DataFrame, Series

# 创建DataFrame
test_data = {&#39;语文&#39;:[66, 95, 95, 90, 80, 80],
          &#39;英语&#39;:[65, 85, 92, 88, 90, 90],
          &#39;数学&#39;:[None, 98, 96, 77, 90, 90]}

test_df = DataFrame(test_data,
                    columns = [&#39;语文&#39;, &#39;英语&#39;, &#39;数学&#39;],
                   index = [&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;])
test_df.index.name = &#39;姓名&#39;

# 数据清洗
# 删除重复数据
test_df.drop_duplicates(inplace = True)

# 检查含有缺失值数据行
cond=test_df[test_df.isnull().any(axis = 1)]

# 思路一:删除含有缺失值数据行
test_df.drop(index = &#39;张飞&#39;, axis = 1,inplace = True)

# 思路二:补全含有缺失数据行(补全为0
test_df.fillna(0, inplace = True)

# 思路三:补全有缺失数据行(用平均值补充)
test_df.fillna(test_df[&#39;数学&#39;].mean(), inplace = True)

# 思路四:补全有缺失数据行(用插值补充)
test_df = test_df.fillna(method = &#39;ffill&#39;, axis = 1)

# 添加‘总和’列
f4 = lambda x: x[0] + x[1] + x[2]
test_df[&#39;总和&#39;] = test_df.apply(f4, axis = &#39;columns&#39;)</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/54/d9/76a53118.jpg" width="30px"><span>清风</span> 👍（0） 💬（1）<div>data = {&#39;姓名&#39;:[&#39;张飞&#39;,&#39;关羽&#39;, &#39;赵云&#39;, &#39;黄忠&#39;, &#39;典韦&#39;, &#39;典韦&#39;], &#39;语文&#39;:[66,95,95,90,80,80], &#39;英语&#39;:[65,85,92,88,90,90], &#39;数学&#39;: [None,98,96,77,90,90]}
df3 = DataFrame(data)
df3 = df3.set_index(&#39;姓名&#39;)

# 去重
df3.duplicated()
df3.drop_duplicates(keep=&#39;first&#39;)

# 查取空值 用均值填补
df3.isnull().any()
df3[&#39;数学&#39;].fillna(df3[&#39;数学&#39;].mean(), inplace=True)

# 新增总和一列
sum = 0
#df3[&#39;总和&#39;] = df3[&#39;语文&#39;] + df3[&#39;英语&#39;] + df3[&#39;数学&#39;]
# df3.drop(columns=&#39;总和&#39;, inplace=True)
df3[&#39;总和&#39;] = df3.sum(axis=1)
df3</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/70/9f/741cd6a4.jpg" width="30px"><span>Henry</span> 👍（0） 💬（1）<div># 练习 python 3.x
data = {&#39;Chinese&#39;: [66, 95, 95, 90, 80, 80],
        &#39;English&#39;: [65, 85, 92, 88, 90, 90],
        &#39;Math&#39;: [None, 98, 96, 77, 90, 90]}
df = DataFrame(data, index=[&#39;ZhangFei&#39;, &#39;GuanYu&#39;, &#39;ZhaoYun&#39;, &#39;HuangZhong&#39;, &#39;DianWei&#39;, &#39;DianWei&#39;], columns=[&#39;English&#39;, &#39;Math&#39;, &#39;Chinese&#39;])
print(df)

df.drop_duplicates(inplace=True)
print(df)
df.dropna(inplace=True)
print(df)
df[&#39;total&#39;] = df.apply(func=lambda x: sum(x), axis=1)
print(df)</div>2020-05-11</li><br/>
</ul>