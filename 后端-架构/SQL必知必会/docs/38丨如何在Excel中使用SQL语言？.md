在进阶篇中，我们对设计范式、索引、页结构、事务以及查询优化器的原理进行了学习，了解这些可以让我们更好地使用SQL来操作RDBMS。实际上SQL的影响力远不止于此，在数据的世界里，SQL更像是一门通用的语言，虽然每种工具都会有一些自己的“方言”，但是掌握SQL可以让我们接触其它以数据为核心的工具时，更加游刃有余。

比如Excel。

你一定使用过Excel，事实上，Excel的某些部分同样支持我们使用SQL语言，那么具体该如何操作呢？

今天的课程主要包括以下几方面的内容：

1. 如何在Excel中获取外部数据源？
2. 数据透视表和数据透视图是Excel的两个重要功能，如何通过SQL查询在Excel中完成数据透视表和透视图？
3. 如何让Excel与MySQL进行数据交互？

## 如何在Excel中获取外部数据源？

使用SQL查询数据，首先需要数据源。如果我们用Excel来呈现这些数据的话，就需要先从外部导入数据源。这里介绍两种直接导入的方式：

1. 通过OLE DB接口获取外部数据源；
2. 通过Microsoft Query导入外部数据源。

下面我们通过导入数据源heros.xlsx体验一下这两种方式，你可以从[这里](https://github.com/cystanford/SQL-Excel)下载数据源。

### 通过OLE DB接口获取外部数据源
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/aa/db213a66.jpg" width="30px"><span>莫弹弹</span> 👍（15） 💬（2）<div>老师我发现安装 mysql-for-excel-1.3.8.msi 时会报错
The Microsoft Visual Studio Tools for Office Runtime must be nstalled prior to running this istlation.
找了一下微软的说明
ttps:&#47;&#47;docs.microsoft.com&#47;en-us&#47;visualstudio&#47;vsto&#47;how-to-install-the-visual-studio-tools-for-office-runtime-redistributable?view=vs-2019
需要下载 Visual Studio 2010 Tools for Office Runtime 才能运行
下载链接在这里
https:&#47;&#47;www.microsoft.com&#47;zh-CN&#47;download&#47;confirmation.aspx?id=56961</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/aa/db213a66.jpg" width="30px"><span>莫弹弹</span> 👍（10） 💬（1）<div>这个功能也是比较好的报表工具了，产品经理经常让我提取一些数据出来，例如指定时间段的数据，指定用户的业务记录数量，如果有Excel插件和MySQL配合的话，可以实现我从MySQL导出Excel报表的功能，非常方便</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（9） 💬（3）<div>Mac 用户说我太难了😭</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（5） 💬（1）<div>这个功能犹如AWT</div>2019-09-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/D4KnXmgkeITtk6ibZvIKDML36SeicWTnWbqRlKHx32rhicIIsYR8Qru1QDWH4E0SeV8p8xjxayJRCyQzNnlibSWiaGQ/132" width="30px"><span>Geek_aab935</span> 👍（4） 💬（1）<div>老师好，请教一个问题，我要建一张80万条的数据表，数据来自3张表的汇总，我用create table 表名 as 方式建表太慢，有什么好的方式快速建表？</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（3） 💬（1）<div>日常编程的话确实用不到，不过工作中，如果想临时生成一下可视化的图表，用这种方式那确实是很方便的，感谢老师分享。</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/95/32/8c6dc643.jpg" width="30px"><span>jonnypppp</span> 👍（3） 💬（1）<div>平时基本不用，不过涨知识了</div>2019-08-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（3） 💬（0）<div>这个功能比较好，可以直接使用Excel操作SQL</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2b/39/19041d78.jpg" width="30px"><span>😳</span> 👍（3） 💬（0）<div>日常工作没使用过，不过现在知道还能这样玩了</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（2） 💬（2）<div>为什么我在用Microsoft query导入表中数据报错，数据源中没有包含可见的表格，这个怎么解决？</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>长见识了，经常用Excel倒腾数据，不知道还有执行SQL的功能</div>2024-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/da/ab/bc298b94.jpg" width="30px"><span>Geek_664122</span> 👍（0） 💬（0）<div>为啥我无法下载hero.exel</div>2023-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3a/a9/9cba7c32.jpg" width="30px"><span>宇</span> 👍（0） 💬（0）<div>使用 Excel 的自动填充功能来进行姓氏的填写，是具体怎么做的</div>2021-08-26</li><br/>
</ul>