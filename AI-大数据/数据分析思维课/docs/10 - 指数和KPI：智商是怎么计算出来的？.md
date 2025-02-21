数据给你一双看透本质的眼睛，这里是《数据分析思维课》，我是郭炜。

在日常生活中，我们经常希望用一个数字去衡量一个特别复杂的事物，这样即使是外行也能一下就了解某件事情的程度和分布。

那什么数字可以满足这个苛刻的要求呢？答案是指数。

简单来讲，**凡是用指数描述的东西，都是一个长期存在或者需要大范围衡量的事情。**指数就像一把尺子，把指数放在这里一量，你就能知道现在这个事情所处的状态是怎样的。于是我们经常在生活当中看到各种各样的指数，从空气的污染指数到股票的上证指数，从用户忠诚度指数到智力指数（IQ）等等均是如此。

指数本身的定义很简单，就是变量值除以标准值再乘以100。

![](https://static001.geekbang.org/resource/image/c0/7c/c05b0eb180df22062295d64ae422847c.jpg?wh=1142x640)

接下来你可以想想，如果让你来设计一个数字去代表上海证券交易所整体的行情，你会怎么做呢？

如果你只选一只股票来代表整个上海证券交易所的行情，就会出现很多问题。比如你找的这家公司的股票退市了，那怎么办？或者是它进行了一些股票的增发/除权，突然之间价格变化非常大，那它能代表着当时所有股票的行情吗？

很明显单只股票是无法代表整体行情的，这个时候就轮到指数登场了。

## 简单的指数：上证指数

接下来我就以上证指数为例，带你看一下一个标准的指数应该由什么构成。

首先它得有标准值，也就是分母。你要注意，这个标准值不仅是一个数字值，也代表一个具体的时间点。比如，新的上证综合指数就是以2005年12月30日为基日（即基准日），以当日所有样本股票的市值总值为基期，以1000点为基点来做的分母。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/69/18/74c57d42.jpg" width="30px"><span>80分</span> 👍（13） 💬（4）<div>德鲁克说过，如果一件事你无法衡量它，你就无法增长它。指数的作用便是如此。</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/31/bbb513ba.jpg" width="30px"><span>mtfelix</span> 👍（10） 💬（1）<div>数字中国，最关键的是各种指数的定义和修正机制的建设啊！</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/9f/0a/51a9c792.jpg" width="30px"><span>艺霖子</span> 👍（3） 💬（3）<div>今天课程拔高了。
老师能给我们学院建立一个QQ社群嘛，这样我们学习的过程，也可以互相交流啥的。</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（2） 💬（2）<div>用户留存的计算，可以以自然日作为计算，后来发现有的统计方法是以玩家注册时候24小时来计算。同一个指数指标，因维度不同，而差异蛮大的。</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2a/b1/e34dcb82.jpg" width="30px"><span>SVV</span> 👍（1） 💬（1）<div>想到两个案例，一是现在的天气应用，不局限于提供天气数据本身，还会结合日常生活以及其他数据，提供类似“穿衣指数”“感冒指数”“出行指数”这样的指数，在想要传达的意图上容易理解，但背后的机制往往容易让用户困惑、怀疑其可靠性；二是有些健康监测类产品，在科学的健康数据基础上，通过复杂算法预测出很多难以直接获取的健康指数，比如“内分泌指数”“心肺功能指数”，这种指数的机制不透明是可以理解的，只要满足精确度、有效性即可。</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（1） 💬（1）<div>指数，马上想到的是指数基金，果不其然，有说到上证指数~
指数是个复杂抽象的逻辑值。比如贫富差异的购买力指数？比如天气预报？
说到kpi和okr，不禁觉得公司同时践行这两货的不舒服点。月度、季度的okr指标完成了，却算不上绩效，绩效是okr之外额外的成果……</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/3d/d6f1e2e6.jpg" width="30px"><span>TeddyPM</span> 👍（0） 💬（1）<div>那这么说招蚊子的人就比不招蚊子的人要健康了</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/3d/d6f1e2e6.jpg" width="30px"><span>TeddyPM</span> 👍（0） 💬（1）<div>对于投资来说，买指数就是买国运。指数是衡量一个国家兴衰经济发展的情况。
而对于一件事情要不要拍脑袋的照一堆数据出来。前提是你得有能力造得出来这数字在说吧。</div>2021-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（0） 💬（1）<div>老师想问一个问题那就是标签和指数之间的关系，或者说是我给用户打了一个标签，但是我怎么去衡量这个程度呢？</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/f2/2a9a6e9a.jpg" width="30px"><span>行与修</span> 👍（1） 💬（0）<div>复杂的指数：焦虑指数。怎么去定义，规则如何调整呢？</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/c9/08852337.jpg" width="30px"><span>Haoz</span> 👍（1） 💬（0）<div>指数本质上是对复杂数字以及事物的抽象，用一个相关合理的规则以及动态调整的角度来衡量复杂的东西，从而化繁为简。但如何确定这指数背后的公式，而让它能够真正反映数字背后的信息和价值是非常难的事情，也是需要不断演进和迭代的。</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/cc/a0/bd31d495.jpg" width="30px"><span>陆美芳</span> 👍（0） 💬（0）<div>人的幸福指数</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/09/22/791d0f5e.jpg" width="30px"><span>大寒</span> 👍（0） 💬（0）<div>提到上指，让我想到了CPI，老师，这两种指数是不是都是同一类型的啊</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/42/a0/3926aaa6.jpg" width="30px"><span>漠帆</span> 👍（0） 💬（0）<div>老师，怎么去确认制定的指数是合理还是不合理的呢？</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/6f/93/e5bcd0f4.jpg" width="30px"><span>fahsa</span> 👍（0） 💬（0）<div>上证指数的，“以 1000 点为基点来做的分母”，这个基点是做哪个的分母啊？上证指数计算公式里根本没有提到这个基点吧。</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>怎么建立一个指数呢？</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/f5/72/8cbc5cb3.jpg" width="30px"><span>好困啊</span> 👍（0） 💬（0）<div>数据分析，指标定义，指数可以来描述复杂的业务场景和现实，但是一定不要硬套标准，要结合实际情况</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/dd/07/2a969ace.jpg" width="30px"><span>geigei</span> 👍（0） 💬（0）<div>制定指数或者说评价标准的目的是为了让事物可衡量，但环境是不断变化的，所以指标也需要与时俱进，不断更新。</div>2021-10-27</li><br/><li><img src="" width="30px"><span>Geek5965</span> 👍（0） 💬（1）<div>也就是以基期和计算日的股票收盘价.   以基日和计算日。</div>2021-10-09</li><br/>
</ul>