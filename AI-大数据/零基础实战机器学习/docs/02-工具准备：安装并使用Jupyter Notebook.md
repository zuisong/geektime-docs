你好，我是黄佳。

欢迎来到零基础实战机器学习。工欲善其事，必先利其器，好的环境让我们事半功倍。今天我要讲的就是怎么来搭建机器学习运行的环境。

你也许听说过机器学习项目对配置要求高，硬件上需要带GPU的显卡，软件上面需要在Server 中搭建 PyTorch 和 TensorFlow 2.0 什么的。这些东西是不是听起来就挺麻烦的。

其实没有那么复杂。我觉得对于初学者来说，你不必过于纠结上面的工具。我们只是要进行一些简单的实战项目。而这些简单的项目，在本机上完全可以跑通。所以我建议你就用你手头上的笔记本电脑，装个Jupyter Notebook就足够了。

你听到这可能会想问什么是Jupyter Notebook呀？你可以把它想象成一个类似于网页的多媒体文档，但是，比普通网页更高一筹的是，它还能直接通过浏览器运行代码块，在代码块下方展示运行结果，就像下图中这样：

![](https://static001.geekbang.org/resource/image/a3/eb/a38f6f907c83e1cbb30dec791ef265eb.png?wh=1261x792)

Jupyter Notebook可以交互式开发，再加上拥有富文本格式，可以显示图文，非常直观，所以它能迅速地展现数据分析师的想法，是我们上手机器学习的最佳工具。

选好了工具之后，我们还得确定要用什么语言。我们课程选的是Python，所有源代码都是用Python实现的。之所以选Python是因为Python在AI开发中是最常用的语言了，而且Python非常简单，只要你稍微有些编程方面的基础知识，就能看懂我们的代码。而我们推荐使用的工具Jupyter Notebook可以支持多种语言，其中就包括Python。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/02/42/e8ef9639.jpg" width="30px"><span>蝶舞清风寒</span> 👍（3） 💬（1）<div>1、 plotlPlotly工具是基于浏览器的交互工具，其绘图结果html网页文件，因此与jupter notebook更匹配；
2、若是在spyder下运行的时候，console运行时是空白；
3、若要解决spyder运行问题，需要以下步骤
import plotly.io as pio
#如果您想在浏览器中显示您的图形作为完全交互式版本
pio.renderers.default=&#39;browser&#39;
#要切换回在 Spyder 中生成图形
pio.renderers.default=&#39;svg&#39;
在脱机模式下，通过浏览器显示图形或者运行结果
详细解释需要看：https:&#47;&#47;stackoverflow.com&#47;questions&#47;35315726&#47;plotly-how-to-display-charts-in-spyder</div>2021-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/59/52a504f6.jpg" width="30px"><span>u</span> 👍（2） 💬（1）<div>import plotly.express as px
import pandas as pd

if __name__ == &#39;__main__&#39; :
    stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;]
    dataMale = dict(number=[59, 32, 18, 9, 2],stage=stages)
    dataFemale = dict(number=[29,17,8,3,1],stage=stages)

    df_male = pd.DataFrame(dataMale)
    df_male[&#39;性别&#39;] = &#39;男&#39;
    df_female = pd.DataFrame(dataFemale)
    df_female[&#39;性别&#39;] = &#39;女&#39;

    df_total = pd.concat(objs=[df_male,df_female],axis=0)
    fig = px.funnel(df_total,x=&quot;number&quot;,y=&quot;stage&quot;,color=&quot;性别&quot;)
    fig.show()</div>2021-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/77/95/0d10d4b2.jpg" width="30px"><span>茜茜</span> 👍（3） 💬（1）<div>import plotly.express as px
import pandas as pd
stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;]
df_male = pd.DataFrame(dict(number = [59,32,18,9,2], stage = stages, gender = &#39;男性&#39;))
df_female = pd.DataFrame(dict(number = [66,34,20,12,4], stage = stages, gender = &#39;女性&#39;))
df = pd.concat([df_male, df_female], axis = 0)
fig = px.funnel(df, x = &#39;number&#39;, y = &#39;stage&#39;, color = &#39;gender&#39;)
fig.show()</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/53/b4590ccc.jpg" width="30px"><span>阿文</span> 👍（0） 💬（2）<div>我这漏斗图出不来，出现了一块空白区域。这是啥情况啊</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（7） 💬（1）<div>AIK同学已经给出了正确答案，不过在实验的过程中，可以输出df_male和df数据集，看看pandas是如何合并数据集df_male和df_female，plotly.express是将什么样的数据集绘制成图形的。</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（9） 💬（1）<div>import pandas as pd 

stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;]

df_male = pd.DataFrame(dict(number=[30, 15, 10, 6, 1], stage=stages))
df_male[&#39;性别&#39;] = &#39;男&#39;

df_female = pd.DataFrame(dict(number=[29, 17, 8, 3, 1], stage=stages))
df_female[&#39;性别&#39;] = &#39;女&#39;

df = pd.concat([df_male, df_female], axis=0) 
fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;性别&#39;)

fig.show()</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9d/a9/4602808f.jpg" width="30px"><span>黄佳</span> 👍（0） 💬（1）<div>如果大家在安装Plotly包的时候遇到障碍，也可以尝试用这个语句pip install plotly==5.3.1，安装它当前的最新版本。</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/e9/c5/7ecb497f.jpg" width="30px"><span>青松</span> 👍（2） 💬（5）<div>坐等更新！</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/ce/d1/25b26edb.jpg" width="30px"><span>TWJ</span> 👍（1） 💬（1）<div>分享一下。安装pip install plotly过程中报了一堆错，最后显示“ValueError: check_hostname requires server_hostname”，关掉类似VPN的软件，重新执行安装就可以了。</div>2022-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/22/37/61e24c86.jpg" width="30px"><span>抓白兔的大猪文</span> 👍（1） 💬（2）<div>黄老师 在Jupyter中运行代码 pip install plotly 安装模块显示如下报错，是什么原因？
File &quot;C:\Users\APPLE\AppData\Local\Temp&#47;ipykernel_1520&#47;347750890.py&quot;, line 2
    pip install plotly
        ^
SyntaxError: invalid syntax</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/35/34/18caeb26.jpg" width="30px"><span>Null</span> 👍（1） 💬（1）<div>不显示绘图的解决：
pip install cufflinks
import cufflinks as cf
#这两句是离线生成图片的设置
cf.go_offline()
cf.set_config_file(offline=True, world_readable=True)</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/c0/51/77cce580.jpg" width="30px"><span>刘东君</span> 👍（0） 💬（1）<div>请教老师，能否直接用vs code内置的jupyter notebook呢？</div>2024-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bf/6f/1916fba0.jpg" width="30px"><span>贝贝</span> 👍（0） 💬（1）<div> import pandas as pd # 导入Pandas
stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;] # 漏斗的阶段
# 漏斗的数据
df_male = pd.DataFrame(dict(number=[30, 15, 10, 6, 1], stage=stages))
df_male[&#39;性别&#39;] = &#39;男&#39;
df_female = pd.DataFrame(dict(number=[29,17,8,3,1], stage=stages))
df_female[&#39;性别&#39;] = &#39;女&#39;
df = pd.concat([df_male, df_female], axis=0) # 把男生女生的数据连接至一个新的Dataframe对象df
# print(df)
fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;性别&#39;) # 把df中的数据传进漏斗
fig.show()

看起来很简单，和前端使用echarts画图差不多，问题是需要熟悉pandas</div>2024-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/4f/61/018352d4.jpg" width="30px"><span>静静呀</span> 👍（0） 💬（1）<div>import pandas as pd
stages = [&quot;访问数&quot;,&quot;下载数&quot;,&quot;注册数&quot;,&quot;搜索数&quot;,&quot;下单数&quot;]
data_male =pd.DataFrame(dict(data = [50,35,20,10,5],stage = stages))
data_male[&#39;性别&#39;] = &#39;男&#39;
data_fmale = pd.DataFrame(dict(data = [40,30,20,10,6],stage = stages))
data_fmale[&#39;性别&#39;] = &#39;女&#39;
df = pd.concat([data_male,data_fmale],axis = 0)
fig = px.funnel(df,x = &#39;data&#39;,y=&#39;stage&#39;,color = &#39;性别&#39;)
fig.show()</div>2023-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/4f/61/018352d4.jpg" width="30px"><span>静静呀</span> 👍（0） 💬（1）<div>老师，pip install plotly 提示让在IPython shell之外运行，我在cmd 运行安装成功了，但是在jupyter 运行import plotly 还是会报错No module named &#39;plotly&#39;，请问是什么原因呢？安装时是否需要指定路径</div>2023-10-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（0） 💬（1）<div>import plotly.express as px
第一张图片漏了以上这个包.</div>2023-09-24</li><br/><li><img src="" width="30px"><span>Geek_7839ab</span> 👍（0） 💬（1）<div>参考官方文档https:&#47;&#47;plotly.com&#47;python&#47;funnel-charts&#47;</div>2023-09-11</li><br/><li><img src="" width="30px"><span>catmao</span> 👍（0） 💬（1）<div>黄老师，您好，听了您的课，也买了您的书，但是在执行书中的案例时，遇到了问题。不知道为什么在使用kaggle中，notebook右面并没有setting设置选项，无法进行Internet的设置，直接在线运行？</div>2023-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/80/81/791d0f5e.jpg" width="30px"><span>jinsiang_sh</span> 👍（0） 💬（1）<div>import pandas as pd # 导入Pandas
stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;] # 漏斗的阶段
# 漏斗的数据
df_male = pd.DataFrame(dict(number=[59, 32, 18, 9, 2], stage=stages))
df_male[&#39;性别&#39;] = &#39;男&#39;

df_female = pd.DataFrame(dict(number=[37, 41, 18, 6, 5], stage=stages))
df_female[&#39;性别&#39;] = &#39;女&#39;

df = pd.concat([df_male, df_female], axis=0) # 把男生女生的数据连接至一个新的Dataframe对象df

fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;性别&#39;) # 把df中的数据传进漏斗
fig.show()</div>2023-03-21</li><br/><li><img src="" width="30px"><span>冯仁彬</span> 👍（0） 💬（1）<div>import pandas as pd # 导入Pandas
stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;] # 漏斗的阶段
# 漏斗的数据
df_male = pd.DataFrame(dict(number=[30, 15, 10, 6, 1], stage=stages))
df_male[&#39;性别&#39;] = &#39;男&#39;
df_female = pd.DataFrame(dict(number=[29, 17, 8, 3, 1], stage=stages))
df_female[&#39;性别&#39;] = &#39;女&#39;
df = pd.concat([df_male, df_female], axis=0) # 把男生女生的数据连接至一个新的Dataframe对象df
fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;性别&#39;) # 把df中的数据传进漏斗
fig.show()</div>2022-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/c4/2b/b3f917ec.jpg" width="30px"><span>一颗红心</span> 👍（0） 💬（1）<div>简单易学，很有成就感。点赞</div>2022-07-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLSYbuvZOUtOddqCVrktJu4uQaeYjJIEnDXkexCFW6FFYv9fUnhJbr1cvzuiaChgsoN6icEKXPmJfUA/132" width="30px"><span>Geek_ad8af6</span> 👍（0） 💬（1）<div>import pandas as pd # 导入Pandas
stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;] # 漏斗的阶段
# 漏斗的数据
df_male = pd.DataFrame(dict(number=[30, 15, 10, 6, 1], stage=stages))
df_male[&#39;性别&#39;] = &#39;男&#39;
df_female = pd.DataFrame(dict(number=[20, 14, 8, 5, 3], stage=stages))
df_female[&#39;性别&#39;] = &#39;女&#39;
df = pd.concat([df_male, df_female], axis=0) # 把男生女生的数据连接至一个新的Dataframe对象df
fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;性别&#39;) # 把df中的数据传进漏斗
fig.show()</div>2022-06-28</li><br/><li><img src="" width="30px"><span>Geek_bdfd93</span> 👍（0） 💬（1）<div>请问老师在jupyter notebook launch的时候发生-10673的错误是怎么回事</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/6e/f5ee46e8.jpg" width="30px"><span>海滨</span> 👍（0） 💬（1）<div>不知道有没有使用visual studio code来编写jupyter notebook，最后在显示漏斗图出现这种报错的情况？No renderer could be found for MIME type: application&#47;vnd.plotly.v1+json
我贴下我的解决方案，在import ploty包前面添加如下代码
# 解决vs code报错找不到render无法直接显示plotly图表问题
import plotly.io as pio
pio.renderers.default = &quot;notebook_connected&quot;</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5a/65/b80035a6.jpg" width="30px"><span>ryan</span> 👍（0） 💬（1）<div>真的很基础😁适合入门</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/d6/f8/cb21b43c.jpg" width="30px"><span>松饼Muffin</span> 👍（0） 💬（1）<div>stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;] # 漏斗的阶段
# 漏斗的数据
df_male = pd.DataFrame(dict(number=[30, 15, 10, 6, 1], stage=stages, gender=&#39;male&#39;))
df_female = pd.DataFrame(dict(number=[29, 17, 8, 3, 1], stage=stages, gender=&#39;female&#39;))
df = pd.concat([df_male, df_female], axis=0) # 把男生女生的数据连接至一个新的Dataframe对象df
fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;gender&#39;) # 把df中的数据传进漏斗
fig.show()</div>2022-03-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bmgpp5wc8GLmOdHNQccSgrunK0VdIicB6rpTHXCTF5xEkm2YvPHOX2DwNt2EqTzJ70JD41h0u5qW4R0yXRY1ZCg/132" width="30px"><span>Eazow</span> 👍（0） 💬（1）<div>stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;]
df_male = pd.DataFrame(dict(number=[59, 32, 18, 9, 2], stage=stages, gender=[&quot;男&quot;] * 5))
df_female = pd.DataFrame(dict(number=[29, 17, 8, 3, 1], stage=stages, gender=[&quot;女&quot;] * 5))

px.funnel(pd.concat([df_male, df_female]), x=&quot;number&quot;, y=&quot;stage&quot;, color=&quot;gender&quot;).show()</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/24/39/5300ca6f.jpg" width="30px"><span>Cal</span> 👍（0） 💬（1）<div>import pandas as pd
import plotly.express as px #导入Plotly.express工具，命名为px
stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;]
df_male = pd.DataFrame(dict(number=[59, 32, 18, 9, 2], stage=stages))
df_male[&#39;性别&#39;] = &#39;男&#39;
df_female = pd.DataFrame(dict(number=[37, 41, 18, 6, 5], stage=stages))
df_female[&#39;性别&#39;] = &#39;女&#39;
df = pd.concat([df_male, df_female],axis=0)
fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;性别&#39;)
fig.show()</div>2022-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/da/29fe3dde.jpg" width="30px"><span>小宝</span> 👍（0） 💬（1）<div>import pandas as pd
stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;] 
data_male = dict(number=[30, 15, 10, 6, 1], stage=stages)
df_male = pd.DataFrame(data_male)
df_male[&#39;性别&#39;] = &#39;男&#39;

data_female = dict(number=[29, 17, 8, 3, 1], stage=stages)
df_female = pd.DataFrame(data_female)
df_female[&#39;性别&#39;] = &#39;女&#39;

df = pd.concat([df_male, df_female], axis=0)
fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;性别&#39;)

fig.show()</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/b2/24/3b1d2755.jpg" width="30px"><span>Geek_b8d28c</span> 👍（0） 💬（1）<div>import pandas as pd # 导入Pandas
stages = [&quot;访问数&quot;, &quot;下载数&quot;, &quot;注册数&quot;, &quot;搜索数&quot;, &quot;付款数&quot;] # 漏斗的阶段
# 漏斗的数据
df_male = pd.DataFrame(dict(number=[30, 15, 10, 6, 1], stage=stages))
df_male[&#39;性别&#39;] = &#39;男&#39;
df_female = pd.DataFrame(dict(number=[29,17,8,3,1],stage=stages))
df_female[&#39;性别&#39;]=&#39;女&#39;
df = pd.concat([df_male, df_female], axis=0) # 把男生女生的数据连接至一个新的Dataframe对象df
fig = px.funnel(df, x=&#39;number&#39;, y=&#39;stage&#39;, color=&#39;性别&#39;) # 把df中的数据传进漏斗
fig.show()</div>2021-12-19</li><br/>
</ul>