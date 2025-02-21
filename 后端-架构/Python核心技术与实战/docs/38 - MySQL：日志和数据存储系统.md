你好，我是景霄。今天这节课，我们来聊聊日志和存储系统。

在互联网公司中，日志系统是一个非常重要的技术底层。在每一次重要的交互行为中，关键信息都会被记录下来存档，以供日后线下分析，或者线上实时分析。这些数据，甚至可以说是硅谷互联网大公司的命脉所在。

有了它们，你才能建立机器学习模型来预测用户的行为，从而可以精确描绘用户画像，然后针对性地使用推荐系统、分类器，将用户进一步留下，并精准推送广告来盈利。

在量化交易中，日志同样有着非常重要的作用。一如前面所讲，我们重要的数据有：行情数据、策略信号、执行情况、仓位信息等等非常多的信息。

对于简单的、小规模的数据，例如 orderbook 信息，我们完全可以把数据存在 txt、csv 文件中，这样做简单高效。不过，缺点是，随着数据量上升，一个文件将会变得非常大，检索起来也不容易。这时，一个很直观的方式出现了，我们可以把每天的数据存在一个文件中，这样就暂时缓解了尴尬。

但是，随着数据量的上升，或者是你的算法逐渐来到高频交易领域时，简单地把数据存在文件上，已经不足以满足新的需求，更无法应对分布式量化交易系统的需求。于是，一个显而易见的想法就是，我们可以把日志存在数据库系统中。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（11） 💬（1）<div>思考题：
对于高频调用数据，可以考虑在系统启动时把数据从数据库中一次性加载到内存中，并以某种数据结构如DataFrame之类的存贮结构化数据，或以键-值对形式存贮数据，这样就可以避免每次调用时都去访问数据库，可以极大提高访问效率。
另外，也可以考虑把数据放到内存数据库中，如Redis中，以键-值对形式存贮高频数据，这样就可以快速访问高频数据。</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（18） 💬（0）<div>思考题：想到2点，其他想不到
1.以空间换时间，缓存大法。
2.以提前量换时间，例如回测系统中对ohlcv中的计算可以提前做好，放入内存，这部分时间在高频时就省下来了。</div>2019-08-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（10） 💬（0）<div>评论说的很好，一般先用索引进行优化，如果性能还是不够，需要极致的读取延迟，可以考虑内存数据库，redis 是一个很好的例子。</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/3d/2a3b67f8.jpg" width="30px"><span>catshitfive</span> 👍（6） 💬（1）<div>这个Price类看不太明白，老师能细讲下吗(里面还包含了一个内部类Meta)</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/c0/c6880c07.jpg" width="30px"><span>magician</span> 👍（3） 💬（0）<div>高频查询数据使用nosql数据库比如redis做缓存</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（2） 💬（1）<div>这一节是理论，下一节应该就是实操了。</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/07/2f418316.jpg" width="30px"><span>恰饭哒</span> 👍（1） 💬（0）<div>ELK在Python生态中怎么样啊</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（1） 💬（0）<div>回测中重复计算的数据先缓存到数据库里，避免重复计算。</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（1） 💬（0）<div>sql调优相关内容：经常进行检索的字段上创建索引，索引可提高select效率但同时也降低了insert和update的效率，一个表最多可有6个索引，避免在索引列上做计算，用varchar变长代替char定长，使用临时表暂存中间结果等。</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第38讲打卡~</div>2024-07-17</li><br/><li><img src="" width="30px"><span>Geek_cf3aed</span> 👍（0） 💬（0）<div>我使用的是华为p40 无法使用文本中提供代码的    复制  功能</div>2021-07-14</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppQqDE6TNibvr3DNdxG323AruicIgWo5DpVr6U7yZVNkbF2rKluyDfhdpgAEcYEOZTAnbrMdTzFkUw/0" width="30px"><span>图·美克尔</span> 👍（0） 💬（0）<div>1. 索引
2. 消息队列
3. redis</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/48/77/f19fe773.jpg" width="30px"><span>张鑫</span> 👍（0） 💬（0）<div>采用联合索引</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（0） 💬（0）<div>老师，你好，那种微服务的分布式日志怎么搜集呢</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/86/bdf2ad51.jpg" width="30px"><span>©HJ</span> 👍（0） 💬（0）<div>请问老师，量化数据库用MySQL比较好，还是用MongoDB？谢谢
</div>2019-08-05</li><br/>
</ul>