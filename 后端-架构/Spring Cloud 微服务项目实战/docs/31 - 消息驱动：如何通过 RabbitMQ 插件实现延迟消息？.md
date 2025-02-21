你好，我是姚秋辰。

在平时网购的时候，你一定有过下单之后忘记付款的情况，等到再回过头想起要付款，发现订单已经被关闭了，很多网购流程里都有类似的“订单超时关闭”功能。相类似的功能还有“自动确认收货”，如果在一定时间内买家都没有点击确认收货按钮，那么系统会自动确认收货并且将订单款项打给卖家。

我举的这两个例子都有一个共同的特征，那就是业务逻辑会预设在未来的某一个时间点被触发。在早期我们经常会使用TTL+死信队列的方式来实现这种定时事件，通过设置一个正常的消息队列并使用TTL指定超时时间，如果队列中的消息超时了，它就会被DLX（死信交换机）转向死信队列。借助这种曲线救国的方式，你就可以通过MQ组件实现“定时消息”。

相比于TTL+DLX，RabbitMQ提供了一种更为优雅的方式来实现这类业务。在这节课中，我将带你使用RabbitMQ的延迟消息插件，实现延迟发放优惠券的场景。

那么首先，我们先来安装这个延迟消息插件吧。

## 安装插件

你需要先打开RabbitMQ官网并进入到[插件下载页面](https://www.rabbitmq.com/community-plugins.html)，在页面中定位到**rabbitmq\_delayed\_message\_exchange这个插件。**

![图片](https://static001.geekbang.org/resource/image/b8/04/b8c1ee9769b005bb8eb3932b72yy7e04.png?wh=1914x352)

点击插件上的“Releases”链接，你可以看到适配不同RabbitMQ版本的延迟消息插件。我本地安装的的RabbitMQ版本是3.9.8，最新的延迟消息插件的版本是3.9.0，它可以适配3.9.X系列的RMQ组件，所以我建议你下载3.9.0版本对应的rabbitmq\_delayed\_message\_exchange-3.9.0.ez安装包。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/26/9ac98036.jpg" width="30px"><span>招谁惹谁</span> 👍（3） 💬（2）<div>延时消息能取消吗？如果不能取消，业务上还要对超时的已付款的订单再兼容呀。这个是不是定时任务更好一些！</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（1） 💬（1）<div>在电商中 会遇到 下单  -》支付  -》退款    消息的发送点不一样 ，消费点也不一样  怎么保证这个消费成功的顺序呢</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/e2/5768d26e.jpg" width="30px"><span>inrtyx</span> 👍（0） 💬（1）<div>除了mq还有其他方式推荐吗？</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（0） 💬（1）<div>上家公司就遇到过实现任意延时时长消息问题，rabbitmq_delayed_message_exchange这个插件官方说的是有可能适合于生产使用(是性能还是稳定性的考虑、还是出于商业考虑)。为什么官方rabbitmq不推出新特性做支持，而要采用插件？ 目前已知rocketmq只支持队列级别消息，好像也没有进一步去开发任意延时市场消息的趋势，也是为了商业化么？</div>2022-02-28</li><br/>
</ul>