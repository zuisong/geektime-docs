你好，我是Barry。

上节课，我们主要学习了Python基础的数据类型和脚本语言，通过大量的API和案例应用，相信你对Python的基础部分已经有了较全面的了解。

但是，如果我们想要进一步地应用Python，只懂得基础部分是不够的，例如，如果我们想应用Python做数据分析应该如何实现呢？要实现文化社区视频平台，又该掌握Python的哪些技术点呢？

这节课我们就一起来学习Python的高阶应用，相信你已经迫不及待了。Python的高阶应用主要包括数据分析和项目开发两部分，我们先来看数据分析。

## Python数据分析

因为 Python 是数据科学家发明的，所以用它来处理数学计算和数据分析是非常高效且方便的。它可以帮助我们优化工作效率，也能让我们更理性地做业务决策，应用场景非常多。要入门数据分析，就少不了数据的各种操作和计算，下面我们就先来学习一个可以非常高效地处理数值型运算的库—— Numpy库。

### 认识NumPy

NumPy是一个功能非常强大的Python库，它的全称是“ Numeric Python”，主要用来计算、处理一维或多维数组。NumPy库有下面几个特点。

1. Numpy底层使用C语言编写，执行效率远高于纯Python代码。
2. 它可以很方便地处理多维数组。
3. 具有实用的线性代数、数学计算功能。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELLvDhMwfXEVicTwl5rQoCGwTibAebFqusXFDoZwQYMS3bVPkgnr4q4YicJWZkH00rOuv7DjZ7dxY6fg/132" width="30px"><span>derek</span> 👍（1） 💬（1）<div>为什么不用fastapi呢？</div>2023-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（1） 💬（1）<div># 使用 matplotlib 画一个饼图
import numpy as np
import matplotlib.pyplot as plt


data = np.array([10, 20, 30, 40, 50])
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.pie(
		data,
		labels = [&quot;one&quot;, &quot;two&quot;, &quot;three&quot;, &quot;four&quot;, &quot;five&quot;],  # 设置5个图例标志
		colors = [&quot;b&quot;, &quot;g&quot;, &quot;c&quot;, &quot;m&quot;, &quot;y&quot;]  # 设置5个颜色
	)
ax.set_title(&quot;Pie&quot;)
plt.legend(loc=&quot;upper left&quot;)  # 图例位置放置左上方
plt.show()</div>2023-05-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyn6s0CNx9FiclaibWOmxWia4GKPScuEoL2TfTBnLvC1KThqjg61c5S8jF0OLDqx1VjpcI4Sk1icE5cg/132" width="30px"><span>Geek_团子</span> 👍（1） 💬（1）<div>啥是mvt？</div>2023-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（1）<div>第2讲打卡~
通过这节课，领略了Python在数据分析领域的强大能力~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/f5/72/8cbc5cb3.jpg" width="30px"><span>好困啊</span> 👍（0） 💬（1）<div># 饼状图
# 数据
sizes = [15, 30, 45, 10]
labels = [&#39;Frogs&#39;, &#39;Hogs&#39;, &#39;Dogs&#39;, &#39;Logs&#39;]

# 绘制饼状图
plt.pie(sizes, labels=labels, autopct=&#39;%1.1f%%&#39;, shadow=False, startangle=90)

# 设置标题
plt.title(&#39;Pie&#39;)

# 使饼状图为正圆形
plt.axis(&#39;equal&#39;)

# 显示图形
plt.show()</div>2023-08-19</li><br/><li><img src="" width="30px"><span>Geek_e5f033</span> 👍（0） 💬（2）<div>老师有一个问题,经常在网上看到一些python代码,拿来用时,就会发现有好多问题,不是这个库没有装,就是那个库版本不对,作为一个开发者,我们怎样才能根据代码,安装正确的库呢?</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d7/03/db060811.jpg" width="30px"><span>Geek_gong1zu</span> 👍（0） 💬（1）<div>import matplotlib.pyplot as plt
# 设置画布
plt.rcParams[&#39;font.sans-serif&#39;] =&#39;SimHei&#39;
plt.figure(figsize=(6, 6))
label = [&#39;第一产业&#39;, &#39;第二产业 &#39;, &#39;第三产业&#39;]
explode = [0.01, 0.01, 0.01]

values = [4, 6, 7]
plt.pie(values, explode=explode, labels=label, autopct=&#39;%1.1f&#39;)
plt.title(&quot;经济结构&quot;)
plt.savefig(&#39;.&#47;经济结构饼图&#39;)
plt.show()
图片无法上传</div>2023-05-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDqHQQByGiaXcAk94MdDn3ftupZLXyR6bAKibxOzMxy5h3uBwZ7QiaCiaIfbCMK0cIQfGNax8iawoiaQAg/132" width="30px"><span>nuan</span> 👍（0） 💬（6）<div>请问老师，我复制了柱状图和散点图的代码，执行后不显示数轴上的刻度，也不显示lable以及title。
会是什么原因呢？
我的运行环境是：ubuntu 22.04，Python 3.10.6，matplotlib 3.7.1</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（3）<div>请教老师几个问题：
Q1: 本专栏后端开发的python是什么？win10下用PyCharm吗？（被开源软件的开发环境折磨过几次，有点小害怕；学习时间不多，碰上几个环境问题就感觉要崩溃）

Q2: 本专栏的源码放哪里？

Q3: 我笔记本是win10，装了Anaconda。但是，Anaconda不能运行python命令
Win10，开始菜单中运行”Anaconda Powershell prompt”，弹出一个命令行窗口，命令提示符前面是“(base) PS C:\Users\Administrator&gt;”，操作如下：
1 输入: 5+4，显示9. 
2 输入:print(“hello”), 提示“无法初始化设备 PRN”；
3 输入：a+=10，回车后提示：a+=10 : 无法将“a+=10”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。
为什么？</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>快更！</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/88/3814fea5.jpg" width="30px"><span>安静点</span> 👍（0） 💬（1）<div>期待更新！</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/04/3c/9f97f7bd.jpg" width="30px"><span>一米</span> 👍（0） 💬（1）<div>1.numpy数组与python列表性能对比处 应该有两处勘误
# 1.1应该引入time 
# 1.2原代码第9行使用的变量应该是d
import numpy as np
#import time

time1 = time.time()
array = []
for d in range(100000):
    array.append(x**2)
    # array.append(d**2)
time2 = time.time()
use_time = time2 - time1
print(use_time)

time3 = time.time()
n = np.arange(100000)**2
time4 = time.time()
print(time4-time3)

2.django应该是采用MTV模式吧

3.思考题
from matplotlib import pyplot as plt

#添加图形对象
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])

#准备数据
langs = [&#39;football&#39;, &#39;tennis&#39;, &#39;basketball&#39;, &#39;ping-pong&#39;, &#39;volleyball&#39;]
students = [23,17,35,29,12]
#绘制饼状图
ax.pie(students, labels = langs,autopct=&#39;%.2f%%&#39;)
plt.show()</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/03/c5/b3364e49.jpg" width="30px"><span>佩慎斯予氪蕾沐</span> 👍（0） 💬（1）<div>大二的时候因为期末考试会用Python画各种图，现在过了一年全部还给老师了😂😂</div>2023-04-26</li><br/>
</ul>