今天我来给你讲讲Python的可视化技术。

如果你想要用Python进行数据分析，就需要在项目初期开始进行探索性的数据分析，这样方便你对数据有一定的了解。其中最直观的就是采用数据可视化技术，这样，数据不仅一目了然，而且更容易被解读。同样在数据分析得到结果之后，我们还需要用到可视化技术，把最终的结果呈现出来。

## 可视化视图都有哪些？

按照数据之间的关系，我们可以把可视化视图划分为4类，它们分别是比较、联系、构成和分布。我来简单介绍下这四种关系的特点：

1. 比较：比较数据间各类别的关系，或者是它们随着时间的变化趋势，比如折线图；
2. 联系：查看两个或两个以上变量之间的关系，比如散点图；
3. 构成：每个部分占整体的百分比，或者是随着时间的百分比变化，比如饼图；
4. 分布：关注单个变量，或者多个变量的分布情况，比如直方图。

同样，按照变量的个数，我们可以把可视化视图划分为单变量分析和多变量分析。

单变量分析指的是一次只关注一个变量。比如我们只关注“身高”这个变量，来看身高的取值分布，而暂时忽略其他变量。

多变量分析可以让你在一张图上可以查看两个以上变量的关系。比如“身高”和“年龄”，你可以理解是同一个人的两个参数，这样在同一张图中可以看到每个人的“身高”和“年龄”的取值，从而分析出来这两个变量之间是否存在某种联系。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（14） 💬（4）<div>思考题1：对车祸数据成对关系的的探索，程序代码如下：

#车祸数据分析
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# 数据准备
crashes = sns.load_dataset(&#39;car_crashes&#39;)
crashes_data = pd.DataFrame(crashes)

# 用 Seaborn 画成对关系
sns.pairplot(crashes)
plt.show()

思考题2：模拟企业隐患数据分析，代码如下：

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#定义生成隐患数量函数
def GenerateHDNum(hdtimes):
    #hdtimes表示要生成多少隐患数量
    HD_NumList = list(pd.Series(np.random.rand(hdtimes)))
    return [int(x * 100) for x in HD_NumList]

#数据准备函数
def MakeData():

    #创建以月份为单位的时间索引
    dti = pd.date_range(start=&#39;2017-01-01&#39;, end=&#39;2018-12-31&#39;, freq=&#39;M&#39;)
    monthlist = [str(x * 100 + y) for x,y in zip(dti.year,dti.month)]
    
    hdtimes = len(monthlist)
    #生成各种隐患数量
    NormalHD = GenerateHDNum(hdtimes)
    ImportHD = GenerateHDNum(hdtimes)
    HDNum = { &#39;Normal&#39;: NormalHD
             ,&#39;Import&#39;: ImportHD}

    HD_Frame = pd.DataFrame(data = HDNum, index=monthlist)

    print(HD_Frame)
    return HD_Frame

def AnalyData(HDSet,AnalyType=&#39;0&#39;):

    #AnalyType取值：1：成对关系图；2：散点图；3：核密度图；4：Hexbin图

    #成对关系图
    if AnalyType == &#39;1&#39;:
        sns.pairplot(HDSet)

    #散点图
    if AnalyType == &#39;2&#39;:
        sns.jointplot(x=&#39;Normal&#39;, y=&#39;Import&#39;, data=HDSet, kind=&#39;scatter&#39;)

    #核密度图
    if AnalyType == &#39;3&#39;:
        sns.jointplot(x=&#39;Normal&#39;, y=&#39;Import&#39;, data=HDSet, kind=&#39;kde&#39;)

    #Hexbin图
    if AnalyType == &#39;4&#39;:
        sns.jointplot(x=&#39;Normal&#39;, y=&#39;Import&#39;, data=HDSet, kind=&#39;hex&#39;)
    
    plt.show()

def ShowMenu():
    print(&#39;=&#39;*20)
    print(&#39;1.显示成对关系图&#39;)
    print(&#39;2.显示散点图&#39;)
    print(&#39;3.显示核密度图&#39;)
    print(&#39;4.显示Hexbin图&#39;)
    print(&#39;R.换一批数据&#39;)
    print(&#39;0.退出&#39;)
    print(&#39;=&#39;*20)
    return input(&#39;请输入命令:&#39;)

def main():

    HDSet = MakeData()
    while True:
        command = ShowMenu()

        if command == &#39;0&#39;:
            break
        elif command == &#39;R&#39;:
            HDSet = MakeData()
        else:
            AnalyData(HDSet, command)

main()</div>2019-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yYzf0yonEqKny7dHlvLibc7OrQJ6HszX3VP1fciaMD3hITFySbayL9vULch5hvicoqGA2EBzcPicss2ciaB7ibodgQ6w/132" width="30px"><span>sxpujs</span> 👍（9） 💬（1）<div>在 Mac 下设置中文字体，可以使用以下路径：
# 设置中文字体
font = FontProperties(fname=&quot;&#47;System&#47;Library&#47;Fonts&#47;STHeiti Medium.ttc&quot;, size=14)</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e5/43/7bc7cfe3.jpg" width="30px"><span>跳跳</span> 👍（4） 💬（1）<div>第一题：seaborn car_crashes成对关系探索
iris=sns.load_dataset(&quot;car_crashes&quot;)
sns.pairplot(iris)
plt.show()
第二题：由第一题可以看出酒精和速度由类似线性关系，因此做酒精和速度二元变量的分布图
iris=sns.load_dataset(&quot;car_crashes&quot;)
print(iris.head(10))
sns.jointplot(x=&#39;alcohol&#39;,y=&#39;speeding&#39;,data=iris,kind=&#39;scatter&#39;)
sns.jointplot(x=&#39;alcohol&#39;,y=&#39;speeding&#39;,data=iris,kind=&#39;kde&#39;)
sns.jointplot(x=&#39;alcohol&#39;,y=&#39;speeding&#39;,data=iris,kind=&#39;hex&#39;)
碎碎念一下：为啥留言不支持图片？难受</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/ef/23/1f192e21.jpg" width="30px"><span>jion</span> 👍（3） 💬（1）<div>你好，练习成对关系图时，除下如下错误，是何原因？
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
# 数据准备
iris_datas = datasets.load_iris()
iris = pd.DataFrame(iris_datas.data, columns=[&#39;SpealLength&#39;, &#39;Spealwidth&#39;, &#39;PetalLength&#39;, &#39;PetalLength&#39;])
print(iris.shape,&quot;\n&quot;,iris)
# 用Seaborn画成对关系
sns.pairplot(iris)
出现如下错误：ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().</div>2021-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f9/ce/4985c6fc.jpg" width="30px"><span>求知鸟</span> 👍（3） 💬（3）<div>python在慢慢追赶R，我的R语言分析水平停止了，python水平在往上涨，现在的状态是，有老师的课就学课，没有就看《精益数据分析》。
</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/88/4c/2c3d2c7d.jpg" width="30px"><span>小强</span> 👍（2） 💬（2）<div>各种场景的视图，试用什么场景，怎么分析，例子太少了，理解不够深。</div>2020-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3c/a2/09a2215c.jpg" width="30px"><span>夕子</span> 👍（1） 💬（1）<div>car_crashes = sns.load_dataset(&#39;car_crashes&#39;)
car_crashes.head(10)

# 成对关系探索
sns.pairplot(car_crashes)
plt.show()

# 画散点图
sns.jointplot(x = &#39;speeding&#39;, y = &#39;total&#39;, data = car_crashes, kind = &#39;scatter&#39;)
plt.show()

# 画核密度图
sns.jointplot(x = &#39;speeding&#39;, y = &#39;total&#39;, data = car_crashes, kind = &#39;kde&#39;)
plt.show()

# 画hexbin图
sns.jointplot(x = &#39;speeding&#39;, y = &#39;total&#39;, data = car_crashes, kind = &#39;hex&#39;)
plt.show()</div>2021-03-18</li><br/><li><img src="" width="30px"><span>丁思森</span> 👍（1） 💬（2）<div>请问一下，有人在运行sns.load_dataset(&#39;tips&#39;),遇到报错urllib.error.URLError: &lt;urlopen error [Errno 11004] getaddrinfo failed&gt;么？这里直接加载数据集会报错，你们是怎么解决的？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a1/d6/1407001c.jpg" width="30px"><span>毛毛🐛虫🌻</span> 👍（1） 💬（2）<div>热力图那个是颜色越浅，值越大么？</div>2019-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a9/a7/de3ee890.jpg" width="30px"><span>拉我吃</span> 👍（1） 💬（1）<div># coding:utf-8
import matplotlib.pyplot as plt
import seaborn as sns

# Data Prep
car_crashes = sns.load_dataset(&#39;car_crashes&#39;)
sns.pairplot(car_crashes)
plt.show()

# plot with seaborn (scatter, kde, hex)
sns.jointplot(x=&#39;alcohol&#39;, y=&#39;speeding&#39;, data=car_crashes, kind=&#39;scatter&#39;)
sns.jointplot(x=&#39;alcohol&#39;, y=&#39;speeding&#39;, data=car_crashes, kind=&#39;kde&#39;)
sns.jointplot(x=&#39;alcohol&#39;, y=&#39;speeding&#39;, data=car_crashes, kind=&#39;hex&#39;)
plt.show()

二元关系选了喝酒和超速的对比，基本上在大部分区间下是线性关系，就是喝得多速度快:)</div>2019-01-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/u4OemUpkKSvWIo55u5MfCXKEEdAJCdJjUWpibk4wxXavqo6CBscrbRgpxffsbAklLKggmX7B2cNxzbdQ5W8Orlg/132" width="30px"><span>陶铖</span> 👍（0） 💬（1）<div>持续学习中，受益匪浅！</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d1/af/49b0b4ee.jpg" width="30px"><span>Dorothy</span> 👍（0） 💬（1）<div>运行sns.load_dataset()的时候遇到这个问题：
URLError: &lt;urlopen error [Errno 61] Connection refused&gt; 请问大家有解决办法吗？</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0c/2c/e905e970.jpg" width="30px"><span>如果</span> 👍（0） 💬（1）<div>麻烦问下，seaborn数据集导入报错，在网上查了资料以后加入ssl认证，还是报错，怎么解决的</div>2020-04-18</li><br/><li><img src="" width="30px"><span>十六。</span> 👍（0） 💬（1）<div>import matplotlib.pyplot as plt
import seaborn as sns
# 数据准备
crashes = sns.load_dataset(&quot;car_crashes&quot;)
sns.pairplot(crashes)
plt.show()</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/cb/cffd466b.jpg" width="30px"><span>王辉</span> 👍（0） 💬（2）<div>老师我一点基础都没有 感觉听这个像天书</div>2020-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ba/6d318c08.jpg" width="30px"><span>GS</span> 👍（0） 💬（1）<div>奉上我的笔记  https:&#47;&#47;github.com&#47;leledada&#47;jupyter&#47;blob&#47;master&#47;matplotlibDemo.ipynb</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ba/6d318c08.jpg" width="30px"><span>GS</span> 👍（0） 💬（1）<div>遇到个问题：&#39;module&#39; object has no attribute &#39;lineplot&#39;. 
https:&#47;&#47;stackoverflow.com&#47;questions&#47;51846948&#47;seaborn-lineplot-module-object-has-no-attribute-lineplot
解决方案：
pip install seaborn==0.9.0</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a2/bf/4998c844.jpg" width="30px"><span>Geek_592dcb</span> 👍（0） 💬（1）<div>可以把三维图、曲面图加上，这两个非常重要，用的也比较多</div>2019-07-22</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIc88LLmwU7RU1tGcmo5OZyPibKeXPg31wMxyc2uByEO3g44f6uLcu1bXGNO9AHVgn0PK5hwkcfYZA/132" width="30px"><span>董大琳儿</span> 👍（0） 💬（1）<div>import matplotlib.pyplot as plt
import seaborn as sns
# 数据准备
iris = sns.load_dataset(&#39;iris&#39;)
# 用 Seaborn 画成对关系
sns.pairplot(iris)
plt.show()
</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（0） 💬（1）<div>语言Python3.6， 环境IDLE
&gt;&gt;&gt; car_crashes = sns.load_dataset(&#39;car_crashes&#39;)
第一个问题：
&gt;&gt;&gt; sns.pairplot(car_crashes)
&lt;seaborn.axisgrid.PairGrid object at 0x125a9cdd8&gt;
第二个问题：查看获取到的数据维度，针对车祸数与速度画二元变量分布图，以及针对车祸数与酒精含量画二元变量分布图
&gt;&gt;&gt; sns.jointplot(x=&#39;total&#39;,y=&#39;speeding&#39;,data=car_crashes,kind=&#39;scatter&#39;)
&lt;seaborn.axisgrid.JointGrid object at 0x1259d7d68&gt;
&gt;&gt;&gt; sns.jointplot(x=&#39;total&#39;,y=&#39;speeding&#39;,data=car_crashes,kind=&#39;kde&#39;)
&lt;seaborn.axisgrid.JointGrid object at 0x129fe9ba8&gt;
&gt;&gt;&gt; sns.jointplot(x=&#39;total&#39;,y=&#39;speeding&#39;,data=car_crashes,kind=&#39;hex&#39;)
&lt;seaborn.axisgrid.JointGrid object at 0x12ff26eb8&gt;
&gt;&gt;&gt; sns.jointplot(x=&#39;total&#39;,y=&#39;alcohol&#39;,data=car_crashes,kind=&#39;scatter&#39;)
&lt;seaborn.axisgrid.JointGrid object at 0x131b19550&gt;
&gt;&gt;&gt; sns.jointplot(x=&#39;total&#39;,y=&#39;alcohol&#39;,data=car_crashes,kind=&#39;kde&#39;)
&lt;seaborn.axisgrid.JointGrid object at 0x129f5a630&gt;
&gt;&gt;&gt; sns.jointplot(x=&#39;total&#39;,y=&#39;alcohol&#39;,data=car_crashes,kind=&#39;hex&#39;)
&lt;seaborn.axisgrid.JointGrid object at 0x12605c630&gt;
&gt;&gt;&gt; plt.show()

最后执行一次plt.show() 所创建的图片都会显示出来</div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/67/681dcf02.jpg" width="30px"><span>Y2Y</span> 👍（0） 💬（1）<div>为什么sns画图操作之后也要plt.show()一下呢？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5a/94/1d064846.jpg" width="30px"><span>靳学佳</span> 👍（0） 💬（1）<div>老师很全面 就是很深 我零基础</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/de/5c67895a.jpg" width="30px"><span>周飞</span> 👍（0） 💬（1）<div>1.车祸数据集的成对关系：
import matplotlib.pyplot as plt
import seaborn as sns
# 数据准备
car_crash = sns.load_dataset(&#39;car_crashes&#39;)
# 用 Seaborn 画成对关系
sns.pairplot(car_crash)
plt.show()
2.seaborn 画二元变量分布图：
# 用 Seaborn 画二元变量分布图（散点图，核密度图，Hexbin 图）
sns.jointplot(x=&quot;total_bill&quot;, y=&quot;tip&quot;, data=tips, kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total_bill&quot;, y=&quot;tip&quot;, data=tips, kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total_bill&quot;, y=&quot;tip&quot;, data=tips, kind=&#39;hex&#39;)
plt.show()

</div>2019-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnryDfaYkQh7mTgVIQqk4vdeuY2oa82w0yxOVNfsz4qfSMqEqPFE9gKFvlhS53xY6YOrib86Z6vPA/132" width="30px"><span>Lambert</span> 👍（0） 💬（1）<div>第一题答案
import matplotlib.pyplot as plt
import seaborn as sns
car_crashes = sns.load_dataset(&#39;car_crashes&#39;)
sns.pairplot(car_crashes)
plt.show()

第二题答案
import matplotlib.pyplot as plt
import seaborn as sns
car_crashes = sns.load_dataset(&quot;car_crashes&quot;)
print(car_crashes.head(10))
sns.jointplot(x=&quot;total&quot;, y=&quot;speeding&quot;, data=car_crashes, kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;speeding&quot;, data=car_crashes, kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;speeding&quot;, data=car_crashes, kind=&#39;hex&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;alcohol&quot;, data=car_crashes, kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;alcohol&quot;, data=car_crashes, kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;alcohol&quot;, data=car_crashes, kind=&#39;hex&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;not_distracted&quot;, data=car_crashes, kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;not_distracted&quot;, data=car_crashes, kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;not_distracted&quot;, data=car_crashes, kind=&#39;hex&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;no_previous&quot;, data=car_crashes, kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;no_previous&quot;, data=car_crashes, kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;no_previous&quot;, data=car_crashes, kind=&#39;hex&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;ins_premium&quot;, data=car_crashes, kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;ins_premium&quot;, data=car_crashes, kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;ins_premium&quot;, data=car_crashes, kind=&#39;hex&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;ins_losses&quot;, data=car_crashes, kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;ins_losses&quot;, data=car_crashes, kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;ins_losses&quot;, data=car_crashes, kind=&#39;hex&#39;)
plt.show()</div>2019-02-21</li><br/><li><img src="" width="30px"><span>xiaoyu0309</span> 👍（0） 💬（1）<div>#第15课作业,微信：xiaoyu41102126
import matplotlib.pyplot as plt
import seaborn as sns
# 数据准备
data = sns.load_dataset(&#39;car_crashes&#39;)
print(data.head(20))
sns.pairplot(data)
sns.jointplot(x=&quot;total&quot;, y=&quot;speeding&quot;, data=data, kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;speeding&quot;, data=data, kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total&quot;, y=&quot;speeding&quot;, data=data, kind=&#39;hex&#39;)
plt.show()</div>2019-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erBSoNm28CNCYpvytDbhfSYpgCo6T9vuzKkSoflr3sX8VucMz8ykrichKDY9vVoMVomUIakXSQq9icw/132" width="30px"><span>xfoolin</span> 👍（0） 💬（1）<div>一、
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#准备数据
car_crashes = sns.load_dataset(&#39;car_crashes&#39;)
#探索成对关系
sns.pairplot(car_crashes)
plt.show()

二、
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#准备数据
car_crashes = sns.load_dataset(&#39;car_crashes&#39;)
print(car_crashes.head(5))
df = pd.DataFrame({&#39;x&#39;:car_crashes[&#39;total&#39;],&#39;y&#39;:car_crashes[&#39;alcohol&#39;]})
#画散点图
sns.jointplot(x = &#39;x&#39;,y = &#39;y&#39;,data = df,kind = &#39;scatter&#39;)
#画核密度图
sns.jointplot(x = &#39;x&#39;,y = &#39;y&#39;,data = df,kind  = &#39;kde&#39;)
#画hexbin图
sns.jointplot(x = &#39;x&#39;,y = &#39;y&#39;,data = df,kind = &#39;hex&#39;)
plt.show()</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（0） 💬（1）<div>使用mac的同学，在加载中文字体时，路径可使用
font=FontProperties(fname=&#39;&#47;Library&#47;Fonts&#47;Songti.ttc&#39;,size=14)</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（0） 💬（1）<div>作业：
通过成对关系探索，发现total和no_previous成线性关系，在二元变量分布选取该俩变量
# 探索car_crashes数据集的成对关系
# 成对关系
import matplotlib.pyplot as plt
import seaborn as sns
# 数据准备
crashes=sns.load_dataset(&#39;car_crashes&#39;)
print(crashes.head(10))

#用seaborn画成对关系
sns.pairplot(crashes)
plt.show()

# 二元变量分布
# 用seaborn画二元变量分布图（散点图，核密度图，hexbin图）
sns.jointplot(x=&quot;total&quot;,y=&quot;no_previous&quot;,data=crashes,kind=&#39;scatter&#39;)
sns.jointplot(x=&quot;total&quot;,y=&quot;no_previous&quot;,data=crashes,kind=&#39;kde&#39;)
sns.jointplot(x=&quot;total&quot;,y=&quot;no_previous&quot;,data=crashes,kind=&#39;hex&#39;)
plt.show()</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/e2/3640e491.jpg" width="30px"><span>小熊猫</span> 👍（0） 💬（1）<div>import matplotlib.pyplot as plt
import seaborn as sns

car_crashes = sns.load_dataset(&#39;car_crashes&#39;)
car_crashes.head()
# 成对关系
sns.pairplot(car_crashes)
# 二元变量
sns.jointplot(x=&#39;alcohol&#39;, y=&#39;speeding&#39;, data=car_crashes, kind=&#39;scatter&#39;)
sns.jointplot(x=&#39;alcohol&#39;, y=&#39;speeding&#39;, data=car_crashes, kind=&#39;kde&#39;)
sns.jointplot(x=&#39;alcohol&#39;, y=&#39;speeding&#39;, data=car_crashes, kind=&#39;hex&#39;)</div>2019-02-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI45zO9GOMquk9JymTibN9sC25Sy4WtsDGRQzIRVIoIzPnaJGKmGe3jXqxP0zKZyTYazrXHBGYjBzw/132" width="30px"><span>柚子</span> 👍（0） 💬（1）<div>1、seaborn car_crashes成对关系探索：
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
car_crashes = sns.load_dataset(&#39;car_crashes&#39;)
sns.pairplot(car_crashes)

2、以酒精和超速画二元变量分布图：
散点图：sns.jointplot(x = &#39;alcohol&#39;,y = &#39;speeding&#39;,data =car_crashes, kind = &#39;scatter&#39;)
核密度图：sns.jointplot(x = &#39;alcohol&#39;,y = &#39;speeding&#39;,data =car_crashes, kind = &#39;kde&#39;)
hexbin图：sns.jointplot(x = &#39;alcohol&#39;,y = &#39;speeding&#39;,data =car_crashes, kind = &#39;hex&#39;)</div>2019-02-13</li><br/>
</ul>