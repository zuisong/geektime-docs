你好，我是尹会生。

在上一讲中，我们学习了怎么使用Seaborn来生成图片格式的图表。事实上，图片格式的图表也被称作静态图表，它能通过数据来更直观地展示结果。

不过很多时候，我们不仅要通过图片直观地展示数据，还要让图片容纳更多种类、更丰富的数据信息。这个时候，静态图表能展示的结果就十分有限了。比如你希望能给领导和同事在会议上演示数据的分析结果时，需要通过一张图来容纳更多的数据。

别担心，这时候我们可以**采用动态图表的方法，来增强图片的表现力**。因为动态图表展示的结果，相当于静态图表和数据这两者的混合，所以容纳的内容信息也就更丰富。

举个例子，我希望用一张图片来展示全国新冠确诊病例的分布。如果采用动态图，我就可以把鼠标移动到我需要查看的省份上面，显示该地区的确诊人数等相关信息。

就像下面这张截图一样。这张分布图不但基于颜色深浅显示了确诊人数的变化，还能通过鼠标悬停来显示具体的数据。使用起来是不是很方便？

![](https://static001.geekbang.org/resource/image/60/01/6063f764e3493cb69b2922b1988dcf01.png?wh=803%2A603)

这张动态图表是使用HTML网页文件格式来展示的。同时，它也采用了Python的库pyecharts进行了绘制，其中的图形、数据都可以基于你的需要进行调整。最重要的是，绘制这样一张图片，操作起来和seaborn生成静态图表一样简单。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/7d/368df396.jpg" width="30px"><span>somenzz</span> 👍（1） 💬（1）<div>思考题：定时任务，先删除文件，然后执行下上述脚本，控制浏览器强制刷新。</div>2021-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/34/70/6bd49fab.jpg" width="30px"><span>任</span> 👍（1） 💬（1）<div>如何生成图片放在PPT中或者纯粹是PPT</div>2021-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/8d/abb7bfe3.jpg" width="30px"><span>Ed_Lee™</span> 👍（0） 💬（1）<div>之前在工作中，用plotly做过类似的动态分析图（数据格式是dataframe），当时觉得图例类型也覆盖的很全；听说echarts很强大，但自己一直也没用过

因此想请教下，plotly和echarts之间对比，它们会有很不一样的适用场景吗？</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/0c/c438c5df.jpg" width="30px"><span>天国之影</span> 👍（0） 💬（1）<div>如果使用Jupyter Notebook运行，可以使用map_chart.render_notebook()进行展示
代码示例：https:&#47;&#47;relph1119.github.io&#47;TechBooks-ReadingNote&#47;#&#47;python_office_automation&#47;section05</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/7a/0b/b0d918da.jpg" width="30px"><span>谢韬 Fragos</span> 👍（1） 💬（0）<div>为了让加载的这些json数据容易阅读， 我写了下面的代码让数据结构匹配缩进。运行后就很容找到areaTree 和children 。 

import requests
import json

url=&#39;https:&#47;&#47;view.inews.qq.com&#47;g2&#47;getOnsInfo?name=disease_h5&#39;
data = requests.get(url)
print (data)

alldata= json.loads(data.json()[&#39;data&#39;])
print(alldata)
print(type(alldata))

readable_file = &#39;readable_eq_data.json&#39;
with open(readable_file,&#39;w&#39;,encoding=&#39;utf8&#39;) as f:
    json.dump(alldata,f,indent=4,ensure_ascii= False)</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-22</li><br/>
</ul>