你好，我是姚秋辰。

在上节课中，我们通过Spring Cloud Stream和RabbitMQ落地了两个业务场景，实现了用户领券和删除券的操作。如果在Consumer消费消息的时候发生了异常，比如用户领取的优惠券超过了券模板约定的上限，或者用户想要删除一张压根不存在的券，那么Consumer会抛出一个运行期异常。你知道在Stream中有哪些优雅的异常处理方式呢？

你可以调用deleteCoupon接口删除一张不存在的优惠券，人为制造一个异常场景，你会观察到，在Consumer端的日志中，当前消费者逻辑被执行了三次。这三次执行包括首次消息消费和两次重试，这就是Stream默认的一种异常处理方式：消息重试。

接下来，我先带你从本地重试出发，看下如何在消费者端配置重试规则。然后再进一步带你了解消息降级和死信队列这两个异常处理手段。

## 消息重试

消息重试是一种简单高效的异常恢复手段，当Consumer端抛出异常的时候，Stream会自动执行2次重试。重试次数是由ConsumerProperties类中的maxAttempts参数指定的，它设置了一个消息最多可以被Consumer执行几次。

```plain
private int maxAttempts = 3;
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（4） 💬（1）<div>事务消息是针对发送者的，消费者要确保做好异常处理和重试逻辑。


基于RocketMQ或Kafka的事务消息，实现分布式事务：
（1）订单系统在消息队列上开启一个事务
（2）订单系统给消息服务器发送一个“半消息”，半消息和普通消息的唯一区别是，在事务提交之前，对于消费者来说，这个消息是不可见的。
（3）半消息发送成功后，订单系统就可以执行本地事务了，在订单库中创建一条订单记录，并提交订单库的数据库事务。
（4）根据本地事务的执行结果决定提交或者回滚事务消息。如果这一步失败，kafka是直接抛出异常，让用户在业务层代码自己处理；RocketMQ 中的事务实现中，增加了事务反查的机制来解决事务消息提交失败的问题。
（5）投递消息，消费者先执行消费的逻辑，只有消费逻辑执行成果后再进行消息的ack确认</div>2022-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（3） 💬（1）<div>老师，我在测试requeue的时候，只设置requeue-rejected: true无法生效，需要同步设置auto-bind-dlq: false,这样才能生效，是不是我的版本问题？</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师两个关于Gateway的问题：
Q1：Spring Gateway和Nacos、微服务应用通信是用RPC还是Rest API？
Q2：Spring Gateway内部有“微服务客户端”吗？</div>2022-02-21</li><br/>
</ul>