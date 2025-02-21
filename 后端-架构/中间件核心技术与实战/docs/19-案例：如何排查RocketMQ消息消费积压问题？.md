你好，我是丁威。

我想，几乎每一位使用过消息中间件的小伙伴，都会在消息消费时遇到消费积压的问题。在处理这类问题时，大部分同学都会选择横向扩容。但不幸的是，这种解决办法治标不治本，到最后问题还是得不到解决。

说到底，消费端出现消息消费积压是一个结果，但引起这个结果的原因是什么呢？**在没有弄清楚原因之前谈优化和解决方案都显得很苍白。**

这节课，我们就进一步认识一下消费积压和RocketMQ的消息消费模型，看看怎么从根本上排查消费积压的问题。

## RocketMQ的消息消费模型

在RocketMQ消费领域中，判断消费端遇到的瓶颈通常会用到两个重要的指标：Delay和LastConsumeTime。

在开源版本的控制台rocketmq-console界面中，我们可以查阅消费端的这两个指标：

![图片](https://static001.geekbang.org/resource/image/yy/07/yy0cf8266e7c6c1cb8cfa7caf7562207.png?wh=1039x692)

- Delay指的是消息积压数量，它是由BrokerOffset（服务端当前最大的逻辑偏移量）减去ConsumerOffset（消费者消费的当前位点）计算出来的。**如果Delay值很大，说明消费端遇到了瓶颈**。
- LastConsumeTime表示上一次成功消费消息的存储时间。**这个值如果很大，同样能说明消费端遇到了瓶颈。**如果这个值线上为1970年，表示消费者当前消费位点对应的消息在服务端已经过期，被删除了。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/79/673f4268.jpg" width="30px"><span>小杰</span> 👍（3） 💬（2）<div>因为消费位点是consumer定时发给broker的，而每次发的时候只发最小确认offset，所以有可能消费者挂了又起来，大量消息都得重新消费，老师是这个原因吗？</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/64/457325e6.jpg" width="30px"><span>Sam Fu</span> 👍（1） 💬（1）<div>老师可以讲下消费成功或者失败 本地以及broker offset的更新机制吗？
是每条消息消费完都会更新本地offset还是拉取的一批全部处理完才会更新.

如果这一批有一条消费失败的就全部扔回吗 还是只扔消费失败的</div>2023-02-04</li><br/>
</ul>