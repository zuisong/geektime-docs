你好，我是叶伟民。

实战案例1存在一个问题，并非所有同学都有一个现成的MIS系统可以改造。对于这部分同学，没有办法深入研究实战案例1。

针对这一点，我推出了实战案例2，它就是“AI读报小助手”。这个实战案例最终的效果是，让大模型每天从国外著名的IT新闻网站CNET获取当天的IT新闻，然后进行摘要和翻译成中文，整理成一份简报，并自动打开给你查阅。

相比实战案例1，这个实战案例可能绝大部分同学都感兴趣，而且比较实用。这样一来，你动手实践，甚至在使用中改进项目的动力也更强，这样也距离我们提升自身RAG能力的目标更进一步。毕竟师傅带进门，修行在个人。

好，我们这就开始今天的内容。

## 效果展示

现在我们来看看这个实战案例的效果。

![](https://static001.geekbang.org/resource/image/04/58/04476607be9cc34dd1d7048b976bec58.jpg?wh=1103x339)  
这个实战案例会通过Windows任务计划每天运行一次Python脚本。在本地电脑上生成一份CNET当天新闻的简报，并通过浏览器自动打开。

这个实战案例的业务价值主要有三点。

第一，没有AI读报小助手的话，我们需要每天打开CNET网站。完成这个案例以后，我们就可以把这一步时间省了。

第二，CNET新闻是英文的，有些同学看起来会比较费劲。这个案例将内容翻译成中文，看起来轻松多了。

第三，CNET新闻是很长的一整篇文章，而且还夹有广告，阅读体验不好。这个案例将对整篇的文章做摘要。这样同学们可以先看摘要，确认文章是自己感兴趣的，然后再点击新闻链接，查看详细内容。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/UWpN1EIAJib8k5iaGISZD1PhjgKOL6I0q6pP8Dic6VEtnj42jzIfk9m89Lug2ROedc1LerrVIrtyVIthNMCq5rZDA/132" width="30px"><span>ティア（Erlin Ma）</span> 👍（1） 💬（1）<div>可以根据需求，只获取感兴趣的类别的文章，或者按照类别分多次获取。
同意类别内的文章，也可以按照喜好或者基于特定指标进行排序后去top##。
说到底，感觉就是信息提供方的推荐策略的反向应用。不知大家是否同意，欢迎讨论。</div>2024-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/f7/a0/3a2aa99f.jpg" width="30px"><span>jfdghb</span> 👍（0） 💬（1）<div>老师，这个爬虫需自己要去学吗</div>2024-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（1）<div>根据自己的喜好，设置不同维度，然后让AI去评分，总分10分，让AI筛选出评分高于8分的文章。这块可以做的简单，也可以很复杂。</div>2024-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/e7/81da1150.jpg" width="30px"><span>小韩爱学习</span> 👍（0） 💬（0）<div>催更+++</div>2024-09-18</li><br/>
</ul>