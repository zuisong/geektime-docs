今天我来带你进行EM的实战。上节课，我讲了EM算法的原理，EM算法相当于一个聚类框架，里面有不同的聚类模型，比如GMM高斯混合模型，或者HMM隐马尔科夫模型。其中你需要理解的是EM的两个步骤，E步和M步：E步相当于通过初始化的参数来估计隐含变量，M步是通过隐含变量来反推优化参数。最后通过EM步骤的迭代得到最终的模型参数。

今天我们进行EM算法的实战，你需要思考的是：

- 如何使用EM算法工具完成聚类？
- 什么情况下使用聚类算法？我们用聚类算法的任务目标是什么？
- 面对王者荣耀的英雄数据，EM算法能帮助我们分析出什么？

## 如何使用EM工具包

在Python中有第三方的EM算法工具包。由于EM算法是一个聚类框架，所以你需要明确你要用的具体算法，比如是采用GMM高斯混合模型，还是HMM隐马尔科夫模型。

这节课我们主要讲解GMM的使用，在使用前你需要引入工具包：

```

from sklearn.mixture import GaussianMixture

```

我们看下如何在sklearn中创建GMM聚类。

首先我们使用gmm = GaussianMixture(n\_components=1, covariance\_type=‘full’, max\_iter=100)来创建GMM聚类，其中有几个比较主要的参数（GMM类的构造参数比较多，我筛选了一些主要的进行讲解），我分别来讲解下：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/c4/83/d1c4237a.jpg" width="30px"><span>哆哩咪fa👻</span> 👍（15） 💬（5）<div>才买的课，请问有vx群或者可以相互沟通的群么</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a0/3a/312ce1b7.jpg" width="30px"><span>高桥凉瓜</span> 👍（11） 💬（2）<div>之所以热力图不显示最大攻速和攻击范围，是因为这两列的数据的类型是string，想要在热力图也显示这两项的话可以在构建热力图前就进行数据清洗：
```
data[u&#39;最大攻速&#39;] = data[u&#39;最大攻速&#39;].apply(lambda x: float(x.strip(&#39;%&#39;))&#47;100)
data[u&#39;攻击范围&#39;]=data[u&#39;攻击范围&#39;].map({&#39;远程&#39;:1,&#39;近战&#39;:0})
```</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/99/8e760987.jpg" width="30px"><span>許敲敲</span> 👍（7） 💬（1）<div>最后一个 data_to_csv()也最好加上encoding=&#39;gb18030&#39;;不然会乱码</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/5d/430ed3b6.jpg" width="30px"><span>从未在此</span> 👍（4） 💬（1）<div>问下老师，当几个特征相关性较大时，怎么选择最具有代表性的那个呢</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/de/5c67895a.jpg" width="30px"><span>周飞</span> 👍（2） 💬（2）<div>1.不做特征选择的情况下，得到的Calinski_Harabaz 分数 大约是 23.1530273621 ,做特征选择的情况下 大约是：21.2142191471.
2.聚类个数为3的时候 Calinski_Harabaz 分数 大约是 22.9119297953 。聚类个数为30的时候 Calinski_Harabaz 分数 大约是 21.2142191471</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/5d/430ed3b6.jpg" width="30px"><span>从未在此</span> 👍（2） 💬（2）<div>还有，非数值型的特征怎么进行聚类？</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/17/01/1c5309a3.jpg" width="30px"><span>McKee Chen</span> 👍（1） 💬（1）<div>分别针对以下三种情况进行聚类操作，得到的Calinski_Harabaz 分数分别为：
1.使用所有特征数，聚类类别为30，得分为33.286020580818494
2.特征数降维处理后，聚类类别为30，得分为27.964658388803077
3.特征数降维处理后，聚类类别为3，得分为19.358008332914284

根据以上结果，可以总结出：当聚类类别数相同时，特征数越多，聚类效果越好；当进行特征数降维处理时，聚类类别数越多，聚类效果越好</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9d/eb/2c7f3d3b.jpg" width="30px"><span>Ricky</span> 👍（0） 💬（1）<div>问个问题：关于calinski_harabaz_score的使用，同一套样本数据，用不同的模型计算prediction后，对比值得大小么？
谢谢！</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/36/88/20b6a6ee.jpg" width="30px"><span>Simon</span> 👍（0） 💬（1）<div>&#39;攻击范围&#39; 特征进行映射为0,1后，是不是可以不用z-score了？</div>2020-04-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/oseia6IjJIPziamTI2EQ0Bpr8icUicXTea2UuH105t4Bia4yFwBHld49cIQbjORvDdTtMCVdL39H9WxFwzyXspqqHUg/132" width="30px"><span>groot888</span> 👍（0） 💬（2）<div>热力图展现出来，相关的分数大，是不是也可以当做一种聚类算法。</div>2020-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（0） 💬（1）<div>全部特征，聚类个数为3个：
[0 0 2 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 2 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1
 1 0 1 1 1 1 1 1 1 0 0 0 1 2 0 2 0 0 0 0 0 1 2 0 2 2 0 2 1 1 0 1]
22.91192979526994
全部特征：聚类个数为30个
[16 12 11 13  2  2 19 11  3 12 15 12 13  8 24 15 25 13 21 27 26  7 27  7
  7  7 27 22 28  1  8  1 29 28  1  1 28  6 20 18 29 28 28  1 28 18 12 20
 12 28 17 14 21  4  4 16  0 12 23 21  0  5  9 16 10 14 14 16 22]
22.211084900636873</div>2019-04-20</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（0） 💬（1）<div>老师，同一程序每次运行结果不一样，有时赵云和孙悟空聚在一类，有时赵云和兰陵王聚在一类，这种情况正常吗？</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（0） 💬（1）<div># -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding(&#39;utf8&#39;)

import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

# 数据加载，避免中文乱码问题
data_ori = pd.read_csv(&#39;.&#47;heros.csv&#39;, encoding=&#39;gb18030&#39;)
features = [u&#39;最大生命&#39;, u&#39;生命成长&#39;, u&#39;初始生命&#39;, u&#39;最大法力&#39;, u&#39;法力成长&#39;, u&#39;初始法力&#39;, u&#39;最高物攻&#39;, u&#39;物攻成长&#39;, u&#39;初始物攻&#39;, u&#39;最大物防&#39;, u&#39;物防成长&#39;, u&#39;初始物防&#39;,
            u&#39;最大每5秒回血&#39;, u&#39;每5秒回血成长&#39;, u&#39;初始每5秒回血&#39;, u&#39;最大每5秒回蓝&#39;, u&#39;每5秒回蓝成长&#39;, u&#39;初始每5秒回蓝&#39;, u&#39;最大攻速&#39;, u&#39;攻击范围&#39;]
data = data_ori[features]

# 对英雄属性之间的关系进行可视化分析
# 设置 plt 正确显示中文
plt.rcParams[&#39;font.sans-serif&#39;] = [&#39;SimHei&#39;]  # 用来正常显示中文标签
plt.rcParams[&#39;axes.unicode_minus&#39;] = False  # 用来正常显示负号
# 用热力图呈现 features_mean 字段之间的相关性
corr = data[features].corr()
plt.figure(figsize=(14, 14))
# annot=True 显示每个方格的数据
sns.heatmap(corr, annot=True)
plt.show()

pd.set_option(&#39;mode.chained_assignment&#39;, None)
data[u&#39;最大攻速&#39;] = data[u&#39;最大攻速&#39;].apply(lambda x: float(x.strip(&#39;%&#39;)) &#47; 100)
data[u&#39;攻击范围&#39;] = data[u&#39;攻击范围&#39;].map({u&#39;远程&#39;: 1, u&#39;近战&#39;: 0})

# 采用 Z-Score 规范化数据，保证每个特征维度的数据均值为 0，方差为 1
ss = StandardScaler()
data = ss.fit_transform(data)

#print(data)

# 构造 GMM 聚类
gmm = GaussianMixture(n_components=3, covariance_type=&#39;full&#39;)
gmm.fit(data)
# 训练数据
prediction = gmm.predict(data)
print(prediction)

# 将分组结果输出到 CSV 文件中
data_ori.insert(0, &#39;分组&#39;, prediction)
data_ori.to_csv(&#39;.&#47;hero_out2.csv&#39;, index=False, sep=&#39;,&#39;, encoding=&#39;utf-8&#39;)

from sklearn.metrics import calinski_harabaz_score
print(calinski_harabaz_score(data, prediction))

    分组    英雄  最大生命   生命成长  初始生命  ...    初始每5秒回蓝    最大攻速  攻击范围  主要定位  次要定位 
0    0   夏侯惇  7350  288.8  3307  ...         15  28.00%    近战    坦克     战士
...
43   1    张良  5799  198.0  3027  ...         18  14.00%    远程    法师    NaN
...
68   2  百里守约  5611  185.1  3019  ...         16  28.00%    远程    射手     刺客

[69 rows x 24 columns]
23.869655882044263</div>2019-03-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/wJphZ3HcvhjVUyTWCIsCugzfQY5NAy6VJ0XoPLibDlcHWMswFmFe678zd0lUjFETia80NQhyQcVnGDlKgKPcRGyw/132" width="30px"><span>JingZ</span> 👍（0） 💬（1）<div># EM算法
全部特征值
[20 11  9 27  5  5  0  9  6  2 16 22 27 11 25 16 24  6  5 14  7 14 13 14
 14 14 13 18 21  8 11  8 28 21  8  8 21 23  1 11 28 21 21  8  8 28 22  1
 11 21 10  4 17  3  3 20 12  4 26  5 12 17 19 20 15  4 29  4 18]
23.16819127214688

聚类个数=3
[0 0 1 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 2 2 2 2 2 2 2 2 2 2 2 0 2 2 2 2 2 2
 2 0 2 2 2 2 2 2 2 0 0 0 2 1 0 1 0 0 0 0 0 2 1 0 1 1 0 1 2 2 0 2]
22.91192979526994

聚类个数=30
[10  1  9  8  2  2  6  9  8 27  4  5  8  1 19  4 25  8 12  3 23 17  3 17
 17 17  3 11  0 13  1 18 18  0 13 18  0  7 20 22 22  0  0 18  0 22  5 20
  5  0 28 14 12 24 24 10 10 26 21  2 10 29 15 10 16 26 26 10 11]
21.034625759895164</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（0） 💬（1）<div>1、用全部的特征值矩阵进行聚类训练
[12 17  9 13  1  1 15  9  3 27 18 24 13 17 14 18 12  3  1  5 23 11  5 11
 11 11  5 22  7 26 17  7 21  7 26  7  7  4  0 28 21  7  7  7  7 28 24  0
 17  7 25  2  8 19 19 12 10  2 20  1 10  8 16 12  6  2 29  2 22]
23.195087563465346

2、依然用王者荣耀英雄数据集，
1）聚类个数为 3 以及
[1 1 2 1 2 2 2 2 1 1 1 1 1 1 1 1 1 1 2 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0
 0 1 0 0 0 0 0 0 0 1 1 1 0 2 1 2 1 1 1 1 1 0 2 1 2 2 1 2 0 0 1 0]
聚类结果评估：22.91192979526994

2）聚类个数为 30 
[20 12  9 16  3  3 18  9  6 20 15  4 16 28 26 15  0  6 23 14  7  5 14  5
  5  5 14 24 10 29 28 10 10 10 29 10  1 21 25 19 10  1 10 10 10 19  4 25
  4 10  8  2 23 17 17 20  2 12 19  3  2 11 13 20 22 27 27 12 24]
聚类结果评估：21.300387287083122</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/53/60fe31fb.jpg" width="30px"><span>深白浅黑</span> 👍（0） 💬（1）<div>全部特征
聚类个数为3：
[2 2 0 2 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 1 1 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1
 1 1 2 1 1 1 1 1 1 2 1 2 1 0 2 0 1 1 2 2 2 1 0 2 0 0 2 0 1 1 2 1]
34.46996086536748
聚类个数为30：
[22 23 11 16  1  1 25 11  2  7  9  7 16 24 28  9 14  2  1  4  5  4 20  4
  4  4 20 27  0  8 23  0 26  0  8  0  0 17 15 10 26  0  0 26  0 10 29 15
  7  0  6  3 12 13 13 22 22 23 18  1 22 12 21 22 19  3  3 23 27]
25.04467629288216</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（28） 💬（2）<div>有一个疑惑，在数据规范化的时候，为何Z-Score进行规范化，而不是Min-Max进行规范化，虽然最后的结果是差不多的。
请问在数据规范化时，何时用Z-Score进行规范化，何时是Min-Max</div>2019-02-24</li><br/><li><img src="" width="30px"><span>iamtalent123</span> 👍（12） 💬（0）<div>老师，请问有没有什么方法在得到相关性系数后，自动筛选出不太相关的特征呢？在特征比较多的时候，自己一个一个的看是不是有点太费时了？</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/25/bb/20c876ce.jpg" width="30px"><span>Frank</span> 👍（8） 💬（0）<div>老师，covariance_type这个参数，什么情况下选择什么类型，能不能再说的详细点儿呢？</div>2019-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（8） 💬（0）<div>思考：为什么分类越少，反而指标分数越高，分类效果越好？
总样本过少，分成的类越多，每个类的所拥有的个体相对越少，类中个体差异变大，导致指标分数变低
为3个
[2 2 1 2 1 1 1 1 2 2 2 2 2 0 2 2 2 2 1 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 2 0 2 0 1 0 1 0 0 2 2 0 0 1 2 1 1 2 1 0 0 0 0]
34.74970397246901

为30
[ 1 20  5 13 26 15 14  5  8 20 16 20 13  0 22 16 19 22 26 10  6  4 10  4
  4  4 10 12  3 27  0 27 29  3 27  3  3 24 27 18 29  3  3 27  3 18 20 27
 20  3 21 11  2 23 23  1 28 11 25 26 28  2 17  1  9 11 11  7 12]
24.220124542171177</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d4/47/6d9f2da6.jpg" width="30px"><span>Miracle</span> 👍（6） 💬（1）<div>老师，我有一个疑惑，  这个EM算法算硬币的那个看明白了，但是放到一个具体的项目里面，很好奇究竟是怎么聚类的呢？   比如就拿上面这个王者荣耀英雄聚类来讲，我们给的输入是好多条数据，然后我假设聚成3类。 那么这里的隐藏变量是啥？  E步和M步又都是怎么操作的啊？  能不能讲讲这个流程啊？    </div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a9/32/eb71b457.jpg" width="30px"><span>Grandia_Z</span> 👍（5） 💬（1）<div>画热力图时 为什么没有“最大攻速”和“攻击范围”这两项</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8e/0a/31ec5392.jpg" width="30px"><span>挠头侠</span> 👍（2） 💬（0）<div>老师能否说明一下不同的协方差类型会带来一个什么样的效果呢？</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（2） 💬（0）<div>跑案例提示如下，请问老师怎么破？谢谢。

SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: http:&#47;&#47;pandas.pydata.org&#47;pandas-docs&#47;stable&#47;indexing.html#indexing-view-versus-copy
  data[u&#39;最大攻速&#39;] = data[u&#39;最大攻速&#39;].apply(lambda x: float(x.strip(&#39;%&#39;)) &#47; 100)
E:\DevelopTool\Python\Python27\lib\site-packages\pandas\core\indexes\base.py:3259: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
  indexer = self._engine.get_indexer(target._ndarray_values)
G:&#47;Program&#47;python&#47;Geekbang&#47;DataAnalysis&#47;Part01&#47;Lesson29&#47;01_GMM.py:31: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: http:&#47;&#47;pandas.pydata.org&#47;pandas-docs&#47;stable&#47;indexing.html#indexing-view-versus-copy
  data[u&#39;攻击范围&#39;] = data[u&#39;攻击范围&#39;].map({&#39;远程&#39;: 1, &#39;近战&#39;: 0})
E:\DevelopTool\Python\Python27\lib\site-packages\sklearn\preprocessing\data.py:625: DataConversionWarning: Data with input dtype int64, float64 were all converted to float64 by StandardScaler.
  return self.partial_fit(X, y)
E:\DevelopTool\Python\Python27\lib\site-packages\sklearn\utils\extmath.py:776: RuntimeWarning: invalid value encountered in true_divide
  updated_mean = (last_sum + new_sum) &#47; updated_sample_count
...
Traceback (most recent call last):
  ...
ValueError: Input contains NaN, infinity or a value too large for dtype(&#39;float64&#39;).</div>2019-03-01</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>出现两个问题：
一、发生异常: ValueError could not convert string to float: &#39;近战&#39; File &quot;D:\EM_data-master\here_em.py&quot;, line 21, in &lt;module&gt; corr = data[features].corr() ^^^^^^^^^^^^^^^^^^^^^ ValueError: could not convert string to float: &#39;近战&#39;
解决：在尝试计算数据帧（DataFrame）中特征之间的相关性时，使用了corr()方法。这个方法默认情况下只能在数值型数据上进行计算，无法处理字符串类型的数据。为了解决这个问题，需要确保所有参与相关性计算的特征都是数值型数据。为此需要在代码中　“　corr = data[features].corr()　”　前，增加两行实现的：
data[u&#39;最大攻速&#39;] = data[u&#39;最大攻速&#39;].apply(lambda x: float(x.strip(&#39;%&#39;))&#47;100)
data[u&#39;攻击范围&#39;]=data[u&#39;攻击范围&#39;].map({&#39;远程&#39;:1,&#39;近战&#39;:0})

二、发生异常: ImportError cannot import name &#39;calinski_harabaz_score&#39; from &#39;sklearn.metrics&#39; (c:\Python311\Lib\site-packages\sklearn\metrics\__init__.py) File &quot;D:\EM_data-master\here_em1.py&quot;, line 49, in &lt;module&gt; from sklearn.metrics import calinski_harabaz_score ImportError: cannot import name &#39;calinski_harabaz_score&#39; from &#39;sklearn.metrics&#39; (c:\Python311\Lib\site-packages\sklearn\metrics\__init__.py)
这个问题的原因是在较新版本的scikit-learn中，calinski_harabaz_score已经被重命名为calinski_harabasz_score。因此，正确的导入方式应该是从sklearn.metrics导入calinski_harabasz_score。为了解决这个问题，安装更新最新scikit-learn版本，
将代码：
from sklearn.metrics import calinski_harabaz_score
print(calinski_harabaz_score(data, prediction))
改为：
from sklearn.metrics import calinski_harabasz_score
print(calinski_harabasz_score(data, prediction))</div>2024-04-11</li><br/><li><img src="" width="30px"><span>Geek_e888b2</span> 👍（1） 💬（0）<div>最后.insert()和.to_scv()括号里面怎么理解？</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/aa/d1/076482f3.jpg" width="30px"><span>白夜</span> 👍（1） 💬（1）<div>这个相关性的计算原理能扩展讲讲吗？蛮好奇的</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/86/79/066a062a.jpg" width="30px"><span>非同凡想</span> 👍（0） 💬（0）<div>1.全部特征 30个聚类
[25 13  8  5  1  1 21  8 12 13  2 13  5  4 28  2 15 12  1 24 18  9 24  9
  9  9 24 22  6  6  4  6  6  6  6  6  6  7 23  0  6  6  6  6  6  0 27 23
 13  6 16 26  1  3  3 25 11 26 14  1 11 10 17 25 20 26 19 29 22]
23.507078366657264

2.全部特征 3个聚类
[2 2 1 2 1 1 1 1 2 2 2 2 2 0 2 2 2 2 1 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 2 0 2 0 1 0 1 0 0 2 2 0 0 1 2 1 1 2 1 0 0 0 0]
34.74970397246901

3. 12个特征，30个聚类
[ 9 19  5 12  3  3 23 29 12  1  7 19 12  6 20  7 28 12  3  2 17  2  2  2
  2  2  2  0 21 26  6 21  4 21 26 21 21 10 14 11  4 21 21  4 21 11 19 14
 19 21 27 13  8 16 16  9 25 19 24  3 25  8 15  9 18 13 13 22  0]
20.931148834796

4.12个特征，3个聚类
[0 0 1 1 1 1 2 1 1 0 1 0 1 0 1 1 0 1 1 2 2 2 2 2 2 2 2 2 2 2 0 2 2 2 2 2 2
 2 0 2 2 2 2 2 2 2 0 0 0 2 0 0 0 0 0 0 0 0 2 1 0 0 0 0 0 0 0 0 2]
20.773369734506527</div>2020-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（0） 💬（0）<div>交作业：
https:&#47;&#47;github.com&#47;LearningChanging&#47;Data-analysis-in-action&#47;tree&#47;master&#47;29-EM%E8%81%9A%E7%B1%BB%EF%BC%88%E4%B8%8B%EF%BC%89%EF%BC%9A%E7%94%A8EM%E7%AE%97%E6%B3%95%E5%AF%B9%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80%E8%8B%B1%E9%9B%84%E8%BF%9B%E8%A1%8C%E5%88%92%E5%88%86</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（0） 💬（0）<div>为什么分类越少，反而指标分数越高，分类效果越好？
总样本过少，分成的类越多，每个类的所拥有的个体相对越少，类中个体差异变大，导致指标分数变低</div>2019-04-05</li><br/>
</ul>