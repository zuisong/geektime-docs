今天我来带你进行K-Means的学习。K-Means是一种非监督学习，解决的是聚类问题。K代表的是K类，Means代表的是中心，你可以理解这个算法的本质是确定K类的中心点，当你找到了这些中心点，也就完成了聚类。

那么请你和我思考以下三个问题：

- 如何确定K类的中心点？
- 如何将其他点划分到K类中？
- 如何区分K-Means与KNN？

如果理解了上面这3个问题，那么对K-Means的原理掌握得也就差不多了。

先请你和我思考一个场景，假设我有20支亚洲足球队，想要将它们按照成绩划分成3个等级，可以怎样划分？

## K-Means的工作原理

对亚洲足球队的水平，你可能也有自己的判断。比如一流的亚洲球队有谁？你可能会说伊朗或韩国。二流的亚洲球队呢？你可能说是中国。三流的亚洲球队呢？你可能会说越南。

其实这些都是靠我们的经验来划分的，那么伊朗、中国、越南可以说是三个等级的典型代表，也就是我们每个类的中心点。

所以回过头来，如何确定K类的中心点？一开始我们是可以随机指派的，当你确认了中心点后，就可以按照距离将其他足球队划分到不同的类别中。

这也就是K-Means的中心思想，就是这么简单直接。你可能会问：如果一开始，选择一流球队是中国，二流球队是伊朗，三流球队是韩国，中心点选择错了怎么办？其实不用担心，K-Means有自我纠正机制，在不断的迭代过程中，会纠正中心点。中心点在整个迭代过程中，并不是唯一的，只是你需要一个初始值，一般算法会随机设置初始的中心点。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（35） 💬（2）<div>两者的区别的比喻是，
Kmeans开班，选老大，风水轮流转，直到选出最佳中心老大
Knn小弟加队伍，离那个班相对近，就是那个班的

一群人的有些人想要聚在一起
首先大家民主（无监督学习）随机选K个老大（随机选择K个中心点）
谁跟谁近，就是那个队伍的人（计算距离，距离近的聚合到一块）
随着时间的推移，老大的位置在变化（根据算法，重新计算中心点）
直到选出真正的中心老大（重复，直到准确率最高）

Knn
一个人想要找到自己的队伍
首先听从神的旨意（有监督学习），随机最近的几个邻居
看看距离远不远（根据算法，计算距离）
近的就是一个班的了（属于哪个分类多，就是哪一类）

#输入数据
#数据探索
import pandas as pd
data=pd.read_csv(&quot;.&#47;26&#47;data.csv&quot;,encoding=&#39;gbk&#39;)
# print(data)数据符合完整合一，数据质量较高

#提取数据
train_x=data[[&quot;2019年国际排名&quot;,&quot;2018世界杯&quot;,&quot;2015亚洲杯&quot;]]

#数据规范化
from sklearn import preprocessing
ss=preprocessing.StandardScaler()
train_ss_x=ss.fit_transform(train_x)

#对数据进行拟合并预测
from sklearn.cluster import KMeans
kmeans=KMeans(n_clusters=5)
kmeans.fit(train_ss_x)
pre=kmeans.predict(train_ss_x)

#数据对比
train_x=pd.DataFrame(train_x)
result=pd.concat((data,pd.DataFrame(pre)),axis=1)

result.rename({0:u&#39;聚类&#39;},axis=1,inplace=True)
print(result)</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/eb/6d6a94d2.jpg" width="30px"><span>Lee</span> 👍（9） 💬（1）<div># coding: utf-8
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
# 输入数据
data = pd.read_csv(r&#39;F:\Python\notebook\K-Means\kmeans-master\data.csv&#39;, encoding = &#39;gbk&#39;)
data.head()
train_x = data[[&quot;2019年国际排名&quot;,&quot;2018世界杯&quot;,&quot;2015亚洲杯&quot;]]
df = pd.DataFrame(train_x)
kmeans = KMeans(n_clusters=5)
# 规范化
min_max_scaler=preprocessing.StandardScaler()
train_x=min_max_scaler.fit_transform(train_x)
# kmeans 算法
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u&#39;聚类&#39;},axis=1,inplace=True)
print(result)

       国家  2019年国际排名  2018世界杯  2015亚洲杯  聚类
0       中国         73       40        7   0
1       日本         60       15        5   3
2       韩国         61       19        2   3
3       伊朗         34       18        6   3
4       沙特         67       26       10   0
5      伊拉克         91       40        4   0
6      卡塔尔        101       40       13   4
7      阿联酋         81       40        6   0
8   乌兹别克斯坦         88       40        8   0
9       泰国        122       40       17   4
10      越南        102       50       17   4
11      阿曼         87       50       12   2
12      巴林        116       50       11   2
13      朝鲜        110       50       14   2
14      印尼        164       50       17   1
15      澳洲         40       30        1   3
16     叙利亚         76       40       17   4
17      约旦        118       50        9   2
18     科威特        160       50       15   1
19    巴勒斯坦         96       50       16   4</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/aa/d1/076482f3.jpg" width="30px"><span>白夜</span> 👍（10） 💬（3）<div>然后我们再重新计算这三个类的中心点，如何计算呢？最简单的方式就是取平均值，然后根据新的中心点按照距离远近重新分配球队的分类，再根据球队的分类更新中心点的位置。计算过程这里不展开，最后一直迭代（重复上述的计算过程：计算中心点和划分分类）到分类不再发生变化。

老师，这段可以再解释一下吗？没计算过程不太理解</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ec/c4/19f85ada.jpg" width="30px"><span>乃鱼同学</span> 👍（7） 💬（1）<div>K-Means 是聚类算法：经常做坏事的人 ，就是坏人。
KNN 是分类算法：坏人经常做坏事。
我对孩子就是这么说的。</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/50/91/0dd2b8ce.jpg" width="30px"><span>听妈妈的话</span> 👍（4） 💬（3）<div>代码里的第八行应该去掉列名里的空格：
train_x = data[[&#39;2019年国际排名&#39;,&#39;2018世界杯&#39;,&#39;2015亚洲杯&#39;]]
Z-score标准化的代码：train_x=preprocessing.scale(train_x)

国家	2019年国际排名	2018世界杯	2015亚洲杯	聚类
0	中国	73	40	7	3
1	日本	60	15	5	1
2	韩国	61	19	2	1
3	伊朗	34	18	6	1
4	沙特	67	26	10	1
5	伊拉克	91	40	4	3
6	卡塔尔	101	40	13	0
7	阿联酋	81	40	6	3
8	乌兹别克斯坦	88	40	8	3
9	泰国	122	40	17	4
10	越南	102	50	17	4
11	阿曼	87	50	12	0
12	巴林	116	50	11	0
13	朝鲜	110	50	14	0
14	印尼	164	50	17	2
15	澳洲	40	30	1	1
16	叙利亚	76	40	17	4
17	约旦	118	50	9	0
18	科威特	160	50	15	2
19	巴勒斯坦	96	50	16	4</div>2019-03-22</li><br/><li><img src="" width="30px"><span>iamtalent123</span> 👍（4） 💬（2）<div>老师，请问为什么要对train_x转化为datadframe格式呢？df=pd.DataFrame(train_x)，df有什么用呢？</div>2019-03-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1rd5KVxbBWO1Jnq3syrfRQg0NGerVl4Dt7uHTMcy9A7KTqxmy7iaoomoWsjuHM4n7fBr0ESG8OqfJKCDHExzjvQ/132" width="30px"><span>juixv3937</span> 👍（2） 💬（2）<div>为什么,你们的代码,运行出来跟我的结果都不一样</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/de/5c67895a.jpg" width="30px"><span>周飞</span> 👍（2） 💬（1）<div>k-means的算法原理就是：
1.选择几个初始的中心点。
2.计算每个点到各个中心点的距离，然后把每个点划分到距离最近的中心点所在的类。
3.更新中心点的值。对于每个类，计算类中所有数据的平均值，把平均值作为新的中心点。
4.重复 2 和4 步骤，直到每个类中的数据不再变化，或者到达指定的迭代步数。</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/21/c03839f1.jpg" width="30px"><span>FORWARD―MOUNT</span> 👍（2） 💬（2）<div>如何调整聚类中心没听懂</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d6/c7/7390039f.jpg" width="30px"><span>Jack</span> 👍（1） 💬（1）<div>老师，对于K-Means算法，我们如何评估模型的好坏，常用的评价指标都有哪些呢？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/40/39d41615.jpg" width="30px"><span>Yafei</span> 👍（1） 💬（1）<div>这也就是 K-Means 的中心思想，就是这么简单直接。你可能会问：如果一开始，选择一流球队是中国，二流球队是伊朗，三流球队是韩国，中心点选择错了怎么办？其实不用担心，K-Means 有自我纠正机制，在不断的迭代过程中，会纠正中心点。中心点在整个迭代过程中，并不是唯一的，只是你需要一个初始值，一般算法会随机设置初始的中心点。
老师，这段是否表述有误，如果你一开始就给中国一流球队的标签，在计算所有点到中国距离的平均距离过程中，分类点会收敛到这类标签的中心点，但是标签还是一流球队，并不会改变，变化的仅是分类点。因此，对于聚类，我们只是将所有样本点归到一个类别下，具体类别的标签应该是我们自己来标记的。如理解不对，还望指正！</div>2019-07-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/wJphZ3HcvhjVUyTWCIsCugzfQY5NAy6VJ0XoPLibDlcHWMswFmFe678zd0lUjFETia80NQhyQcVnGDlKgKPcRGyw/132" width="30px"><span>JingZ</span> 👍（1） 💬（2）<div>import numpy as np 这行代码不需要吧~感觉没用到</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/86/79/066a062a.jpg" width="30px"><span>非同凡想</span> 👍（0） 💬（1）<div>交作业了
import pandas as pd
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.cluster import KMeans

data  = pd.read_csv(&#39;~&#47;Documents&#47;kmeans&#47;data.csv&#39;,encoding=&#39;gbk&#39;)

print(data.info())
print(data.head())

features = data.columns[1:]

train_x = data[features]

# scaler = MinMaxScaler()
scaler = StandardScaler()
train_x = scaler.fit_transform(train_x)

model = KMeans(n_clusters=5)

clusters = model.fit_predict(train_x)
data[&#39;聚类&#39;] = clusters
print(data)

       国家  2019年国际排名  2018世界杯  2015亚洲杯  聚类
0       中国         73       40        7   2
1       日本         60       15        5   1
2       韩国         61       19        2   1
3       伊朗         34       18        6   1
4       沙特         67       26       10   1
5      伊拉克         91       40        4   2
6      卡塔尔        101       40       13   0
7      阿联酋         81       40        6   2
8   乌兹别克斯坦         88       40        8   2
9       泰国        122       40       17   4
10      越南        102       50       17   4
11      阿曼         87       50       12   0
12      巴林        116       50       11   0
13      朝鲜        110       50       14   0
14      印尼        164       50       17   3
15      澳洲         40       30        1   1
16     叙利亚         76       40       17   4
17      约旦        118       50        9   0
18     科威特        160       50       15   3
19    巴勒斯坦         96       50       16   4</div>2020-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ziaN7rOONp15HJm6A9JoAYicJL8VA59x10DX4JZyvcfqmmpCnumXgAkNn37aFoALftyTaQNlUF7te54LibvVm20TQ/132" width="30px"><span>Geek_c9fa4e</span> 👍（0） 💬（1）<div>K-Means的算法原理：就是通过初始化一个类别，通过计算出它们直接的距离，来区别属于哪一个类。</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bf/e3/2aa8ec84.jpg" width="30px"><span>鱼非子</span> 👍（0） 💬（1）<div>        国家  2019年国际排名  2018世界杯  2015亚洲杯  聚类
0       中国         73       40        7   3
1       日本         60       15        5   1
2       韩国         61       19        2   1
3       伊朗         34       18        6   1
4       沙特         67       26       10   3
5      伊拉克         91       40        4   3
6      卡塔尔        101       40       13   0
7      阿联酋         81       40        6   3
8   乌兹别克斯坦         88       40        8   3
9       泰国        122       40       17   0
10      越南        102       50       17   0
11      阿曼         87       50       12   2
12      巴林        116       50       11   2
13      朝鲜        110       50       14   2
14      印尼        164       50       17   4
15      澳洲         40       30        1   1
16     叙利亚         76       40       17   0
17      约旦        118       50        9   2
18     科威特        160       50       15   4
19    巴勒斯坦         96       50       16   0
</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bf/e3/2aa8ec84.jpg" width="30px"><span>鱼非子</span> 👍（0） 💬（1）<div># coding: utf-8

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing

data = pd.read_csv(&quot;data.csv&quot;,encoding=&#39;gbk&#39;)
print(data.head(5))

train_x = data[[&quot;2019年国际排名&quot;,&quot;2018世界杯&quot;,&quot;2015亚洲杯&quot;]]
# df = pd.DataFrame(data)

model = KMeans(n_clusters=5)
stand = preprocessing.StandardScaler()
# min_max_scaler = preprocessing.MinMaxScaler()
# train_x = min_max_scaler.fit_transform(train_x)
train_x = stand.fit_transform(train_x)

model.fit(train_x)
predict = model.predict(train_x)

# df[&#39;聚类&#39;] = predict
data[&#39;聚类&#39;] = predict
# result = pd.concat((data,pd.DataFrame(predict)),axis=1)
print(data)</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（0） 💬（1）<div>from sklearn.cluster import KMeans
from sklearn import preprocessing
import numpy as np
import pandas as pd

#输出数据
data=pd.read_csv(&#39;.&#47;kmeans-master&#47;data.csv&#39;,encoding =&#39;gbk&#39;)
train_x = data[[&#39;2019年国际排名&#39;,&#39;2018世界杯&#39;,&#39;2015亚洲杯&#39;]]

#规范化数据
min_max_scaler=preprocessing.MinMaxScaler()
train_x_mm=min_max_scaler.fit_transform(train_x)
# print(train_x)

#构建kmeans聚类器
kmeans = KMeans(n_clusters=3)
kmeans.fit(train_x_mm)
pred_y=kmeans.predict(train_x_mm)

#合并聚类结果
result = pd.concat((data,pd.DataFrame(pred_y)),axis=1)
result.rename({0:u&#39;聚类&#39;},axis=1,inplace=True)
print(result)
print(&#39;\n&#39;)


#练习：K-Means=5,且采用标准化方式规范化

#规范化数据StandScaler
ss=preprocessing.StandardScaler()
train_x_z=ss.fit_transform(train_x)
print(train_x_z)

#构建kmeans聚类器
kmeans = KMeans(n_clusters=5)
kmeans.fit(train_x_z)
pred2_y=kmeans.predict(train_x_z)

#合并聚类结果
result = pd.concat((data,pd.DataFrame(pred2_y)),axis=1)
result.rename({0:u&#39;聚类&#39;},axis=1,inplace=True)
print(result)</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/07/0c1c76c2.jpg" width="30px"><span>Frederick</span> 👍（0） 💬（1）<div>老师，我想问下，决策树可以用来聚类吗，如果可以，要怎么做呢？</div>2019-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/a0/f12115b7.jpg" width="30px"><span>Sam.张朝</span> 👍（0） 💬（1）<div>运行一次，结果变化一次。</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/a0/f12115b7.jpg" width="30px"><span>Sam.张朝</span> 👍（0） 💬（3）<div>文章里的代码也好，问题的解决代码也好，中国都会在0 和2 之间变化。运行一次，变化一次。</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（0） 💬（1）<div>老师，想问个问题，为何我计算出来的结果正好相反，就是后面聚类生成的0、1、2 这些数据，最弱的队归位来0类，一流队归类来2类，看留言里的代码大家计算出来的结果也不尽相同，想问下老师，是不是K-Means结果只是起到聚类的效果，没有展示其它属性的效果</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/de/5c67895a.jpg" width="30px"><span>周飞</span> 👍（0） 💬（1）<div>分为5来的代码：
# coding: utf-8
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
# 输入数据
data = pd.read_csv(&#39;data.csv&#39;, encoding=&#39;gbk&#39;)
print(data)
train_x = data[[&quot;2019年国际排名&quot;,&quot;2018世界杯&quot;,&quot;2015亚洲杯&quot;]]
df = pd.DataFrame(train_x)
kmeans = KMeans(n_clusters=5)
# 规范化到 [0,1] 空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
# kmeans 算法
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u&#39;聚类&#39;},axis=1,inplace=True)
result.sort_values(&#39;聚类&#39;,inplace=True)
print(result)
运行结果：
        国家  2019年国际排名  2018世界杯  2015亚洲杯  聚类
0       中国         73       40        7   0
5      伊拉克         91       40        4   0
7      阿联酋         81       40        6   0
8   乌兹别克斯坦         88       40        8   0
18     科威特        160       50       15   1
14      印尼        164       50       17   1
1       日本         60       15        5   2
2       韩国         61       19        2   2
3       伊朗         34       18        6   2
4       沙特         67       26       10   2
15      澳洲         40       30        1   2
17      约旦        118       50        9   3
11      阿曼         87       50       12   3
12      巴林        116       50       11   3
13      朝鲜        110       50       14   3
16     叙利亚         76       40       17   4
9       泰国        122       40       17   4
6      卡塔尔        101       40       13   4
10      越南        102       50       17   4
19    巴勒斯坦         96       50       16   4
</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（0） 💬（1）<div>Kmeans开班，选老大，风水轮流转，直到选出最佳中心老大
Knn小弟加队伍，离那个班相对近，就是那个班的

一群人的有些人想要聚在一起
首先大家民主（无监督学习）随机选K个老大（随机选择K个中心点）
谁跟谁近，就是那个队伍的人（计算距离，距离近的聚合到一块）
随着时间的推移，老大的位置在变化（根据算法，重新计算中心点）
直到选出真正的中心老大（重复，直到准确率最高）

Knn
一个人想要找到自己的队伍
首先听从神的旨意（有监督学习），随机最近的几个邻居
看看距离远不远（根据算法，计算距离）
近的就是一个班的了（属于哪个分类多，就是哪一类）</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e5/43/7bc7cfe3.jpg" width="30px"><span>跳跳</span> 👍（0） 💬（1）<div>k-means的原理是：先假定有要聚类个数个中心点，然后根据中心点对其余点分类。接着重新计算中心点，计算的时候采用取均值的方式，再重新划分中心点，再对其余点分类。以此类推
# coding: utf-8
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
# 输入数据
data = pd.read_csv(&#39;data1.csv&#39;, encoding=&#39;gbk&#39;)
train_x = data[[&quot;2019年国际排名&quot;,&quot;2018世界杯&quot;,&quot;2015亚洲杯&quot;]]
df = pd.DataFrame(train_x)
kmeans = KMeans(n_clusters=5)
# 规范化到标准空间
ss = preprocessing.StandardScaler()
train_x = ss.fit_transform(train_x)
# kmeans 算法
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u&#39;聚类&#39;},axis=1,inplace=True)
print(result)
k-means分成5类在代码中体现为n_clusters=5，0-1标准化体现在StandardScaler

</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f8/1e/0d5f8336.jpg" width="30px"><span>fancy</span> 👍（0） 💬（1）<div>K-Means算法原理：
1. 初始化K类，比如K=3，K1=中国，K2=日本，K3=韩国，所以，此时这三类的中心点分别为K1=(0.3,0.71428571,0.375)
K2=(0.2,0,0.25)
K3=(0.20769231,0.11428571,0.0624)
将每个国家看作一个点，此时这三个类别还是空的，不包含任何样本数据中的点
2. 计算样本数据中各点到初始化中心点的距离，每个点被分配到距离近的中心点所在的类别
3. 经过步骤2的计算分类后，现在K1，K2，K3中都包含了多个点，这时，分别计算每个类别中的所有点的特征值的平均值，将这个平均值作为新的中心点，这就是为什么叫K-Means；在这里，每个点含有三个特征，那么就要分别计算这三个特征值的平均值
4. 再次计算各点到新的中心点的距离，每个中心点代表的类别不变，还是中、日、韩三国。将点分类到距离近的那个类别
5. 重复3，4，直到各点所属类别不再发生变化，或者到达了max_iter所设置的最大迭代次数，停止。</div>2019-03-04</li><br/><li><img src="" width="30px"><span>liyooo</span> 👍（0） 💬（1）<div>眼界大开！</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（0） 💬（1）<div># 划分成 5 类
kmeans = KMeans(n_clusters=5)
# Z-Score规范化
from sklearn.preprocessing import StandardScaler
standardscaler = StandardScaler()
train_x = standardscaler.fit_transform(train_x)
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
result = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
result.rename({0: &#39;聚类&#39;}, axis=1, inplace=True)
result
国家	2019年国际排名	2018世界杯	2015亚洲杯	聚类
0	中国	73	40	7	3
1	日本	60	15	5	1
2	韩国	61	19	2	1
3	伊朗	34	18	6	1
4	沙特	67	26	10	1
5	伊拉克	91	40	4	3
6	卡塔尔	101	40	13	0
7	阿联酋	81	40	6	3
8	乌兹别克斯坦	88	40	8	3
9	泰国	122	40	17	4
10	越南	102	50	17	4
11	阿曼	87	50	12	0
12	巴林	116	50	11	0
13	朝鲜	110	50	14	0
14	印尼	164	50	17	2
15	澳洲	40	30	1	1
16	叙利亚	76	40	17	4
17	约旦	118	50	9	0
18	科威特	160	50	15	2
19	巴勒斯坦	96	50	16	4
</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/53/60fe31fb.jpg" width="30px"><span>深白浅黑</span> 👍（0） 💬（1）<div>kmean是无监督的聚类算法，先对K类数量进行设置，再设置K类的中心点，算法会自行在迭代过程中对中心点进行调整，按照各点与中心点的距离进行分类划分，直至分类不变。
比较适数据特征的归类。
        国家  2019年国际排名  2018世界杯  2015亚洲杯  聚类
0       中国         73       40        7   3
1       日本         60       15        5   1
2       韩国         61       19        2   1
3       伊朗         34       18        6   1
4       沙特         67       26       10   1
5      伊拉克         91       40        4   3
6      卡塔尔        101       40       13   0
7      阿联酋         81       40        6   3
8   乌兹别克斯坦         88       40        8   3
9       泰国        122       40       17   2
10      越南        102       50       17   2
11      阿曼         87       50       12   0
12      巴林        116       50       11   0
13      朝鲜        110       50       14   0
14      印尼        164       50       17   4
15      澳洲         40       30        1   1
16     叙利亚         76       40       17   2
17      约旦        118       50        9   0
18     科威特        160       50       15   4
19    巴勒斯坦         96       50       16   2</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/19/5ee3f996.jpg" width="30px"><span>切克闹</span> 👍（0） 💬（1）<div>K-Means中关于如何更新中心点，以及方式不太清楚</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cb/07/e34220d6.jpg" width="30px"><span>李沛欣</span> 👍（0） 💬（1）<div>K-means是聚类算法，属于非监督式学习，K代表了类别数；

KNN 是分类算法，属于有监督式学习，K代表了K个抱团的邻居；

看到Kmeans总会想起被因子分析法支配的恐惧，哈哈😄</div>2019-02-15</li><br/>
</ul>