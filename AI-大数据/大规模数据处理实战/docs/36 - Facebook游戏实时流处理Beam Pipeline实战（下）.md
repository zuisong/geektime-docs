你好，我是蔡元楠。

在上一讲中，我们一起对怎样实现一个简易的游戏积分排行榜展开了讨论，也一起研究了如何使用批处理计算的方式在Beam中构建出一个数据流水线来得出排行榜结果。

我们知道，虽然批处理计算可以得到一个完整的结果，但是它也存在着自身的不足，比如会有一定的延时，需要额外的crontab来管理定时任务，增加了维护成本等等。

所以在上一讲的末尾，我们提出了使用实时流处理来改进这些不足，而其中就需要用到窗口、触发器和累加模式这几个概念。

相信学习了[第32讲](https://time.geekbang.org/column/article/105707)的内容后，你对于窗口在Beam中是如何运作的，已经比较了解了。对于有效时间为一周的积分排行榜来说，我们可以赋予一个“窗口时长为一周的固定窗口”给数据流水线。也就是说，我们最终的结果会按照每一周的时长来得出。

那接下来的问题就剩下我们怎么定义触发器和累加模式了。

首先，我想先讲讲触发器在Beam中是怎么运作的。在[第23讲](https://time.geekbang.org/column/article/100478)中，我们已经了解了触发器在Beam中的作用。它是用于告诉数据流水线，什么时候需要计算一遍落在窗口中的所有数据的。这在实时流处理中尤为重要。

在实时流处理当中，我们总是需要在数据结果的**完整性**和**延迟性**上做出一些取舍。

如果我们设置的触发器比较频繁，例如说每隔几分钟甚至是几秒钟，或者是在时间上很早发生的话，那就表示我们更倾向于数据流水线的延时比较小，但是不一定能够获得完整的数据。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f0/3e/f9f021bf.jpg" width="30px"><span>Geeker</span> 👍（1） 💬（1）<div>例子很好！</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（6） 💬（1）<div>老师讲的很好！要是能提供一个完整的案例，包括测试数据和运行时，不需要读者折腾太多，下载下来直接就能运行，相信会引起更多的共鸣，将这个专栏衬托得更加精彩！</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8d/d4/64eae0b3.jpg" width="30px"><span>时光机器</span> 👍（3） 💬（0）<div>感觉这个例子没有提现出流式计算的实时特性呀。老师能举个像阿里实时战报看板这样高实时性要求的例子吗，感谢感谢</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a0/f4/7e122a67.jpg" width="30px"><span>之渊</span> 👍（1） 💬（0）<div>参考https:&#47;&#47;blog.csdn.net&#47;a799581229&#47;article&#47;details&#47;106444576 这个博客入门以及触发器说明的也不错</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/0b/d475f530.jpg" width="30px"><span>Cool</span> 👍（1） 💬（0）<div>觉得这些例子逻辑上还是相对来说比较简单， 流式处理当输入源是多个的时候， 比如对于交易所来说  一个是实时 trade,  一个是实时的 price，都使用相同的 fix_window,  join 起来之后，再做计算输出等等</div>2019-09-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dAkTIgz3sFoO20qQMbRiaRqWrpicIWiaLMbkeLkribTOUvrzDZPOaRfZgQOvTtAgib35D7DKFiarejer74F4Qs0771mQ/132" width="30px"><span>stephen</span> 👍（0） 💬（0）<div>如果窗口跟滑动步长一样或者更大，比如推荐点击率，20秒窗口，每20秒计算一次，也要允许延迟前一个窗口期甚至几个窗口期的延迟数据重新计算，这种beam能好的支持么？还是说只能借助外部hbase一类实时转储结果？</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/0b/d475f530.jpg" width="30px"><span>Cool</span> 👍（0） 💬（1）<div>蔡老师， 对于流处理需要对pipeline中的数据，进行数据补充时，可以使用 sideinput, 但是我看了官方文档，只能是静态的metadata，然后再Pardo中加到每一条数据， 并不能动态更新这个sideinput（比如在数据库中动态查询), 请问这种情况能怎么解决？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/b0/77e5f8c8.jpg" width="30px"><span>李孟聊AI</span> 👍（0） 💬（1）<div>老师我想问下， PCollection&lt;String&gt;这个种懒加载出来的集合怎么转存成临时的list集合？</div>2019-07-24</li><br/>
</ul>