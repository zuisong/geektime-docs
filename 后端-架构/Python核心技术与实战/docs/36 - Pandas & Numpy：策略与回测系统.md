大家好，我是景霄。

上节课，我们介绍了交易所的数据抓取，特别是orderbook和tick数据的抓取。今天这节课，我们考虑的是，怎么在这些历史数据上测试一个交易策略。

首先我们要明确，对于很多策略来说，我们上节课抓取的密集的orderbook和tick数据，并不能简单地直接使用。因为数据量太密集，包含了太多细节；而且长时间连接时，网络随机出现的不稳定，会导致丢失部分tick数据。因此，我们还需要进行合适的清洗、聚合等操作。

此外，为了进行回测，我们需要一个交易策略，还需要一个测试框架。目前已存在很多成熟的回测框架，但是为了Python学习，我决定带你搭建一个简单的回测框架，并且从中简单一窥Pandas的优势。

## OHLCV数据

了解过一些股票交易的同学，可能知道K线这种东西。K线又称“蜡烛线”，是一种反映价格走势的图线。它的特色在于，一个线段内记录了多项讯息，相当易读易懂且实用有效，因此被广泛用于股票、期货、贵金属、数字货币等行情的技术分析。下面便是一个K线示意图。

![](https://static001.geekbang.org/resource/image/47/9b/470a68b8eaff3807efd89bc616e5659b.png?wh=730%2A320)

K线示意图

其中，每一个小蜡烛，都代表着当天的开盘价（Open）、最高价（High）、最低价（Low）和收盘价（Close），也就是我画的第二张图表示的这样。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（44） 💬（1）<div>整理后的代码在这里：https:&#47;&#47;github.com&#47;Eyelidstl&#47;GeekTimePythonClass</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（2） 💬（1）<div>这章比较难了，照着课程敲代码，调了半天可以运行了，结果却不对。把老师的代码下载回来仔细研究，终于清楚一些了。</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/e7/e4b4afcc.jpg" width="30px"><span>方向</span> 👍（9） 💬（0）<div>有没有整理后的源代码，想统一查看</div>2019-07-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jsMMDDzhbsTzhicsGZiaeV0PWSnAS0fBlb1r6CsuB32vr3hRwV9UubmfHQx45v7jtaXajPlQ8kQ17b3zpQzHmqVw/132" width="30px"><span>fy</span> 👍（6） 💬（0）<div>老师，可以用git管理每次分析的代码么？</div>2019-07-31</li><br/><li><img src="" width="30px"><span>Geek_kuntena</span> 👍（5） 💬（0）<div>pandas 的 resample 函数方便的进行合成大周期的k线数据</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/b6/f3f68a39.jpg" width="30px"><span>马建华</span> 👍（3） 💬（0）<div>    def buy(self):
        &quot;&quot;&quot;
        用当前账户剩余资金，按照市场价格全部买入
        :return:
        &quot;&quot;&quot;
        self._position = float(self._cash &#47; (self.current_price * (1 + self._commission)))
        self._cash = 0.0

老师，这里应该是：self._position = float(self._cash * (1-self._commission) &#47; (self.current_price))吧？</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/b6/f3f68a39.jpg" width="30px"><span>马建华</span> 👍（3） 💬（0）<div>assert_msg(isinstance(commission, Number), &#39;commission不是浮点数值类型&#39;)为何不是用float而是number</div>2020-08-10</li><br/><li><img src="" width="30px"><span>宋强</span> 👍（2） 💬（1）<div>按照代码逻辑实现了一遍，发现即便是交易经手费是0，最后的收益也很大取决于数据本身。策略并不一定能盈利</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（1） 💬（0）<div>SMA函数只做了一件事：pd.Series(values).rolling(n).mean()
将传入的values转成一位数组以n个数据为单位滚动切分取平均值，返回一个均值数组
SMA的调用位置：
SmaCross在继承Strategy后必须要重写的抽象方法init中：
self.sma1 = self.I(SMA, self.data.Close, self.fast)  # 用收盘价计算的10日均线
self.sma2 = self.I(SMA, self.data.Close, self.slow)  # 用收盘价计算的20日均线

提议：数据可视化更能直观表达实现策略的方案。</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（1） 💬（0）<div>30日均线、10日均线、5日均线、小时、分钟...
大窗口SMA -&gt; 小窗口SMA
策略：小窗口SMA从下穿过大窗口SMA，买入。大窗口SMA从下方突破小窗口 SMA，卖出。
这要先看看股市的简单策略分析才能明白。刚开始看，完全不懂。。。</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/97/fb/7cfc315e.jpg" width="30px"><span>长青</span> 👍（1） 💬（1）<div>老师iself._indicators.append(value)这一步有有什么意义呢   没大看明白。还有
buy和sell是不是应该在下一根K线执行才对？比如我指标计算时用的15分钟K线   在10:15分出现买卖信号后，应该在10:30执行操作 ，因为指标时根据收盘价计算的

</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第36讲打卡~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/89/34f2cbcc.jpg" width="30px"><span>杨宇</span> 👍（0） 💬（0）<div>def __init__(self, data: pd.DataFrame, ...)
def crossover(series1, series2) -&gt; bool: ...
——方法参数、返回值，怎么带类型了，之前的课没教过这种写法吧？</div>2021-12-05</li><br/><li><img src="" width="30px"><span>rock feng</span> 👍（0） 💬（0）<div>这堂课，看得我迷糊，第一次接触量化交易，太多知识点....</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/e5/f1/880994da.jpg" width="30px"><span>忧伤的胡萝卜</span> 👍（0） 💬（0）<div>assert_msg(not data[[&#39;Open&#39;, &#39;High&#39;, &#39;Low&#39;, &#39;Close&#39;]].max().isnull().any(), (&#39;部分OHLC包含缺失值，请去掉那些行或者通过差值填充. &#39;)) 请问这里为什么要用.max().isnull().any()来进行判空？</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/42/78/212d3762.jpg" width="30px"><span>啟俊</span> 👍（0） 💬（0）<div>老师可以讲一下pandas中apply的应用，有什么方法可以替代，优化提升运行效率</div>2019-08-07</li><br/><li><img src="" width="30px"><span>瞳梦</span> 👍（0） 💬（0）<div>assert_msg(not data[[&#39;Open&#39;, &#39;High&#39;, &#39;Low&#39;, &#39;Close&#39;]].max(skipna=False).isnull().any()这一行max()方法应该要加一个参数: skipna=False</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/42/d7/1f1634af.jpg" width="30px"><span>无才不肖生</span> 👍（0） 💬（0）<div>而想要检查某个时刻两个 SMA 是否交叉，你只需要查看两个数...
这个我理解的有问题吗，只拿最后两人数作比较不能确定吧，窗口设置10个数时，可能在1到8个数时相等，不是判断不准确？</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（0） 💬（2）<div>    def buy(self):
        &quot;&quot;&quot;
        用当前账户剩余资金，按照市场价格全部买入
        &quot;&quot;&quot;
        self._position = float(self._cash &#47; (self.current_price * (1 + self._commission)))
        self._cash = 0.0

老师，你这里手续费的计算方式有问题吧？ 手续费是针对每次交易来算，不是针对每个比特币来算的吧</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>看了老师的文章，对金融又感兴趣了。</div>2019-07-31</li><br/>
</ul>