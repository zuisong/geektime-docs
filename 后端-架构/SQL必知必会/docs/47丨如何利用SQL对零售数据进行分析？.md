我们通过OLTP系统实时捕捉到了用户的数据，还需要在OLAP系统中对它们进行分析。之前我们讲解了如何对数据进行清洗，以及如何对分散在不同地方的数据进行集成，今天我们来看下如何使用SQL分析这些数据。

关于这部分内容，今天我们一起来学习下：

1. 使用SQL进行数据分析都有哪几种姿势？
2. 如何通过关联规则挖掘零售数据中的频繁项集？
3. 如何使用SQL+Python完成零售数据的关联分析？

## 使用SQL进行数据分析的5种姿势

在DBMS中，有些数据库管理系统很好地集成了BI工具，可以方便我们对收集的数据进行商业分析。

SQL Server提供了BI分析工具，我们可以通过使用SQL Server中的Analysis Services完成数据挖掘任务。SQL Server内置了多种数据挖掘算法，比如常用的EM、K-Means聚类算法、决策树、朴素贝叶斯和逻辑回归等分类算法，以及神经网络等模型。我们还可以对这些算法模型进行可视化效果呈现，帮我们优化和评估算法模型的好坏。

PostgreSQL是免费开源的对象-关系数据库（ORDBMS），它的稳定性非常强，功能强大，在OLTP和OLAP系统上表现都非常出色。同时在机器学习上，配合Madlib项目可以让PostgreSQL如虎添翼。Madlib包括了多种机器学习算法，比如分类、聚类、文本分析、回归分析、关联规则挖掘和验证分析等功能。这样我们可以通过使用SQL，在PostgreSQL中使用各种机器学习算法模型，帮我们进行数据挖掘和分析。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（19） 💬（2）<div>import numpy as np
import pandas as pd
title = [&#39;牛奶&#39;, &#39;面包&#39;, &#39;尿布&#39;, &#39;可乐&#39;, &#39;啤酒&#39;, &#39;鸡蛋&#39;];
x = [[1, 1, 1, 0, 0, 0],
     [0, 1, 1, 1, 1, 0],
     [1, 0, 1, 0, 1, 1],
     [1, 1, 1, 0, 1, 0],
     [1, 1, 1, 1, 0, 0]]
df = pd.DataFrame(x, columns=title)


# 创建两个表 分别作为支持度和置信度的准备表
df1 = pd.DataFrame(np.zeros([1, 6]), index=[&#39;支持度&#39;], columns=title)
df2 = pd.DataFrame(np.zeros([6, 6]), index=title, columns=title)
df3 = pd.DataFrame(np.zeros([6, 6]), index=title, columns=title)


# 计算支持度
for i in x:
    for j in range(1):
        for k in range(j, 6):
           if not i[k] : continue
           df1.iloc[j,k] += 1

support = df1.apply(lambda x: x &#47;5)
# 返回支持度的结果
print(support)

# 计算置信度
for i in x:
    for j in range(5):
        # 如果为0 就跳过
        if not i[j] : continue
        # 如果不0，继续遍历，如果有购买，便+1
        for k in range(j+1,5):
            if not i[k] : continue
            df2.iloc[j,k] += 1
            df2.iloc[k,j] += 1
for j in range(6):
    df3.iloc[j] = df2.iloc[j] &#47; df.sum()[j]
confidence = df3.round(2) # 以3位小数返回置信度表
# 返回置信度的结果
print(confidence)

      牛奶   面包   尿布   可乐   啤酒   鸡蛋
支持度  0.8  0.8  1.0  0.4  0.6  0.2
      牛奶    面包   尿布    可乐   啤酒   鸡蛋
牛奶  0.00  0.75  1.0  0.25  0.5  0.0
面包  0.75  0.00  1.0  0.50  0.5  0.0
尿布  0.80  0.80  0.0  0.40  0.6  0.0
可乐  0.50  1.00  1.0  0.00  0.5  0.0
啤酒  0.67  0.67  1.0  0.33  0.0  0.0
鸡蛋  0.00  0.00  0.0  0.00  0.0  0.0
</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/f1/16545faf.jpg" width="30px"><span>学习</span> 👍（2） 💬（1）<div>牛奶，面包，尿布同时出现是3，支持度是3&#47;5=0.6</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（1） 💬（1）<div>	支持度
牛奶	0.8
面包	0.8
尿布	1
可乐	0.4
啤酒	0.6
鸡蛋	0.2
</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（1） 💬（1）<div>efficient-apriori官方文档
https:&#47;&#47;efficient-apriori.readthedocs.io&#47;en&#47;stable&#47;</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/a6/4e331ef4.jpg" width="30px"><span>骑行的掌柜J</span> 👍（0） 💬（1）<div>评论里朋友ttttt说” 
遇到错误：mysql.connector.errors.NotSupportedError) Authentication plugin &#39;caching_sha2_password&#39; is not supported “
换pymysql就可以，不过我这里有另一种解法，可以到我的博客看看，希望对你有帮助！谢谢
https:&#47;&#47;blog.csdn.net&#47;weixin_41013322&#47;article&#47;details&#47;103427293 </div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（0） 💬（1）<div>transactions = []
temp_index = 0
for i, v in orders_series.items():
    if i != temp_index:
        temp_set = set()
        temp_index = i
        temp_set.add(v)
        transactions.append(temp_set)
        print(transactions)
    else:
        temp_set.add(v)
老师，这里的transactions = [] 里面的元素，不应该是每个订单所有的商品集合吗？  但是上述代码不是实现这个需求</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（0） 💬（2）<div>
# 一行代码数据集格式转换
# transactions = list(data.groupby(&#39;Transaction&#39;).agg(lambda x: set(x.Item.values))[&#39;Item&#39;])
# 完整代码
from efficient_apriori import apriori
import sqlalchemy as sql
import pandas as pd

# 数据加载
engine = sql.create_engine(&#39;mysql+pymysql:&#47;&#47;root:passwd@localhost&#47;wucai&#39;)
query = &#39;SELECT * FROM bread_basket&#39;
data = pd.read_sql_query(query, engine)

# 统一小写
data[&#39;Item&#39;] = data[&#39;Item&#39;].str.lower()
# 去掉none项
data = data.drop(data[data.Item == &#39;none&#39;].index)

# 得到一维数组orders_series，并且将Transaction作为index, value为Item取值
orders_series = data.set_index(&#39;Transaction&#39;)[&#39;Item&#39;]
# 将数据集进行格式转换
transactions = transactions = list(data.groupby(&#39;Transaction&#39;).agg(lambda x: set(x.Item.values))[&#39;Item&#39;])

# 挖掘频繁项集和频繁规则
itemsets, rules = apriori(transactions, min_support=0.02, min_confidence=0.5)
print(&#39;频繁项集：&#39;, itemsets)
print(&#39;关联规则：&#39;, rules)

# ----------输出结果------------------ #
频繁项集： {1: {(&#39;alfajores&#39;,): 344, (&#39;bread&#39;,): 3096, (&#39;brownie&#39;,): 379, (&#39;cake&#39;,): 983, (&#39;coffee&#39;,): 4528, (&#39;cookies&#39;,): 515, (&#39;farm house&#39;,): 371, (&#39;hot chocolate&#39;,): 552, (&#39;juice&#39;,): 365, (&#39;medialuna&#39;,): 585, (&#39;muffin&#39;,): 364, (&#39;pastry&#39;,): 815, (&#39;sandwich&#39;,): 680, (&#39;scandinavian&#39;,): 275, (&#39;scone&#39;,): 327, (&#39;soup&#39;,): 326, (&#39;tea&#39;,): 1350, (&#39;toast&#39;,): 318, (&#39;truffles&#39;,): 192}, 2: {(&#39;bread&#39;, &#39;cake&#39;): 221, (&#39;bread&#39;, &#39;coffee&#39;): 852, (&#39;bread&#39;, &#39;pastry&#39;): 276, (&#39;bread&#39;, &#39;tea&#39;): 266, (&#39;cake&#39;, &#39;coffee&#39;): 518, (&#39;cake&#39;, &#39;tea&#39;): 225, (&#39;coffee&#39;, &#39;cookies&#39;): 267, (&#39;coffee&#39;, &#39;hot chocolate&#39;): 280, (&#39;coffee&#39;, &#39;juice&#39;): 195, (&#39;coffee&#39;, &#39;medialuna&#39;): 333, (&#39;coffee&#39;, &#39;pastry&#39;): 450, (&#39;coffee&#39;, &#39;sandwich&#39;): 362, (&#39;coffee&#39;, &#39;tea&#39;): 472, (&#39;coffee&#39;, &#39;toast&#39;): 224}}
关联规则： [{cake} -&gt; {coffee}, {cookies} -&gt; {coffee}, {hot chocolate} -&gt; {coffee}, {juice} -&gt; {coffee}, {medialuna} -&gt; {coffee}, {pastry} -&gt; {coffee}, {sandwich} -&gt; {coffee}, {toast} -&gt; {coffee}]</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（2） 💬（0）<div>遇到错误：NotSupportedError: (mysql.connector.errors.NotSupportedError) Authentication plugin &#39;caching_sha2_password&#39; is not supported (Background on this error at: http:&#47;&#47;sqlalche.me&#47;e&#47;tw8g)
解决方法
engine = sql.create_engine( &#39;mysql+pymysql:&#47;&#47;{}:{}@{}&#47;{}&#39;.format(user, passwd, host, database))
mysql+mysqlconnector 改成 mysql+pymysql 就行了</div>2019-09-27</li><br/><li><img src="" width="30px"><span>邵家伟</span> 👍（1） 💬（0）<div>C#
string[] item = { &quot;牛奶&quot;, &quot;面包&quot;, &quot;尿布&quot;, &quot;鸡蛋&quot;, &quot;啤酒&quot;, &quot;可乐&quot; };
            int[,] Record = { { 1, 1, 1, 0, 0, 0 }, { 0, 1, 1, 0, 1, 0 }, { 1, 0, 1, 1, 1, 0 }, { 1, 1, 1, 0, 1, 0 }, { 1, 1, 1, 0, 0, 1 } };
            double SupportRate;
            for (int a = 0; a &lt; 6; a++)&#47;&#47;列遍历
            {	int Count = 0;int total = 0;
                for (int b = 0; b &lt; 5; b++)&#47;&#47;行遍历
                {	total += 1;
                    if (Record[b, a] == 1)  Count += 1;
                }
                SupportRate = Convert.ToDouble(Count) &#47; Convert.ToDouble(total);
                Context.Response.Write(item[a] + &quot;支持度为&quot; + SupportRate+&quot;&lt;&#47;br&gt;&quot;);
            }
            double[,] BelieveRate = new double[6, 6];
            for (int a = 0; a &lt; 6; a++)&#47;&#47;行
            {	for (int b = 0; b &lt; 6; b++) &#47;&#47;列
                {	if (a == b)  BelieveRate[a, b] = 0;
                    else
                    {	int total = 0;
                        int count = 0;
                        for (int c = 0; c &lt; 5; c++)
                        {	if(Record[c,a]==1)
                            {	total += 1;
                                if (Record[c, b] == 1)	count += 1;
                            }
                        }
             BelieveRate[a,b]=Convert.ToDouble(count)&#47;Convert.ToDouble(total);
                    }    
                }
            }
            for (int a = 0; a &lt; 7; a++)
            {	for (int b = 0; b &lt; 7; b++)
                {	if (a == 0 &amp;&amp; b == 0)	Context.Response.Write(&quot;置信度&quot;);
                    if(a==0&amp;&amp;b&gt;0)	Context.Response.Write(&quot;&amp;nbsp; &amp;nbsp; &quot; + item[b-1]+ &quot;&amp;nbsp; &amp;nbsp;&amp;nbsp; &quot;);
                    if (a &gt; 0 &amp;&amp; b == 0)	 Context.Response.Write(&quot;&amp;nbsp; &amp;nbsp;&quot; + item[a-1]+ &quot;&amp;nbsp; &amp;nbsp; &amp;nbsp;&quot;);
                    if (a &gt; 0 &amp;&amp; b &gt; 0)	Context.Response.Write(BelieveRate[a - 1, b - 1].ToString(&quot;0.00&quot;) + &quot; &amp;nbsp; &amp;nbsp; &amp;nbsp; &amp;nbsp;  &quot;);
                }
                Context.Response.Write(&quot;&lt;&#47;br&gt;&quot;);
            } 
</div>2021-07-07</li><br/><li><img src="" width="30px"><span>邵家伟</span> 👍（0） 💬（0）<div>结果：
牛奶支持度为0.8
面包支持度为0.8
尿布支持度为1
鸡蛋支持度为0.2
啤酒支持度为0.6
可乐支持度为0.2
置信度    牛奶         面包         尿布         鸡蛋         啤酒         可乐    
   牛奶     0.00         0.75         1.00         0.25         0.50         0.25        
   面包     0.75         0.00         1.00         0.00         0.50         0.25        
   尿布     0.80         0.80         0.00         0.20         0.60         0.20        
   鸡蛋     1.00         0.00         1.00         0.00         1.00         0.00        
   啤酒     0.67         0.67         1.00         0.33         0.00         0.00        
   可乐     1.00         1.00         1.00         0.00         0.00         0.00        </div>2021-07-07</li><br/>
</ul>